from fastapi import FastAPI
from infer import train

app = FastAPI()


@app.post("/train")
async def train():
    """
    Выполнить инференс изображения.

    Args:
        file (UploadFile): Загруженное изображение.

    Returns:
        dict: Результаты предсказания.
    """
    results = train("temp.jpg", "yolo/model/best.pt")
    return {"results": results.tolist()}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8100)
