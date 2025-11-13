"""
Sentence-BERT: Similitud semántica con embeddings multilingües
Modelo: paraphrase-multilingual-mpnet-base-v2
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List
import warnings
warnings.filterwarnings('ignore')

# Cargar modelo pre-entrenado multilingüe
model_sbert = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

def compute_sbert_similarity(candidatos: List[str], referencias: List[str]) -> np.ndarray:
    """
    Calcula similitud de coseno entre candidatos y referencias usando Sentence-BERT.
    
    El modelo paraphrase-multilingual-mpnet-base-v2 genera embeddings semánticos
    que capturan el significado del texto, permitiendo comparar frases con 
    palabras diferentes pero significado similar.
    
    Args:
        candidatos: Lista de textos generados por el modelo
        referencias: Lista de textos de referencia (ground truth)
        
    Returns:
        Array con scores de similitud de coseno (rango: -1 a 1, típicamente 0 a 1)
        Valores cercanos a 1 indican alta similitud semántica
    """
    # Generar embeddings para candidatos y referencias
    embeddings_candidatos = model_sbert.encode(candidatos, convert_to_tensor=False)
    embeddings_referencias = model_sbert.encode(referencias, convert_to_tensor=False)
    
    # Calcular similitud de coseno para cada par
    similarities = []
    for emb_cand, emb_ref in zip(embeddings_candidatos, embeddings_referencias):
        # Reshape para sklearn
        emb_cand = emb_cand.reshape(1, -1)
        emb_ref = emb_ref.reshape(1, -1)
        
        # Calcular similitud de coseno
        sim = cosine_similarity(emb_cand, emb_ref)[0][0]
        similarities.append(sim)
    
    return np.array(similarities)


def print_sbert_stats(similarities: np.ndarray, model_name: str = ""):
    """
    Imprime estadísticas de similitud de Sentence-BERT.
    
    Args:
        similarities: Array con scores de similitud
        model_name: Nombre del modelo evaluado (opcional)
    """
    mean_sim = np.mean(similarities)
    std_sim = np.std(similarities)
    min_sim = np.min(similarities)
    max_sim = np.max(similarities)
    
    print(f"\n{'='*60}")
    print(f"Estadísticas Sentence-BERT{' - ' + model_name if model_name else ''}")
    print(f"{'='*60}")
    print(f"Media:        {mean_sim:.4f}")
    print(f"Desv. Est.:   {std_sim:.4f}")
    print(f"Mínimo:       {min_sim:.4f}")
    print(f"Máximo:       {max_sim:.4f}")
    print(f"{'='*60}\n")
