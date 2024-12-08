import os
from typing import List

from ..utils import aug_data
from sklearn.model_selection import train_test_split
import shutil
from ultralytics import YOLO

def train(source_dir: str, data_yaml: str, model_path: str, epochs: int = 50):
    """
    Обучение YOLO модели.

    Args:
        source_dir (str): Путь к основному каталогу.
        data_yaml (str): Путь к файлу конфигурации данных (YAML).
        model_path (str): Путь для сохранения модели.
        epochs (int): Количество эпох обучения.
    """
    class_names = prepare(source_dir)
    yaml_name = create_yaml(source_dir, class_names)


# === ШАГ 1: ПОДГОТОВКА ДАННЫХ ===
def prepare(source_dir: str):
    # Список всех классов
    class_names = [folder
                   for folder in os.listdir(source_dir)
                   if os.path.isdir(os.path.join(source_dir, folder))]

    # Перебор всех папок (классов) в исходной директории
    for class_name in class_names:
        class_path = os.path.join(source_dir, class_name)
        # Аугментация данных
        aug_data.augmentation(class_path)

        # Создаем директории train и val для текущего класса
        train_dir = os.path.join(source_dir, "train", class_name)
        val_dir = os.path.join(source_dir, "val", class_name)
        os.makedirs(train_dir, exist_ok=True)
        os.makedirs(val_dir, exist_ok=True)

        # Получаем список всех изображений в папке класса
        images = [os.path.join(class_path, img) for img in os.listdir(class_path) if
                  img.endswith((".jpg", ".png", ".jpeg"))]

        # Разделяем изображения на train (80%) и val (20%)
        train_images, val_images = train_test_split(images, test_size=0.2, random_state=42)

        # Копируем изображения в соответствующие папки
        for img_path in train_images:
            shutil.copy(img_path, train_dir)

        for img_path in val_images:
            shutil.copy(img_path, val_dir)
            
        return class_names


# === ШАГ 2: СОЗДАНИЕ ФАЙЛА КОНФИГУРАЦИИ YAML ===
def create_yaml(source_dir: str, class_names: List[str]):
    yaml_content = f"""
    path: {source_dir}
    train: {source_dir}/train
    val: {source_dir}/val
    
    names:
      0: {class_names[0]}
      1: {class_names[1]}
      2: {class_names[2]} 
      3: {class_names[3]}
      4: {class_names[4]}  

    """
    
    yaml_file = os.path.join(source_dir, 'data.yaml')
    with open(yaml_file, 'w') as f:
        f.write(yaml_content)

    return str(yaml_file)


# === ШАГ 3: ОБУЧЕНИЕ МОДЕЛИ YOLOv11 ДЛЯ ЗАДАЧИ КЛАССИФИКАЦИИ ===
def load_model(yolo_model: str=None):
    # Загрузка модели YOLOv11 для классификации
    model = YOLO(yolo_model)
    
    # Обучение модели классификации
    model.train(
        data    = yaml_file,        # Путь к yaml файлу
        epochs  = 50                # Количество эпох
    )


if __name__ == "__main__":
    train("dataset.yaml", "yolo/model/best.pt")