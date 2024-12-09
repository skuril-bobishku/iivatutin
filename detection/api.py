from fastapi import FastAPI
from infer import train

app = FastAPI()

@app.post("/train")
async def train(path: str):
    """
    Выполнить инференс изображения.

    Args:
        path (str): Загруженное изображение.

    Returns:
        dict: Результаты предсказания.
    """
    results = train(path, "yolo/model/best.pt")
    return {"results": results.tolist()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8100)
