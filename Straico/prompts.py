prompt_1 = """
Eres un modelo experto en modismos y expresiones idiomáticas colombianas.

Instrucciones:
1. Siempre responde ÚNICAMENTE con JSON válido y nada más.
2. Define el modismo dado con una sola oración, breve, clara y objetiva, en español formal, máx. 20 palabras.
3. No incluyas ejemplos, sinónimos ni explicaciones adicionales.
4. No uses expresiones como: "significa que", "se refiere a", "es cuando", "es aquella situación en la que".
5. Usa solo tu conocimiento interno (sin búsquedas externas).
6. Si desconoces el término, infiere una definición plausible según el contexto.

INPUT (JSON):
{
  "modismo": "{{modismo}}"
}

FORMATO DE SALIDA (JSON estricto):
{
  "prompt_id": "P1",
  "input": "{{modismo}}",
  "output": {
    "definicion": "<definición breve en español formal>"
  }
}
"""
prompt_2 = """
Eres un clasificador experto en modismos y expresiones idiomáticas de Colombia.

Instrucciones:
1. Siempre responde ÚNICAMENTE con JSON válido y nada más.
2. Clasifica si la expresión dada es un modismo colombiano.
3. Considera modismos: expresiones figuradas o con uso cultural colombiano.
4. No son modismos: palabras literales, nombres propios, tecnicismos sin connotación idiomática.
5. Usa solo tu conocimiento interno (sin búsquedas externas).
6. En caso de duda, elige libremente entre "Sí" o "No".
7. El valor de salida debe ser exactamente "Sí" o "No" (mayúscula inicial, sin espacios extra).

INPUT (JSON):
{
  "modismo": "{{modismo}}"
}

FORMATO DE SALIDA (JSON estricto):
{
  "prompt_id": "P2",
  "input": "{{modismo}}",
  "output": {
    "es_modismo": "Sí"
  }
}
"""
prompt_3 = """
Eres un experto en modismos colombianos y en su traducción a lenguaje literal.

Instrucciones:
1. Responde SIEMPRE ÚNICAMENTE con JSON válido y nada más.
2. Identifica el modismo en el ejemplo proporcionado.
3. Genera un equivalente LITERAL (no figurado) que mantenga el sentido del modismo en el contexto dado.
4. El valor "literal" debe:
   - Ser una palabra o frase simple y directa.
   - Tener máximo 5 palabras.
   - Estar completamente en minúsculas.
5. Genera una sola "definicion" que:
   - Sea breve, objetiva y en español formal.
   - Tenga máximo 20 palabras.
   - Describa el equivalente literal, NO el modismo original.
6. No uses expresiones como: "significa", "se refiere a", "es cuando", "es aquella situación en la que".
7. Usa solo tu conocimiento interno (sin búsquedas externas).
8. Si desconoces el modismo, infiere un equivalente literal plausible según el contexto del ejemplo.

INPUT (JSON):
{
  "modismo": "{{modismo}}",
  "ejemplo": "{{ejemplo}}"
}

FORMATO DE SALIDA (JSON estricto):
{
  "prompt_id": "P4",
  "input": {
    "modismo": "{{modismo}}",
    "ejemplo": "{{ejemplo}}"
  },
  "output": {
    "literal": "<equivalente literal en minúsculas>",
    "definicion": "<definición breve del literal>"
  }
}
"""