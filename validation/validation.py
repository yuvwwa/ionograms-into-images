import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import ionread_python as ionread
from ionograms_into_images.simple_builder import SimpleIonogramArrayBuilder
import os

img_path = "data_result/02.01.2014_07:20:00 UT.jpg"
dat_path = "test_data/01_02_07_20_00.dat"

def validation (img_path, dat_path):
    # Изображение
    img = mpimg.imread(img_path)
    img_height, img_width = img.shape[:2]

    # Ионограмма
    ionogram = ionread.read_ionogram(dat_path)
    ionogram_array_builder = SimpleIonogramArrayBuilder(ionogram=ionogram).process()
    ionogram_array = ionogram_array_builder.get_ndarray()
    array_height, array_width = ionogram_array.shape

    # Координаты
    x1, y1 = 200, 300
    x2, y2 = 550, 650

    # Перевод координат изображения в координаты массива
    ix1 = int((x1 / img_width) * array_width)
    ix2 = int((x2 / img_width) * array_width)
    iy1 = array_height - int((y2 / img_height) * array_height)
    iy2 = array_height - int((y1 / img_height) * array_height)

    # Вырезка фрагментов
    img_crop = img[y1:y2, x1:x2]
    ion_crop = ionogram_array[iy1:iy2, ix1:ix2]

    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    axs[0, 0].imshow(img)
    axs[0, 0].set_title("Изображение")
    axs[0, 0].add_patch(plt.Rectangle((x1, y1), x2 - x1, y2 - y1,
                                    edgecolor='red', facecolor='none', linewidth=2))
    axs[0, 0].axis("off")

    im0 = axs[0, 1].imshow(ionogram_array, cmap='jet', origin='lower', aspect='auto')
    axs[0, 1].set_title("Ионограмма")
    axs[0, 1].add_patch(plt.Rectangle((ix1, iy1), ix2 - ix1, iy2 - iy1,
                                    edgecolor='red', facecolor='none', linewidth=2))
    plt.colorbar(im0, ax=axs[0, 1])
    axs[0, 1].axis("off")

    axs[1, 0].imshow(img_crop)
    axs[1, 0].set_title("Выделенный участок фото")
    axs[1, 0].axis("off")

    im1 = axs[1, 1].imshow(ion_crop, cmap='jet', origin='lower', aspect='auto')
    axs[1, 1].set_title("Выделенный участок ионограммы")
    plt.colorbar(im1, ax=axs[1, 1])
    axs[1, 1].axis("off")

    plt.tight_layout()
    plt.show()

validation(img_path=img_path, dat_path=dat_path)