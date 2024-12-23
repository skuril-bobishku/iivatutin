from click.core import batch
from fastapi import FastAPI
from pydantic import BaseModel
from detection.train import train, predict

app = FastAPI()

model=None

class TrainRequest(BaseModel):
    pName: str
    #mName: str
    fPath: str
    epochs: int
    batch: int
    augmentation: bool

@app.post("/train")
async def train(request: TrainRequest):
    """
    Выполнить обучение модели.

    Args:
        request (TrainRequest): Запрос обучения.

    Returns:
        dict: Результаты предсказания.
    """

    project_name = request.pName
    #model_name = request.mName
    file_path = request.fPath
    t_epochs = request.epochs
    t_batch = request.batch
    t_aug = request.augmentation

    #results = train(project_name, file_path, t_epochs, t_batch, t_aug)
    #return {"results": results.tolist()}


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
