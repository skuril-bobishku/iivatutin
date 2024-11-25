from ultralytics import YOLO

def run_inference(image_path: str, model_path: str):
    """
    Выполнить инференс изображения с использованием YOLO.

    Args:
        image_path (str): Путь к изображению.
        model_path (str): Путь к обученной модели.

    Returns:
        list: Результаты предсказания.
    """
    model = YOLO(model_path)
    results = model.predict(image_path)
    return results[0].boxes.data  # Координаты объектов, классы, вероятности

if __name__ == "__main__":
    results = run_inference("test.jpg", "yolo/model/best.pt")
    print(results)