"""
Este script organiza imágenes descargadas de una base de datos en carpetas específicas según su categoría.

La base de datos descargada contenía imágenes en diferentes carpetas y en desorden. Este script automatiza el proceso de clasificación, moviendo las imágenes a carpetas separadas: una para imágenes de fumadores ("smoking") y otra para imágenes de no fumadores ("not_smoking"). Las imágenes que no coinciden con los patrones esperados se ignoran.

El script utiliza los nombres de los archivos para determinar su categoría:
- Los archivos que comienzan con "smoking_" se copian a la carpeta de fumadores.
- Los archivos que comienzan con "notsmoking_" se copian a la carpeta de no fumadores.
"""
import os
import shutil
from pathlib import Path

def organize_smoking_images(source_folder, smoking_folder, not_smoking_folder):
    # Crear carpetas de destino si no existen
    os.makedirs(smoking_folder, exist_ok=True)
    os.makedirs(not_smoking_folder, exist_ok=True)
    
    # Contador para seguimiento
    smoking_count = 0
    not_smoking_count = 0
    other_files = 0
    
    # Recorrer todos los archivos en la carpeta fuente
    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)
        
        # Verificar que sea un archivo y no una carpeta
        if os.path.isfile(source_path):
            # Procesando archivos que comienzan con "smoking_"
            if filename.lower().startswith('smoking_'):
                shutil.copy2(source_path, os.path.join(smoking_folder, filename))
                smoking_count += 1
            
            # Procesando archivos que comienzan con "notsmoking_"
            elif filename.lower().startswith('notsmoking_'):
                shutil.copy2(source_path, os.path.join(not_smoking_folder, filename))
                not_smoking_count += 1
            
            # Archivos que no coinciden con ningún patrón
            else:
                other_files += 1
    
    print(f"Proceso completado. Resultados:")
    print(f"- Imágenes de fumadores encontradas y copiadas: {smoking_count}")
    print(f"- Imágenes de no fumadores encontradas y copiadas: {not_smoking_count}")
    print(f"- Archivos ignorados (no coinciden con los patrones): {other_files}")

# Ejemplo de uso
if __name__ == "__main__":
    # Configura estas rutas según tu estructura de carpetas
    SOURCE_FOLDER = "data/raw/Validation"                # Carpeta donde están todas las imágenes mezcladas
    SMOKING_FOLDER = "data/raw/smoking"  # Carpeta destino para imágenes de fumadores
    NOT_SMOKING_FOLDER = "data/raw/not_smoking"  # Carpeta destino para imágenes de no fumadores
    organize_smoking_images(SOURCE_FOLDER, SMOKING_FOLDER, NOT_SMOKING_FOLDER)