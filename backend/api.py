import os
import shutil
from sklearn.model_selection import train_test_split
from ultralytics import YOLO
import aug_data
from tqdm import tqdm






# === ШАГ 2: СОЗДАНИЕ ФАЙЛА КОНФИГУРАЦИИ YAML ===





# === ШАГ 3: ОБУЧЕНИЕ МОДЕЛИ YOLOv11 ДЛЯ ЗАДАЧИ КЛАССИФИКАЦИИ ===



# === ШАГ 4: ВАЛИДАЦИЯ МОДЕЛИ YOLOv11 ДЛЯ ЗАДАЧИ КЛАССИФИКАЦИИ ===

# Валидация модели
# results = model.val()



# === ШАГ 5: ТЕСТИРОВАНИЕ МОДЕЛИ НА ИЗОБРАЖЕНИЯХ ===

# Предсказание на одном изображении
image_path = os.path.join(destination_dir, 'test', 'example.jpg')  # Укажите путь к тестовому изображению
result = model.predict(source=image_path)

# Печать результата
print(result)



# === ШАГ 6: АНАЛИЗ РЕЗУЛЬТАТОВ ЧЕРЕЗ TENSORBOARD ===

print("Запустите TensorBoard для анализа результатов обучения:")
print("tensorboard --logdir yolov5/runs/train")
