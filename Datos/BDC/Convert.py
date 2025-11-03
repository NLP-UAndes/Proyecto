from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
import os
import json
from pathlib import Path


def save_text_to_file(text, pdf_filename, output_dir="output"):
    """Guarda el texto extraído a un archivo .txt"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Crear nombre del archivo de salida basado en el PDF
    base_name = Path(pdf_filename).stem
    output_file = os.path.join(output_dir, f"{base_name}_text.txt")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"Texto guardado en: {output_file}")
    return output_file



def save_metadata(metadata, pdf_filename, output_dir="output"):
    """Guarda los metadatos en un archivo JSON"""
    os.makedirs(output_dir, exist_ok=True)
    
    base_name = Path(pdf_filename).stem
    metadata_file = os.path.join(output_dir, f"{base_name}_metadata.json")
    
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"Metadatos guardados en: {metadata_file}")
    return metadata_file

def main():
    # Lista de PDFs a procesar
    pdf_files = [
        "Diccionario_breve_de_Colombiaismos_slown.pdf",
    ]
    
    converter = PdfConverter(artifact_dict=create_model_dict())
    
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            print(f"\nProcesando: {pdf_file}")
            
            try:
                # Convertir PDF
                rendered = converter(pdf_file)
                text, metadata, _ = text_from_rendered(rendered)
                
                # Guardar resultados (sin imágenes)
                save_text_to_file(text, pdf_file)
                save_metadata(metadata, pdf_file)
                
                print(f"✓ Completado: {pdf_file}")
                
            except Exception as e:
                print(f"✗ Error procesando {pdf_file}: {str(e)}")
        else:
            print(f"⚠ Archivo no encontrado: {pdf_file}")

if __name__ == "__main__":
    main()
