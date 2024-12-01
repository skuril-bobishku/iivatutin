import os

import requests
from bs4 import BeautifulSoup

# Создаем папку для изображений
output_folder = "Pedicularis_images"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# URL страницы с изображениями
url = "https://www.inaturalist.org/taxa/49646-Pedicularis/browse_photos"

# Загружаем HTML страницу
response = requests.get(url)
if response.status_code != 200:
    print(f"Ошибка при загрузке страницы: {response.status_code}")
    exit()

# Разбираем HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Находим все изображения
image_tags = soup.find_all('img')

# Скачиваем изображения
download_count = 0
for img in image_tags:
    img_url = img.get('src')

    # Пропускаем невалидные ссылки или миниатюры
    if not img_url or "square" in img_url:
        continue

    # Добавляем полный путь к изображению, если ссылка относительная
    if img_url.startswith("/"):
        img_url = "https://www.inaturalist.org" + img_url

    try:
        img_data = requests.get(img_url).content
        img_name = os.path.join(output_folder, img_url.split('/')[-1])
        with open(img_name, 'wb') as img_file:
            img_file.write(img_data)
        print(f"Скачано: {img_name}")
        download_count += 1
    except Exception as e:
        print(f"Ошибка при скачивании {img_url}: {e}")

print(f"Всего скачано изображений: {download_count}")
