from ultralytics import YOLO

def train_model(data_yaml: str, model_path: str, epochs: int = 50):
    """
    Обучение YOLO модели.

    Args:
        data_yaml (str): Путь к файлу конфигурации данных (YAML).
        model_path (str): Путь для сохранения модели.
        epochs (int): Количество эпох обучения.
    """
    model = YOLO("yolov8n.pt")  # Загружаем предобученную модель
    model.train(data=data_yaml, epochs=epochs, imgsz=640)
    model.save(model_path)
    print(f"Модель сохранена в {model_path}")

if __name__ == "__main__":
    train_model("dataset.yaml", "yolo/model/best.pt")