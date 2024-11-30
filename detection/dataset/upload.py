import os
import zipfile
from fastapi import UploadFile, File

async def uploadZip(file: UploadFile, extractPath: str) -> dict:
    if not file.filename.endswith(".zip"):
        return {"error:" "Not .zip file loaded"}

    zipPath = os.path.join(extractPath, file.filename)
    os.makedirs(extractPath, exist_ok=True)

    with open(zipPath, "wb") as temp_file:
        temp_file.write(await file.read())

    extracted_files = []
    try:
        with zipfile.ZipFile(zipPath, 'r') as zipRef:
            zipRef.extractall(extractPath)
            extracted_files = zipRef.namelist()
    except zipfile.BadZipFile:
        return {"error": "The uploaded file is not a valid ZIP archive"}
    finally:
        os.remove(zipPath)

    return {"extracted_files": extracted_files, "extract_to": extractPath}

#if __name__ == __main__:
