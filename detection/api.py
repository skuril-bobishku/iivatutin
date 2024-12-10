from fastapi import FastAPI
from detection.train import train, predict

app = FastAPI()

model=None

@app.post("/train")
async def train(path: str):
    """
    Выполнить обучение модели.

    Args:
        path (str): Загруженное изображение.

    Returns:
        dict: Результаты предсказания.
    """
    results = train(path, 80)
    return {"results": results.tolist()}


@app.post("/test")
async def test(path_photo: str, path_model: str):
    """
    Выполнить классификацию изображения.

    Args:
        path_photo (str): Загруженное изображение.
        path_model (str): Загруженная модели.

    Returns:
        dict: Результаты предсказания.
    """
    results = predict(path_photo, path_model)
    return {"results": results.tolist()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8101)
