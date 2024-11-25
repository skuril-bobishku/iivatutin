from fastapi import FastAPI, UploadFile, File
from infer.infer import run_inference
app = FastAPI()
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
