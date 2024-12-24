from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from train import augment, train_yolo, predict

load_dotenv()

API_YOLO_URL=os.getenv("API_YOLO_URL", "localhost")
API_YOLO_PORT=int(os.getenv("API_YOLO_PORT", 8102))

VUE_URL=os.getenv("VUE_URL", "localhost")
VUE_PORT=int(os.getenv("VUE_PORT", 8101))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://{VUE_URL}:{VUE_PORT}"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model=None

class AugmentRequest(BaseModel):
    fPath: str

class TrainRequest(BaseModel):
    pName: str
    #mName: str
    fPath: str
    epochs: int
    batch: int


@app.post("/augment")
def augmentation(request: AugmentRequest):
    """
    Выполнить аугментацию датасета.

    Args:
        request (TrainRequest): Запрос на аугментацию.

    Returns:
        dict: Результат.
    """
    try:
        file_path = request.fPath

        if augment(file_path):
            return {"result": "Датасет проаугментирован"}
        else:
            return {"result": "Ошибка при аугментации датасета"}

    except Exception as e:
        print(f"Ошибка в обучении: {str(e)}")
        return {"error": f"Произошла ошибка: {str(e)}"}



@app.post("/train")
def train(request: TrainRequest):
    """
    Выполнить обучение модели.

    Args:
        request (TrainRequest): Запрос обучения.

    Returns:
        dict: Результаты предсказания.
    """
    try:
        project_name = request.pName
        #model_name = request.mName
        file_path = request.fPath
        t_epochs = request.epochs
        t_batch = request.batch

        results = train_yolo(project_name, file_path, t_epochs, t_batch)
        return {"results": results.tolist()}

    except Exception as e:
        print(f"Ошибка в обучении: {str(e)}")
        return {"error": f"Произошла ошибка: {str(e)}"}


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
    uvicorn.run(app, host="localhost", port=8102)
