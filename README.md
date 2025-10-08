# ¿Qué tan bien entienden los LLM los Modismos Colombianos?
Repositorio del proyecto académico para construir y evaluar un corpus de modismos colombianos (DICOL + BDC) y medir el desempeño de LLM en tareas de definición, detección de uso figurado y sustitución por sinónimos.

## Integrantes:

- Santiago Bobadilla - s.bobadilla@uniandes.edu.co
- Juan Diego Osorio - jd.osorioc1@uniandes.edu.co
- María Alejandra Pinzón - ma.pinzonr1@uniandes.edu.co
- Ignacio Chaparro - i.chaparro@uniandes.edu.co

### Estructura del proyecto:

```
Proyecto/
├─ BDC/
│  ├─ Convert.py                        # Convierte PDF a texto y metadata usando Marker
│  ├─ creacionDatasetBDC.ipynb          # Limpieza y normalización del BDC → datasetBDC.csv
│  ├─ datasetBDC.csv                     # Dataset preprocesado de BDC
│  ├─ Diccionario_breve_de_Colombiaisms_slown_text.txt # Texto extraído del PDF
│  ├─ Diccionario_breve_de_Colombiaismos_slown.pdf     # Fuente original
│  └─ read.txt                           # URL de la fuente oficial BDC
│
├─ DICOL/
│  ├─ diccionario_colombianismos_completo.json        # Export de DICOL 
│  ├─ diccionario_colombianismos.txt                  # Versión en texto plano
│  ├─ DictionaryRepository.js                         # Métodos para consumir la API LEXICC
│  ├─ package.json                                    # COnfiguración para node
│  ├─ read.txt                                        # URL a LEXICC - Fuente original
│  └─ Test.js                                         # Uso de DictionaryRepository y estructuración de archivo final
│
├─ Papers/                                            # Revisión de literatura
│  ├─ El Sesgo Lingüístico Digital (SLD)en la inteligencia artificial- ... en español.pdf
│  ├─ Es_igual_pero_no_es_lo_mismo.pdf
│  ├─ Investigating Idiomaticity in Word Representations.pdf
│  ├─ It’s not Rocket Science – Interpreting Figurative Language in Narratives.pdf
│  ├─ Sign of the Times – Evaluating the use of LLM for Idiomaticity Detection.pdf
│  ├─ The widespread adoption of large language model-assisted writing across society.pdf
│  └─ What_idioms_teach_us_about_Al_.pdf
│
├─ AnalisisDatos.ipynb                   # Graficación y análisis descriptivo del corpus
├─ creacionDataset.ipynb                  # Une DICOL + BDC y genera el corpus final
├─ modismos_Dataset_Final.csv             # Conjunto de datos final
└─ README.md
```