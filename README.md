# Proyecto

- Santiago Bobadilla
- Juan Diego Osorio
- María Alejandra Pinzón
- Ignacio Chaparro

### Organización del Repositorio

```
Proyecto/
├─ AnalisisDatos.ipynb               # Notebook para el análisis exploratorio del dataset final.
├─ creacionDataset.ipynb             # Notebook para la creación y unificación de los datasets.
├─ DatasetCaroCuervo.ipynb           # Notebook para procesar los datos del Diccionario Caro y Cuervo.
├─ modismos_Dataset_Final.csv        # Dataset final consolidado con todas las fuentes.
├─ modismos_Dataset_Final_Kaggle.csv # Versión del dataset final preparada para Kaggle.
├─ README.md                         # Documentación principal del proyecto.
├─ BDC/                              # Recursos del "Diccionario breve de Colombianismos".
│  ├─ Convert.py                     # Script para convertir el PDF a texto.
│  ├─ Diccionario_breve_de_Colombiaismos_slown.pdf # Documento PDF original.
│  ├─ Diccionario_breve_de_Colombiaismos_slown_text.txt # Texto extraído del PDF.
│  └─ read.txt                       # Notas sobre la fuente de datos.
├─ DICOL/                            # Recursos del "Diccionario de Colombianismos" (DICOL).
│  ├─ diccionario_colombianismos.json # Datos extraídos de la API en formato JSON.
│  ├─ diccionario_colombianismos.txt  # Datos extraídos de la API en formato de texto.
│  ├─ DictionaryRepository.js        # Lógica para interactuar con la API del diccionario.
│  ├─ package.json                   # Dependencias del proyecto Node.js para el scraping.
│  ├─ read.txt                       # URL de la fuente de datos.
│  └─ Test.js                        # Script para ejecutar la extracción de datos de la API.
└─ Papers/                           # Documentos y artículos de investigación relacionados.
   └─ ...
```