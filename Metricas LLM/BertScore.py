from transformers import AutoModel, logging
from bert_score import score

# Silenciar warnings de transformers
logging.set_verbosity_error()

# Cargar modelo en español
model_name_beto = "dccuchile/bert-base-spanish-wwm-uncased"
model_beto = AutoModel.from_pretrained(model_name_beto)

# Función para calcular BERTScore
#    P: Precisión - qué tan bien las palabras en la oración candidata son cubiertas por la referencia
#    R: Recall - qué tan bien las palabras en la oración de referencia son cubiertas por la candidata
#    F1: Media armónica de P y R
def compute_bertscore_beto(candidatos, referencias):
    P, R, F1 = score(candidatos, referencias, model_type=model_name_beto, num_layers=12, lang="es")
    return P, R, F1


# Cargar modelo en español
model_name_sci_beto = "Flaglab/SciBETO-large"
model_sci_beto = AutoModel.from_pretrained(model_name_sci_beto)

# Función para calcular BERTScore
#    P: Precisión - qué tan bien las palabras en la oración candidata son cubiertas por la referencia
#    R: Recall - qué tan bien las palabras en la oración de referencia son cubiertas por la candidata
#    F1: Media armónica de P y R
def compute_bertscore_sci_beto(candidatos, referencias):
    P, R, F1 = score(candidatos, referencias, model_type=model_name_sci_beto, num_layers=12, lang="es")
    return P, R, F1