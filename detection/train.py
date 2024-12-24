import os
from typing import List

from click.core import batch

from detection.utils import aug_data
from sklearn.model_selection import train_test_split
import shutil
from ultralytics import YOLO


def augment(dataset_dir: str):
    try:
        # Список всех классов
        class_names = [folder
                       for folder in os.listdir(dataset_dir)
                       if os.path.isdir(os.path.join(dataset_dir, folder))]

        # Перебор всех папок (классов) в исходной директории
        for class_name in class_names:
            class_path = os.path.join(dataset_dir, class_name)
            aug_data.augmentation(class_path)

        return True

    except Exception as e:
        raise ValueError(f"Ошибка при обучении модели: {str(e)}")


def train_yolo(p_name: str, f_path: str, epochs_count: int = 50, batch_count: int = 16):
    """
    Обучение YOLO модели.

    Args:
        p_name (str): Путь к основному каталогу.
        f_path (str): Путь к датасету.
        epochs_count (int): Количество эпох обучения.
        batch_count (int): Количество batch обучения.
        do_aug (bool): Делаем аугментацию.
    """
    try:
        project_dir = os.path.join(os.getenv("FILE_DIRECTORY"), p_name)

        class_names = prepare(f_path, project_dir)
        yaml_name = create_yaml(project_dir, class_names)
        return create_model(yaml_name, epochs_count, batch_count, project_dir)

    except Exception as e:
        raise ValueError(f"Ошибка при обучении модели: {str(e)}")


# === ШАГ 1: ПОДГОТОВКА ДАННЫХ ===
def prepare(dataset_dir: str, project_dir: str):
    # Список всех классов
    class_names = [folder
                   for folder in os.listdir(dataset_dir)
                   if os.path.isdir(os.path.join(dataset_dir, folder))]

    # Перебор всех папок (классов) в исходной директории
    for class_name in class_names:
        class_path = os.path.join(dataset_dir, class_name)

        # Создаем директории train и val для текущего класса
        train_dir = os.path.join(project_dir, "train", class_name)
        val_dir = os.path.join(project_dir, "val", class_name)
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
def create_yaml(project_dir: str, class_names: List[str]):
    yaml_content = f"""
    path: {project_dir}
    train: ../train
    val: ../val
    
    names:
      0: {class_names[0]}
      1: {class_names[1]}
      2: {class_names[2]} 
      3: {class_names[3]}
      4: {class_names[4]}  

    """
    
    yaml_file = os.path.join(project_dir, 'data.yaml')
    with open(yaml_file, 'w') as f:
        f.write(yaml_content)

    return str(yaml_file)


# === ШАГ 3: ОБУЧЕНИЕ МОДЕЛИ YOLOv11 ДЛЯ ЗАДАЧИ КЛАССИФИКАЦИИ ===
def create_model(yaml_file: str, epochs_count: int, batch_count: int, model_path: str, yolo_model: str="yolov8s.pt"):
    # Загрузка модели YOLOv11 для классификации
    model = YOLO(yolo_model)
    
    # Обучение модели классификации
    model.train(
        data    = yaml_file,        # Путь к yaml файлу
        epochs  = epochs_count,     # Количество эпох
        batch   = batch_count       # Размер батча
        #imgsz=640
        # Размер изображений
    )

    # Валидация модели
    #model.val()  results =
    model.save(model_path)
    return model


# === ШАГ 4: ТЕСТИРОВАНИЕ МОДЕЛИ НА ИЗОБРАЖЕНИЯХ ===
def predict(destination_dir: str, model_path: str):
    # Предсказание на одном изображении
    model = YOLO(model_path)
    result = model.predict(source=destination_dir)
    return result[0].boxes.data
    #return result