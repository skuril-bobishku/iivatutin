from fastapi import FastAPI

app = FastAPI()
import os
import shutil
from sklearn.model_selection import train_test_split
from ultralytics import YOLO


# Функция проверки существования папки по указанному пути
def manage_directories(base_path: str, folders_list: list):
    # Обходим каждую папку в списке
    for folder in folders_list:
        folder_path = os.path.join(base_path, folder)

        if os.path.exists(folder_path):  # Если папка существует
            # Удаляем все содержимое папки
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # Удаляем файл или символическую ссылку
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Удаляем директорию
                except Exception as e:
                    print(f'Ошибка при удалении {file_path}: {e}')
        else:
            # Создаем папку, если её нет
            os.makedirs(folder_path)
            print(f'Папка {folder} создана.')

# Функция копирования файлов в соответствующие папки
def copy_files(image_list, split):
    for img in image_list:
        shutil.copy(os.path.join(dataset_path, img), os.path.join(output_path, split, img))

# === ШАГ 1: ПОДГОТОВКА ДАННЫХ ===

# Указание путей к исходным данным и выходной директории
dataset_path = '/path/to/images'  # Папка, содержащая изображения разных классов
output_path = '/path/to/output'  # Папка, куда будет сохранена структура train/val/test


# Создание структуры папок для train, val и test
manage_directories(output_path, ['train', 'val', 'test'])


# Получение списка изображений (форматы файлов .jpg, .jpeg, .png)
images = [f for f in os.listdir(dataset_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

# Разделение данные на train, val и test в соотношении 7:2:1
train_images, val_test_images = train_test_split(images, test_size=0.3, random_state=42)
val_images, test_images = train_test_split(val_test_images, test_size=0.33, random_state=42)

    #Распредление изображений по папкам
copy_files(train_images, 'train')
copy_files(val_images, 'val')
copy_files(test_images, 'test')

# === ШАГ 2: СОЗДАНИЕ ФАЙЛА КОНФИГУРАЦИИ YAML ===

#Указание названий классов
class1 = ""
class2 = ""
class3 = ""
class4 = ""
class5 = ""

yaml_content = f"""
path: {output_path}
train: {output_path}/train
val: {output_path}/val
test: {output_path}/test

names:
  0: {class1}
  1: {class2}
  2: {class3} 
  3: {class4}
  4: {class5}  

"""

yaml_file = os.path.join(output_path, 'data.yaml')
with open(yaml_file, 'w') as f:
    f.write(yaml_content)

# === ШАГ 3: ОБУЧЕНИЕ МОДЕЛИ YOLOv11 ДЛЯ ЗАДАЧИ КЛАССИФИКАЦИИ ===

# Загрузка модели YOLOv11 для классификации

yolo_model = 'yolov11n.pt'
model = YOLO(yolo_model)

# Обучение модели классификации
model.train(
    data    = yaml_file,        # Путь к yaml файлу
    epochs  = 50,               # Количество эпох
    imgsz   = 640,              # Размер изображения
    batch   = 16,               # Размер батча
    lr0     = 0.01,             # Начальная скорость обучения
    workers = 4                 # Количество потоков для загрузки данных
)

# === ШАГ 4: ВАЛИДАЦИЯ МОДЕЛИ YOLOv11 ДЛЯ ЗАДАЧИ КЛАССИФИКАЦИИ ===

# Валидация модели
results = model.val()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8100)
# Печать результатов
print(f"Accuracy: {results.metrics['accuracy']:.2f}")
print(f"Loss: {results.metrics['loss']:.2f}")


# === ШАГ 5: ТЕСТИРОВАНИЕ МОДЕЛИ НА ИЗОБРАЖЕНИЯХ ===

# Предсказание на одном изображении
image_path = os.path.join(output_path, 'test', 'example.jpg')  # Укажите путь к тестовому изображению
result = model.predict(source=image_path)

# Печать результата
print(result)



# === ШАГ 6: АНАЛИЗ РЕЗУЛЬТАТОВ ЧЕРЕЗ TENSORBOARD ===

print("Запустите TensorBoard для анализа результатов обучения:")
print("tensorboard --logdir yolov5/runs/train")
