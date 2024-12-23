
import os
import shutil
from sklearn.model_selection import train_test_split
from ultralytics import YOLO
import aug_data
from tqdm import tqdm
import TkinterImageApp

app_instance = None

def set_app_instance(app):
    global app_instance
    app_instance = app

def log_info(text):
    if app_instance:
        app_instance.debug_log(text)

def classify(source_dir, path_to_model=None, epoch_num=2):

    # Путь к новой директории, где будут созданы train и val
    destination_dir = r"D:\pyii\dest"
    print(f"destination_dir = {destination_dir}")

    # Создание новой директории, если она не существует
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)  # Удаляем директорию
    os.makedirs(destination_dir, exist_ok=True)
    log_info(f"Создание новой директории по пути {destination_dir}.")

    # Список всех классов
    class_names = [folder for folder in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, folder))]

    # Перебор всех папок (классов) в исходной директории
    for class_name in class_names:
        class_path = os.path.join(source_dir, class_name)
        # Аугментация данных
        # aug_data.augmentation(class_path)

        # Создаем директории train и val для текущего класса
        train_dir = os.path.join(destination_dir, "train", class_name)
        val_dir = os.path.join(destination_dir, "val", class_name)
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

    log_info(f"Распределение файлов в классах по папкам train (80%) и val (20%).")
    # === ШАГ 2: СОЗДАНИЕ ФАЙЛА КОНФИГУРАЦИИ YAML ===

    yaml_content = f"""
    path: {destination_dir}
    train: {destination_dir}/train
    val: {destination_dir}/val
    
    names:
      0: {class_names[0]}
      1: {class_names[1]}
      2: {class_names[2]} 
      3: {class_names[3]}
      4: {class_names[4]}  
    
    """

    yaml_file = os.path.join(destination_dir, 'data.yaml')
    with open(yaml_file, 'w') as f:
        f.write(yaml_content)
    log_info(f"Создание и запись конфигурационного файла.")
    # === ШАГ 3: ОБУЧЕНИЕ МОДЕЛИ YOLOv11 ДЛЯ ЗАДАЧИ КЛАССИФИКАЦИИ ===
    log_info(f"Обучение модели...")
    # Загрузка модели YOLOv11 для классификации
    if (path_to_model != None):
        yolo_model = path_to_model
    else:
        yolo_model = r"D:\pyii\model\yolo11s-cls.pt"
    model = YOLO(yolo_model)

    # Обучение модели классификации
    model.train(
        data    = destination_dir,        # Путь к yaml файлу
        epochs  = epoch_num                # Количество эпох

    )
    # model.save()
    log_info(f"Обучение модели завершено.")
    return model

def predict(model, path_to_image):
    log_info(f"Обработка изображения...")
    predict_data = model.predict(source=path_to_image, task="classify")

    for predict in predict_data:
        probs = predict.probs  # Получаем объект Probs (это вероятности для всех классов)

        # Получение индекса и вероятности самого вероятного класса
        top_class_idx = probs.top5  # Индекс класса с наибольшей вероятностью
        top_class_prob = probs.top5conf  # Вероятность для этого класса
        # for i in top_class_idx:
        #     print(f"Класс: {model.names[i]}, Вероятность: {top_class_prob[i]:.2f}")
        description = "\n".join([f"Класс: {model.names[top_class_idx[i]]}, Вероятность: {top_class_prob[i]:.2f}"
                                          for i in range(len(top_class_idx))])
    # print(top_class_idx)
    # print(top_class_prob)

        # print(f"Класс: {model.names[top_class_idx]}, Вероятность: {top_class_prob:.2f}")
    # description= ""

        log_info(f"Изображение {os.path.basename(path_to_image).split('/')[-1]} успешно обработано. C вероятностью"
                    f" {probs.top1conf * 100}.2f% изображение принадлежит классу {model.names[probs.top1]}.")
    return description

def save_model(model, path_to_save):
    log_info(f"Сохранение модели...")
    model.save(path_to_save)
    log_info(f"Модель успешно сохранена по пути {path_to_save}.")
    return log_info



