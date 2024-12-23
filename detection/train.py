import os
from typing import List

from detection.utils import aug_data
from sklearn.model_selection import train_test_split
import shutil
from ultralytics import YOLO

def train(p_name: str, f_path: str, epochs: int = 50, batch: int = 16, do_aug: bool = False):
    """
    Обучение YOLO модели.

    Args:
        p_name (str): Путь к основному каталогу.
        f_path (str): Путь к датасету.
        epochs (int): Количество эпох обучения.
        batch (int): Количество batch обучения.
        do_aug (bool): Делаем аугментацию.
    """

    #class_names = prepare(p_name, f_path, do_aug)
    #yaml_name = create_yaml(source_dir, class_names)
    #return create_model(yaml_name, epochs, source_dir)


# === ШАГ 1: ПОДГОТОВКА ДАННЫХ ===
def prepare(source_dir: str, f_path: str, do_aug: bool):
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
def create_model(yaml_file: str, epochs: int, model_path: str, yolo_model: str=None):
    # Загрузка модели YOLOv11 для классификации
    model = YOLO(yolo_model)
    
    # Обучение модели классификации
    model.train(
        data    = yaml_file,        # Путь к yaml файлу
        epochs  =  epochs           # Количество эпох
    )

    # Валидация модели
    model.val() # results =
    model.save(model_path)
    return model


# === ШАГ 4: ТЕСТИРОВАНИЕ МОДЕЛИ НА ИЗОБРАЖЕНИЯХ ===
def predict(destination_dir: str, model_path: str):
    # Предсказание на одном изображении
    model = YOLO(model_path)
    result = model.predict(source=destination_dir)
    return result[0].boxes.data
    #return result