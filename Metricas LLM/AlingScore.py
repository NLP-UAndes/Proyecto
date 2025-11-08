# Suprimir warnings molestos
import warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

# Suprimir logs de transformers y pytorch_lightning
import logging
logging.getLogger('pytorch_lightning').setLevel(logging.ERROR)
logging.getLogger('transformers').setLevel(logging.ERROR)

# Recargar todos los módulos de AlignScore
import sys
import os

# Obtener el directorio actual del notebook
notebook_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()

# Agregar el path al código fuente de AlignScore (path relativo)
alignscore_src_path = os.path.join(notebook_dir, 'AlignScore', 'src')
sys.path.insert(0, alignscore_src_path)

# Importar AlignScore
from alignscore import AlignScore

# Descargar el modelo AlignScore-base
# Primero necesitamos descargar el checkpoint del modelo
import os
import urllib.request

# Crear directorio para el checkpoint si no existe (path relativo)
notebook_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
checkpoint_dir = os.path.join(notebook_dir, 'AlignScore', 'checkpoints')
os.makedirs(checkpoint_dir, exist_ok=True)
checkpoint_path = os.path.join(checkpoint_dir, 'AlignScore-base.ckpt')

# Descargar el checkpoint si no existe
if not os.path.exists(checkpoint_path):
    url = "https://huggingface.co/yzha/AlignScore/resolve/main/AlignScore-base.ckpt" # AlignScore-large.ckpt"  # Para el modelo grande
    urllib.request.urlretrieve(url, checkpoint_path)
    print("Checkpoint descargado en:", checkpoint_path)
else:
    print("Checkpoint ya existe en:", checkpoint_path)


# Detectar el dispositivo disponible (GPU, MPS para Mac, o CPU)
import torch

def get_device():
    """
    Detecta y retorna el mejor dispositivo disponible.
    - cuda: Para GPUs NVIDIA
    - mps: Para GPUs Apple Silicon (M1, M2, M3, etc.)
    - cpu: Fallback si no hay GPU disponible
    """
    if torch.cuda.is_available():
        device = 'cuda'
        print(f"✓ GPU NVIDIA detectada: {torch.cuda.get_device_name(0)}")
    elif torch.backends.mps.is_available():
        device = 'mps'
        print("✓ GPU Apple Silicon (MPS) detectada")
    else:
        device = 'cpu'
        print("⚠ No se detectó GPU, usando CPU")
    
    return device

device = get_device()


# Inicializar el scorer de AlignScore

scorer = AlignScore(
    model='roberta-base',
    batch_size=32,
    device=device,
    ckpt_path=checkpoint_path,
    evaluation_mode='nli_sp'
)