from ionograms_into_images.ionograms_into_images import ShowIonogram
import ionread_python as ionread_python
from ionograms_into_images.simple_builder import SimpleIonogramArrayBuilder


alpha_labels = float(input("Прозрачность подписей (0-1): ").strip())
grid_input = input("Отображать сетку? (Yes/No): ").strip().lower()
show_grid = grid_input == "yes"

cbar_input = input("Отображать цветовую шкалу? (Yes/No): ").strip().lower()
show_colorbar = cbar_input == "yes"

title_font_size = int(input("Размер шрифта заголовка: ").strip())
axis_num_font_size = int(input("Размер шрифта чисел на осях: ").strip())
axis_label_font_size = int(input("Размер шрифта подписей осей: ").strip())
colorbar_num_font_size = int(input("Размер чисел на цветовой шкале: ").strip())

# 01_02_07_20_00
# 03_02_05_08_00
ionogram = ionread_python.read_ionogram('test_data/03_02_05_08_00.dat')
print(ionogram.passport)

ionogram_array_builder = SimpleIonogramArrayBuilder(ionogram=ionogram).process()
ionogram_array = ionogram_array_builder.get_ndarray()

ShowIonogram.show_ionogram(
    ionogram=ionogram,
    ion_arr=ionogram_array,
    alpha_labels=alpha_labels,
    show_grid=show_grid,
    show_colorbar=show_colorbar,
    title_font_size=title_font_size,
    axis_num_font_size=axis_num_font_size,
    axis_label_font_size=axis_label_font_size,
    colorbar_num_font_size=colorbar_num_font_size,
    format='jpg'
)