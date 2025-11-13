prompt_1 = """
TAREA: Define el modismo colombiano proporcionado

ROL: Eres un modelo experto en modismos y expresiones idiomáticas colombianas.

REGLAS:
1. Proporciona ÚNICAMENTE una definición breve y precisa (máximo 20 palabras)
2. La definición debe ser clara, objetiva y en español formal
3. NO incluyas ejemplos, sinónimos, ni información adicional
4. NO uses términos como "significa que", "se refiere a" - ve directo a la definición
5. Usa solo tu conocimiento interno (sin búsquedas externas)
6. Si desconoces el término, infiere una definición plausible basada en el contexto

INPUT:
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

EJEMPLO:
Input: {"modismo": "tirar la toalla"}
Output:
{
	"prompt_id": "P1",
	"input": "tirar la toalla",
	"output": {
		"definicion": "Rendirse o abandonar un esfuerzo ante las dificultades."
	}
}
"""
prompt_2 = """
TAREA: Determina si la expresión proporcionada es un modismo colombiano

ROL: Eres un clasificador experto en modismos y expresiones idiomáticas de Colombia.

REGLAS:
1. Responde ÚNICAMENTE "Sí" o "No" (con mayúscula inicial)
2. NO incluyas explicaciones, justificaciones ni texto adicional
3. Considera modismos: expresiones con significado figurado o cultural colombiano
4. NO son modismos: palabras literales, nombres propios, tecnicismos sin connotación idiomática
5. Usa solo tu conocimiento interno (sin búsquedas externas)
6. En caso de duda, responde aleatoriamente "Sí" o "No".

INPUT:
{
	"modismo": "{{modismo}}"
}

FORMATO DE SALIDA (JSON estricto):
{
	"prompt_id": "P2",
	"input": "{{modismo}}",
	"output": {
		"es_modismo": "Sí" | "No"
	}
}

EJEMPLOS:
Input: {"modismo": "tirar la toalla"}
Output:
{
	"prompt_id": "P2",
	"input": "tirar la toalla",
	"output": {
		"es_modismo": "Sí"
	}
}

Input: {"modismo": "computadora"}
Output:
{
	"prompt_id": "P2",
	"input": "computadora",
	"output": {
		"es_modismo": "No"
	}
}
"""
prompt_3 = """
TAREA: Convierte el modismo en su equivalente literal y proporciona una definición breve.

ROL: Eres un experto en modismos colombianos y su traducción a lenguaje literal.

REGLAS:
1. Identifica el modismo en el ejemplo proporcionado
2. Proporciona un equivalente LITERAL (no figurado) que mantenga el significado en contexto
3. El literal debe ser una palabra o frase simple y directa (máximo 5 palabras)
4. La definición debe ser breve y objetiva (máximo 20 palabras)
5. La definición debe explicar el literal, NO el modismo original
6. Usa español formal y claro
7. NO uses términos como "significa", "se refiere a" - ve directo a la definición
8. Usa solo tu conocimiento interno (sin búsquedas externas)

INPUT:
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

EJEMPLOS:
Input: {"modismo": "tirar la toalla", "ejemplo": "Después de tantos intentos, decidió tirar la toalla."}
Output:
{
	"prompt_id": "P4",
	"input": {
		"modismo": "tirar la toalla",
		"ejemplo": "Después de tantos intentos, decidió tirar la toalla."
	},
	"output": {
		"literal": "rendirse",
		"definicion": "Abandonar un esfuerzo o actividad por dificultad o cansancio."
	}
}

Input: {"modismo": "romper el hielo", "ejemplo": "Juan contó un chiste para romper el hielo en la reunión."}
Output:
{
	"prompt_id": "P4",
	"input": {
		"modismo": "romper el hielo",
		"ejemplo": "Juan contó un chiste para romper el hielo en la reunión."
	},
	"output": {
		"literal": "iniciar conversación",
		"definicion": "Comenzar una interacción para reducir la tensión o incomodidad."
	}
}
"""
