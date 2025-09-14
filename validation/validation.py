import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import ionread_python as ionread
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ionograms_into_images.simple_builder import SimpleIonogramArrayBuilder


'''
img_path = "data_result/02.01.2014_07:20:00 UT.jpg"
dat_path = "test_data/01_02_07_20_00.dat"
'''


img_path = "data_result/02.03.2016_05:08:00 UT.jpg"
dat_path = "test_data/03_02_05_08_00.dat"


def validation (img_path, dat_path):
    # Изображение
    img = mpimg.imread(img_path)
    img_height, img_width = img.shape[:2]
    print(img_height, img_width)

    # Ионограмма
    ionogram = ionread.read_ionogram(dat_path)
    ionogram_array_builder = SimpleIonogramArrayBuilder(ionogram=ionogram).process()
    ionogram_array = ionogram_array_builder.get_ndarray()
    print(ionogram_array[:5, :5])
    array_height, array_width = ionogram_array.shape
    print(array_height, array_width)

    # Координаты
    # <box label="label_3" source="Ground truth" occluded="0" xtl="283.25" ytl="125.75" xbr="478.37" ybr="360.98" z_order="0">
    # <box label="label_1" source="Ground truth" occluded="0" xtl="109.81" ytl="381.57" xbr="444.77" ybr="548.51" z_order="0">
    x1, y1 = 109.81, 381.57
    x2, y2 = 444.77, 548.51

    # Перевод координат изображения в координаты массива
    ix1 = int((x1 / img_width) * array_width)
    print(int(x1/img_width))
    ix2 = int((x2 / img_width) * array_width)
    iy1 = array_height - int((y2 / img_height) * array_height)
    iy2 = array_height - int((y1 / img_height) * array_height)

    # Вырезка фрагментов
    img_crop = img[int(round(y1)):int(round(y2)), int(round(x1)):int(round(x2))]

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