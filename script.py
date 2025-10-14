import argparse
from ionograms_into_images import MakeImageFromDatFile
import ionread_python as ionread
from ionarray.builders import *

def main():
    parser = argparse.ArgumentParser(description="Визуализация ионограммы из .dat файла.")
    parser.add_argument("file_path", type=str, help="Путь к входному .dat файлу")
    parser.add_argument("--save_dir", type=str, default="data_result", help="Директория для сохранения результатов")
    parser.add_argument("--alpha_labels", type=float, default=1.0, help="Прозрачность подписей (0.0 - 1.0)")
    parser.add_argument("--show_grid", type=str, default='yes', help="Отображение сетки (yes/no)")
    parser.add_argument("--show_colorbar", type=str, default='yes', help="Отображение цветовой шкалы (yes/no)")
    parser.add_argument("--title_font_size", type=int, default=20, help="Размер шрифта заголовка")
    parser.add_argument("--axis_num_font_size", type=int, default=12, help="Размер шрифта чисел на осях")
    parser.add_argument("--axis_label_font_size", type=int, default=15, help="Размер шрифта подписей осей")
    parser.add_argument("--colorbar_num_font_size", type=int, default=12, help="Размер чисел на цветовой шкале")

    args = parser.parse_args()

    # Проверка корректности значений
    if not (0.0 <= args.alpha_labels <= 1.0):
        parser.error("grid_alpha должен быть в диапазоне [0.0, 1.0]")
    if args.show_grid.lower() not in ['yes', 'no']:
        parser.error("show_grid должен быть 'yes' или 'no'")
    if args.show_colorbar.lower() not in ['yes', 'no']:
        parser.error("show_colorbar должен быть 'yes' или 'no'")


    try:
        ionogram = ionread.read_ionogram(args.file_path)
  
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

        MakeImageFromDatFile.make_image(
            ionogram = ionogram,
            ion_arr = ionogram_array,
            save_dir = args.save_dir,
            alpha_labels = args.alpha_labels,
            show_grid = args.show_grid,
            show_colorbar = args.show_colorbar,
            title_font_size = args.title_font_size,
            axis_num_font_size = args.axis_num_font_size,
            axis_label_font_size = args.axis_label_font_size,
            colorbar_num_font_size = args.colorbar_num_font_size
        )

    except Exception as e:
        parser.error(f"Ошибка при обработке файла: {e}")


if __name__ == "__main__":
    main()


# Пример запуска программы
# python script.py test_data/03_02_05_08_00.dat --alpha_labels 0.5 --show_grid yes --show_colorbar yes --title_font_size 20 --axis_num_font_size 12 --axis_label_font_size 15 --colorbar_num_font_size 12
# python script.py test_data/01_02_07_20_00.dat --alpha_labels 1 --show_grid yes --show_colorbar yes --title_font_size 20 --axis_num_font_size 12 --axis_label_font_size 15 --colorbar_num_font_size 12
# python script.py test_data/01_02_07_20_00.dat --alpha_labels 0 --show_grid yes --show_colorbar yes --title_font_size 20 --axis_num_font_size 12 --axis_label_font_size 15 --colorbar_num_font_size 12