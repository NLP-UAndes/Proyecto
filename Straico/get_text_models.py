"""
Script para obtener y filtrar modelos de Straico que solo soportan texto (no imágenes).
"""

import json
import requests
from typing import Dict, Any, List

# API Key
API_KEY = "8z-9jQAA88DqGOwysRF8KtHVN46DusE1HicHFJJnGR8S1sORXeD"

def get_available_models() -> Dict[str, Any]:
    """Obtener la lista de modelos disponibles en Straico.
    
    Returns:
        Dict con la lista de modelos y su información (nombre, modelo, pricing, max_output)
    """
    models_url = "https://api.straico.com/v0/models"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    try:
        resp = requests.get(models_url, headers=headers, timeout=30)
    except requests.exceptions.RequestException as exc:
        return {"error": str(exc)}
    
    # Parse JSON
    try:
        data = resp.json()
    except Exception:
        return {"error": "No se pudo parsear la respuesta JSON"}
    
    if 200 <= resp.status_code < 300:
        return data
    
    return {"error": f"status={resp.status_code}", "response": data}


def filter_text_only_models(models_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Filtra los modelos que solo soportan texto (no imágenes).
    
    Args:
        models_data: Respuesta de la API con la lista de modelos
        
    Returns:
        Lista de modelos que solo soportan texto
    """
    if "error" in models_data:
        return []
    
    models_list = models_data.get('data', [])
    text_only_models = []
    
    for model in models_list:
        # Filtrar modelos que no tienen soporte de imágenes
        # Esto puede variar según la estructura de la respuesta de la API
        # Asumimos que los modelos con imagen tienen un campo 'vision' o similar
        
        # Criterios de filtrado (ajustar según la estructura real de la API):
        # 1. No tienen 'vision' en el nombre
        # 2. No tienen 'image' en el nombre
        # 3. No tienen flags de vision/multimodal
        
        name = model.get('name', '').lower()
        model_id = model.get('model', '').lower()
        
        # Excluir modelos con términos relacionados a imágenes/visión
        vision_keywords = ['vision', 'image', 'visual', 'multimodal', 'gpt-4o', 'gpt-4-turbo', 
                          'claude-3', 'gemini-pro-vision', 'gemini-flash', 'gemini-exp']
        
        is_text_only = not any(keyword in name or keyword in model_id for keyword in vision_keywords)
        
        if is_text_only:
            text_only_models.append(model)
    
    return text_only_models


def print_text_models(save_to_file: bool = True):
    """Imprime y opcionalmente guarda la lista de modelos solo texto.
    
    Args:
        save_to_file: Si es True, guarda la lista en un archivo JSON
    """
    print("Obteniendo modelos disponibles...")
    models_data = get_available_models()
    
    if "error" in models_data:
        print(f"Error: {models_data['error']}")
        return
    
    text_models = filter_text_only_models(models_data)
    
    print(f"\n{'='*80}")
    print(f"Total de modelos disponibles: {len(models_data.get('data', []))}")
    print(f"Modelos solo texto: {len(text_models)}")
    print(f"{'='*80}\n")
    
    print("Lista de modelos solo texto:")
    print("-" * 80)
    
    model_ids = []
    for model in text_models:
        name = model.get('name', 'N/A')
        model_id = model.get('model', 'N/A')
        pricing = model.get('pricing', {})
        coins = pricing.get('coins', 'N/A')
        words = pricing.get('words', 'N/A')
        max_output = model.get('max_output', 'N/A')
        
        print(f"Nombre: {name}")
        print(f"  ID: {model_id}")
        print(f"  Precio: {coins} coins por {words} palabras")
        print(f"  Max Output: {max_output} tokens")
        print()
        
        model_ids.append(model_id)
    
    if save_to_file:
        output = {
            "total_models": len(models_data.get('data', [])),
            "text_only_count": len(text_models),
            "text_models": text_models,
            "model_ids": model_ids
        }
        
        output_file = "Straico/text_only_models.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"\n{'='*80}")
        print(f"Lista guardada en: {output_file}")
        print(f"IDs de modelos disponibles: {len(model_ids)}")
        print(f"{'='*80}")
        
        # También guardar solo la lista de IDs para fácil copia
        ids_file = "Straico/text_model_ids.txt"
        with open(ids_file, 'w', encoding='utf-8') as f:
            for mid in model_ids:
                f.write(f"{mid}\n")
        
        print(f"Lista de IDs guardada en: {ids_file}")


if __name__ == "__main__":
    print_text_models(save_to_file=True)
