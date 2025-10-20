from ionograms_into_images import MakeImageFromDatFile
import ionread_python as ionread
from ionarray.builders import *

ionogram = ionread.read_ionogram('test_data/03_02_05_08_00.dat')

boundes = IonogramBounds(
    min_freq=1000, max_freq=15000, min_dist=0, max_dist=2000)

# Получаем массив из ионограммы
boundedBuilder = BoundedIonogramArrayBuilder(boundes, ionogram).process()
ionogram_array = boundedBuilder.get_ndarray()

print(ionogram_array.shape)

# Меняем размерность массива
from ionarray.ionresize import resize_ionogram

ionogram_array = resize_ionogram(ionogram_array, (512, 512))
print(ionogram_array.shape)

print(ionogram.passport)

MakeImageFromDatFile.make_image(
    ionogram=ionogram,
    ion_arr=ionogram_array,
    alpha_labels=0,
    show_grid='no',
    show_colorbar='no',
    title_font_size=14,
    axis_num_font_size=8,
    axis_label_font_size=10,
    colorbar_num_font_size=10,
    format='png'
)