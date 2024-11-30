from fastapi import FastAPI
from infer.infer import run_inference
app = FastAPI()

@app.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...), train_ratio: float = 0.8):
    """
    Загрузка архива, аугментация изображений и разделение на train/validate.

    Args:
        file (UploadFile): Архив с размеченными изображениями.
        train_ratio (float): Доля данных для обучения (остальное для валидации).

    Returns:
        dict: Информация о результатах обработки.
    """
    # 1. Сохранение и распаковка архива
    archive_path = "temp_dataset.zip"
    dataset_dir = "processed_dataset"
    with open(archive_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        zip_ref.extractall(dataset_dir)

    # Удаляем архив, чтобы не засорять
    os.remove(archive_path)

    # 2. Аугментация изображений
    images_dir = Path(dataset_dir) / "images"
    labels_dir = Path(dataset_dir) / "labels"
    augmented_dir = Path(dataset_dir) / "augmented"
    augmented_dir.mkdir(parents=True, exist_ok=True)

    augmentation = A.Compose([
        A.HorizontalFlip(p=0.5),
        A.RandomBrightnessContrast(p=0.2),
        A.Rotate(limit=15, p=0.3),
    ])

    for img_file in images_dir.glob("*.jpg"):
        # Читаем изображение
        image = cv2.imread(str(img_file))
        label_file = labels_dir / f"{img_file.stem}.txt"

        # Аугментируем и сохраняем
        for i in range(5):  # Количество аугментаций
            augmented = augmentation(image=image)
            aug_image = augmented["image"]
            aug_filename = f"{img_file.stem}_aug{i}.jpg"
            cv2.imwrite(str(augmented_dir / aug_filename), aug_image)

            # Копируем метку
            shutil.copy(label_file, augmented_dir / f"{img_file.stem}_aug{i}.txt")

    # 3. Разделение данных
    augmented_images = sorted(augmented_dir.glob("*.jpg"))
    train_files, validate_files = train_test_split(augmented_images, train_size=train_ratio)

    for split, split_name in [(train_files, "train"), (validate_files, "validate")]:
        split_dir = Path(dataset_dir) / split_name
        images_split_dir = split_dir / "images"
        labels_split_dir = split_dir / "labels"
        images_split_dir.mkdir(parents=True, exist_ok=True)
        labels_split_dir.mkdir(parents=True, exist_ok=True)

        for img in split:
            shutil.move(str(img), str(images_split_dir / img.name))
            shutil.move(str(augmented_dir / img.stem.replace("_aug", "") + ".txt"),
                        str(labels_split_dir / img.stem.replace("_aug", "") + ".txt"))

    # Удаляем временную папку
    shutil.rmtree(augmented_dir)

    return {"message": "Dataset processed and split into train/validate", "train_ratio": train_ratio}

@app.post("/infer")
async def infer(file: UploadFile = File(...)):
    """
    Выполнить инференс изображения.

    Args:
        file (UploadFile): Загруженное изображение.

    Returns:
        dict: Результаты предсказания.
    """
    with open("temp.jpg", "wb") as buffer:
        buffer.write(file.file.read())

    results = run_inference("temp.jpg", "yolo/model/best.pt")
    return {"results": results.tolist()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
