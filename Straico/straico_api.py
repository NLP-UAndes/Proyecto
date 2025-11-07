"""
Very small Straico API runner — simplified per user request.

Behavior:
- Every time this script runs it sends the prompts (no --live flag required).
- It uses a hardcoded API key and default models (edit constants below to change).
- It only sends text prompts (no files/images/urls).
"""

import os
import sys
import json
import requests
from typing import List, Optional, Dict, Any

# API endpoint
API_URL = "https://api.straico.com/v1/prompt/completion"

# Hardcoded API key and default model(s)
# NOTE: This is insecure if the repository is shared. Keep it for local testing.
API_KEY = "QX-2ZLKkTvI1lr3MjeoHVD5LTz7iRsrHw09U80aHXA55bDURRmB"
DEFAULT_MODELS = ["amazon/nova-micro-v1"]
PROMPT_ID_MAP = {
    "prompt_1": "P1",
    "prompt_2": "P2",
    "prompt_3": "P3",
    "prompt_4": "P4",
}


def send_prompt(message: str, models: Optional[List[str]] = None) -> Dict[str, Any]:
    """Send a single text prompt to Straico and return the parsed response.

    This function always performs a live HTTP request.
    """
    if models is None:
        models = DEFAULT_MODELS

    payload: Dict[str, Any] = {"models": models, "message": message}

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    except requests.exceptions.RequestException as exc:
        return {"error": str(exc)}

    # Parse JSON if available
    try:
        data = resp.json()
    except Exception:
        data = None

    if 200 <= resp.status_code < 300:
        # Try to extract the assistant 'content' text from the common response
        # shape: data -> completions -> <model> -> completion -> choices[0] -> message -> content
        if isinstance(data, dict):
            completions = data.get('data', {}).get('completions', {})
            # If we passed a single model, try to use that key; otherwise take first
            model_key = None
            if models and len(models) == 1:
                model_key = models[0]
            if not model_key and isinstance(completions, dict) and len(completions) > 0:
                model_key = next(iter(completions.keys()))

            if model_key and model_key in completions:
                try:
                    content = completions[model_key]['completion']['choices'][0]['message']['content']
                    return content
                except Exception:
                    pass

        # Fallback: return raw text or the full JSON string
        if data is None:
            return resp.text
        try:
            return json.dumps(data, ensure_ascii=False)
        except Exception:
            return str(data)

    return {"error": f"status={resp.status_code}", "response": data if data is not None else resp.text}


def _import_prompts() -> Dict[str, str]:
    """Load prompt_1..prompt_4 from prompts.py and return as a dict.

    If prompts.py isn't present, returns an empty dict.
    """
    try:
        from . import prompts as p  # type: ignore
    except Exception:
        try:
            import prompts as p  # type: ignore
        except Exception:
            return {}

    out: Dict[str, str] = {}
    for name in ("prompt_1", "prompt_2", "prompt_3", "prompt_4"):
        if hasattr(p, name):
            out[name] = getattr(p, name)
    return out


def _normalize_response(
    raw_response: Any,
    expected_prompt_id: Optional[str],
    input_value: str,
) -> str:
    """Return a string representation of the response with enforced metadata."""
    if isinstance(raw_response, dict) and raw_response.get('error'):
        details = raw_response.get('response')
        try:
            details_str = json.dumps(details, ensure_ascii=False) if details is not None else ''
        except Exception:
            details_str = str(details)
        return f"ERROR: {raw_response['error']} {details_str}".strip()

    text = str(raw_response)
    if not text:
        return text

    try:
        parsed = json.loads(text)
    except Exception:
        return text

    if isinstance(parsed, dict):
        if expected_prompt_id:
            parsed['prompt_id'] = expected_prompt_id
        parsed['input'] = input_value
        text = json.dumps(parsed, ensure_ascii=False)

    return text


def main() -> int:
    """Main runner: send each prompt and print the result.

    Exits with code 0 on success (no HTTP errors), 1 if any prompt returned an
    HTTP/network error.
    """
    # Load prompt templates from prompts.py
    prompts = _import_prompts()
    if not prompts:
        print("No prompts found in prompts.py. Place prompts.py alongside this file.")
        return 1

    # Path to the dataset CSV (semicolon-separated as in the provided file)
    dataset_path = os.path.join(os.path.dirname(__file__), '..', 'modismos_Dataset_Final.csv')
    # If dataset not found in parent folder, try current working directory
    if not os.path.isfile(dataset_path):
        dataset_path = os.path.join(os.getcwd(), 'modismos_Dataset_Final.csv')
    if not os.path.isfile(dataset_path):
        print(f"Dataset CSV not found at expected locations. Looked for: {dataset_path}")
        return 1

    import csv

    # Read dataset (expects semicolon delimiter with header including 'modismo' and 'ejemplo')
    rows = []
    seen_modismos = set()
    with open(dataset_path, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for r in reader:
            # Normalize keys and keep needed fields
            modismo = r.get('modismo', '')
            modismo = modismo.strip() if isinstance(modismo, str) else ''
            if not modismo:
                continue

            modismo_key = modismo.casefold()
            if modismo_key in seen_modismos:
                continue
            seen_modismos.add(modismo_key)

            ejemplo_val = r.get('ejemplo', '')
            ejemplo = ejemplo_val.strip() if isinstance(ejemplo_val, str) else ''

            rows.append({
                'modismo': modismo,
                'ejemplo': ejemplo
            })

    # Limit to first 50 rows for testing convenience
    rows = rows[:50]

    # For each prompt, create an output CSV with columns: modismo, model1, model2, ...
    for pid, template in prompts.items():
        out_path = os.path.join(os.getcwd(), f'responses_{pid}.csv')
        print(f"Processing {pid} -> writing responses to {out_path}")

        # Determine which input to use per row: if the template contains the word
        # 'ejemplo' before the placeholder, use the dataset 'ejemplo' column;
        # otherwise use the 'modismo' column.
        placeholder_index = template.find("{{input}}")

        use_ejemplo_if_present = False
        if placeholder_index != -1:
            prefix = template[:placeholder_index].lower()
            if 'ejemplo' in prefix:
                use_ejemplo_if_present = True

        models = DEFAULT_MODELS

        # Prepare CSV header using actual model ids (sanitized for CSV column names)
        def _col_name(m: str) -> str:
            # Replace characters that are inconvenient in CSV headers
            return m.replace('/', '_').replace(':', '_')

        header = ['modismo'] + [_col_name(m) for m in models]

        with open(out_path, 'w', encoding='utf-8', newline='') as outf:
            writer = csv.writer(outf)
            writer.writerow(header)

            # Iterate dataset rows and call API for each model
            total = len(rows)
            for idx, r in enumerate(rows, start=1):
                mod = r['modismo']
                ejemplo = r.get('ejemplo', '')
                input_text = ejemplo if (use_ejemplo_if_present and ejemplo) else mod

                # Fill template
                prompt_text = template.replace('{{input}}', input_text)

                responses = []
                for m in models:
                    # send_prompt expects a list of models; we pass one at a time
                    resp = send_prompt(prompt_text, models=[m])
                    expected_prompt_id = PROMPT_ID_MAP.get(pid)
                    resp_str = _normalize_response(resp, expected_prompt_id, input_text)
                    responses.append(resp_str)

                writer.writerow([mod] + responses)
                # Periodic progress output so user sees the script is running
                if idx % 50 == 0 or idx == total:
                    print(f"{pid}: processed {idx}/{total} rows")
                    # flush to ensure output appears promptly
                    try:
                        outf.flush()
                    except Exception:
                        pass

    return 0


if __name__ == '__main__':
    code = main()
    sys.exit(code)