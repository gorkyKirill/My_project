import os
from PIL import Image

def count_pixels(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        return width * height

directory = 'C:/Users/gorky/Downloads/artificial_intelligence/negative'
trash_directory = 'C:/Users/gorky/Downloads/artificial_intelligence/trash'

if not os.path.exists(trash_directory):
    os.makedirs(trash_directory)

for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):
        try:
            img = Image.open(file_path)
            num_pixels = count_pixels(file_path)
            if img.format != 'JPEG' or img.verify() is False or num_pixels > 89478485:
                os.rename(file_path, os.path.join(trash_directory, filename))
                print(f"Файл {filename} перемещен в папку 'trash'")
        except Exception as e:
            print(f"Ошибка при обработке файла {filename}: {e}")
            os.rename(file_path, os.path.join(trash_directory, filename))
            print(f"Файл {filename} перемещен в папку 'trash'")

