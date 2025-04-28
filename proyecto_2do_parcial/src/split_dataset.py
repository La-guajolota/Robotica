"""
Divide las imágenes de cada categoría respetando la proporción 70%-15%-15% (puedes ajustar estos valores)
Copia las imágenes a las carpetas correspondientes dentro de processed/
Muestra un resumen de cuántas imágenes se han colocado en cada conjunto
"""
import os
import random
import shutil
from pathlib import Path

def split_dataset(raw_smoking_dir, raw_not_smoking_dir, processed_dir, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
    """
    Divide las imágenes en conjuntos de entrenamiento, validación y prueba
    """
    # Verificar que las proporciones sumen 1
    assert train_ratio + val_ratio + test_ratio == 1.0, "Las proporciones deben sumar 1"
    
    # Crear directorios si no existen
    train_smoking_dir = os.path.join(processed_dir, "train", "smoking")
    train_not_smoking_dir = os.path.join(processed_dir, "train", "not_smoking")
    val_smoking_dir = os.path.join(processed_dir, "validation", "smoking")
    val_not_smoking_dir = os.path.join(processed_dir, "validation", "not_smoking")
    test_smoking_dir = os.path.join(processed_dir, "test", "smoking")
    test_not_smoking_dir = os.path.join(processed_dir, "test", "not_smoking")
    
    for directory in [train_smoking_dir, train_not_smoking_dir, 
                      val_smoking_dir, val_not_smoking_dir, 
                      test_smoking_dir, test_not_smoking_dir]:
        os.makedirs(directory, exist_ok=True)
    
    # Procesar imágenes de fumadores
    process_category(raw_smoking_dir, train_smoking_dir, val_smoking_dir, test_smoking_dir, 
                     train_ratio, val_ratio, test_ratio)
    
    # Procesar imágenes de no fumadores
    process_category(raw_not_smoking_dir, train_not_smoking_dir, val_not_smoking_dir, test_not_smoking_dir,
                     train_ratio, val_ratio, test_ratio)

def process_category(source_dir, train_dir, val_dir, test_dir, train_ratio, val_ratio, test_ratio):
    """
    Procesa una categoría (smoking o not_smoking) y divide sus imágenes
    """
    # Listar todas las imágenes en el directorio
    all_images = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f)) and 
                 f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    # Mezclar aleatoriamente
    random.shuffle(all_images)
    
    # Calcular los índices de división
    train_end = int(len(all_images) * train_ratio)
    val_end = train_end + int(len(all_images) * val_ratio)
    
    # Dividir la lista
    train_images = all_images[:train_end]
    val_images = all_images[train_end:val_end]
    test_images = all_images[val_end:]
    
    # Copiar imágenes a sus respectivos directorios
    for img in train_images:
        shutil.copy2(os.path.join(source_dir, img), os.path.join(train_dir, img))
    
    for img in val_images:
        shutil.copy2(os.path.join(source_dir, img), os.path.join(val_dir, img))
    
    for img in test_images:
        shutil.copy2(os.path.join(source_dir, img), os.path.join(test_dir, img))
    
    # Imprimir resumen
    print(f"Categoría procesada desde {source_dir}:")
    print(f"  - Total imágenes: {len(all_images)}")
    print(f"  - Imágenes de entrenamiento: {len(train_images)}")
    print(f"  - Imágenes de validación: {len(val_images)}")
    print(f"  - Imágenes de prueba: {len(test_images)}")

if __name__ == "__main__":
    # Configurar rutas (ajusta según tu estructura)
    RAW_SMOKING_DIR = "data/raw/smoking"
    RAW_NOT_SMOKING_DIR = "data/raw/not_smoking"
    PROCESSED_DIR = "data/processed"
    
    # Ejecutar la división del conjunto de datos
    split_dataset(RAW_SMOKING_DIR, RAW_NOT_SMOKING_DIR, PROCESSED_DIR)
    print("¡División del conjunto de datos completada!")