import detection.utils.augmentation_instruments as aui
import glob
import os
import random
import shutil
from functools import partial
from sys import argv
from tqdm import tqdm


def get_img_data(img_path):
    file_root, file_name = os.path.split(img_path)
    img_name, img_ext = os.path.splitext(file_name)
    return file_root, img_name, img_ext


def is_path(path):
    if not os.path.exists(path):
        os.mkdir(path)


def apply_augmentation(img_path, aug_type):
    """
    Применить аугментацию к изображению, если тип аугментации доступен
    и если есть файл *.txt с разметкой

    @img_path: относительный путь к изображению
    @aug_type: тип аугментации из числа "deblur", "gaus_blur", "sp_noise", "brightness", "contrast"
    """
    image = aui.PictureAugmentation(img_path)

    img_root, image_name, img_ext = get_img_data(img_path)

    brightness_level = random.choice([-150, -75, 75, 150])
    contrast_level = random.choice([-64, 64])
    mask_size_level = random.choice([7, 9, 11, 13])
    sp_noise_level = random.uniform(0.04, 0.13)

    angles = [90, 180, 270]

    augmentation = {#"deblur": partial(image.deblurring),
                    "gaus_blur": partial(image.gaussian_blurring, mask_size=mask_size_level),
                    #"sp_noise": partial(image.sp_noise, sp_noise_level),
                    "brightness": partial(image.apply_brightness_contrast, brightness=brightness_level),
                    "contrast": partial(image.apply_brightness_contrast, contrast=contrast_level)}

    augmented_image = augmentation[aug_type]()

    #is_path(os.path.join(img_root, aug_type))

    aui.save_image(augmented_image,
                   #os.path.join(img_root, aug_type),
                   img_root,
                   image_name,
                   suffix="_" + aug_type)

    # поворот аугментированного изображения на все углы
    for angle in angles:
        #im = aui.YOLORotateBbox(os.path.join(img_root, aug_type, image_name) + "_" + aug_type, img_ext, angle)
        im = aui.YOLORotateBbox(os.path.join(img_root, image_name) + "_" + aug_type, img_ext, angle)

        rotated_image = im.rotate_image()

        aui.save_image(rotated_image,
                       #os.path.join(img_root, aug_type),
                       img_root,
                       image_name,
                       suffix="_" + aug_type + "_" + "rot" + str(angle))


def augmentation(folder_path):
    # перечисляем изображения в папке
    all_files = glob.glob(os.path.join(folder_path, "*.jpg"))
    # создаём список возможных аугментаций
    #augmentation_types = {0: "deblur", 1: "gaus_blur", 2: "sp_noise", 3: "brightness", 4: "contrast"}
    augmentation_types = {0: "gaus_blur", 1: "brightness", 2: "contrast"}

    # для каждого изображения в папке применим аугментацию
    print("Augmentation is in progress...")
    for img in tqdm(all_files):
        # проверка на наличие разметки в данных
        img_root, image_name, _ = get_img_data(img)
        for aug_type in augmentation_types.values():
            apply_augmentation(img, aug_type)