prompt_1 = """
Actúa como un modelo de lenguaje especializado en definiciones breves y precisas. Define la siguiente palabra o expresión en el contexto colombiano, sin incluir ejemplos ni explicaciones adicionales. Usa solo tu conocimiento previo, ya que no tienes acceso a internet. Si no conoces la palabra, proporciona una definición aleatoria. Responde únicamente en formato JSON con la siguiente estructura: { "prompt_id": "P1", "input": "<palabra o expresión>", "output": { "definicion": "<definición breve>" }
} Ejemplo de salida:
{ "prompt_id": "P1", "input": "tirar la toalla", "output": { "definicion": "Rendirse o dejar de intentar algo difícil." }
} Palabra o expresión a definir: {{input}}"""
prompt_2 = """
Actúa como un modelo de lenguaje especializado en modismos colombianos. Tu tarea es determinar si la palabra o expresión proporcionada es un modismo colombiano. Responde únicamente con "Sí" o "No". No incluyas explicaciones ni texto adicional. Usa solo tu conocimiento previo, ya que no tienes acceso a internet. Responde en el siguiente formato JSON: { "prompt_id": "P2", "input": "<palabra o expresión>", "output": { "es_modismo": "Sí" o "No" }
} Ejemplo de salida:
{ "prompt_id": "P2", "input": "tirar la toalla", "output": { "es_modismo": "Sí" }
} Palabra o expresión a evaluar: {{input}}
"""
prompt_3 = """
Actúa como un modelo de lenguaje especializado en el español colombiano. Define y clasifica la palabra o expresión proporcionada, sin incluir ejemplos ni texto adicional. Usa solo tu conocimiento previo, ya que no tienes acceso a internet. Si no conoces la palabra, proporciona una definición aleatoria. Responde únicamente en formato JSON con la siguiente estructura: { "prompt_id": "P3", "input": "<palabra o expresión>", "output": { "definicion": "<definición breve>", "es_modismo": "Sí" o "No" }
} Ejemplo de salida:
{ "prompt_id": "P3", "input": "romper el hielo", "output": { "definicion": "Iniciar una conversación para disminuir la tensión.", "es_modismo": "Sí" }
} Palabra o expresión a analizar: {{input}}
"""
prompt_4 = """
Actúa como un modelo de lenguaje especializado en modismos colombianos. Tu tarea es reemplazar el modismo {{input}} por una palabra o frase literal que mantenga el mismo significado. No incluyas explicaciones ni texto adicional. Usa solo tu conocimiento previo y, si no conoces la expresión, inventa un reemplazo posible. Responde solo en formato JSON con esta estructura: { "prompt_id": "P4", "input": "{{input}}", "output": { "reemplazo": "<palabra o frase literal>" } }
"""
