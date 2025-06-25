# Ionograms Into Images

## Описание проекта

Этот проект предназначен для преобразования ионограмм, содержащихся в бинарных файлах формата `*.dat`, в визуальные изображения `*.jpg`.

### Основные компоненты:

- **`BaseIonogramArrayBuilder`** — абстрактный базовый класс, описывающий интерфейс преобразования данных ионограммы в двумерный массив.
- **`SimpleIonogramArrayBuilder`** — конкретная реализация строителя массива, преобразующего ионограмму в `numpy.ndarray`.
- **`ShowIonogram`** — класс для отрисовки и сохранения изображения ионограммы с визуальными аннотациями, осями и цветовой шкалой.

Результаты сохраняются в директорию `data_result` в формате `JPG`, с возможностью настройки отображения сетки, подписей и цветовой шкалы.

### Пример использования:

#### Способ 1

```bash
# Запуск одной командой

python script.py test_data/03_02_05_08_00.dat --alpha_labels 0.5 --show_grid yes --show_colorbar yes --title_font_size 20 --axis_num_font_size 12 --axis_label_font_size 15 --colorbar_num_font_size 12

python script.py test_data/01_02_07_20_00.dat --alpha_labels 1 --show_grid no --show_colorbar yes --title_font_size 25 --axis_num_font_size 14 --axis_label_font_size 10 --colorbar_num_font_size 14

python script.py test_data/01_02_07_20_00.dat --alpha_labels 0 --show_grid yes --show_colorbar no --title_font_size 15 --axis_num_font_size 8 --axis_label_font_size 12 --colorbar_num_font_size 8
```

где:
- file_path — Путь к входному .dat файлу
- alpha_labels — Прозрачность подписей (0.0 - 1.0)
- show_grid — Отображение сетки (yes/no)
- show_colorbar — Отображение цветовой шкалы (yes/no)
- title_font_size — Размер шрифта заголовка
- axis_num_font_size — Размер шрифта чисел на осях
- axis_label_font_size — Размер шрифта подписей осей
- colorbar_num_font_size — Размер чисел на цветовой шкале

#### Способ 2

```bash 
# Интерактивный способ
python main.py
```

### Установка приложения

```bash
git clone https://github.com/yuvwwa/ionograms-into-images.git
cd ionograms-into-images
pip install .
```

Предварительно следует уставить библиотеку `ionread_python` или `ionread` (https://git.iszf.irk.ru/data-mapping/ionogram-wrappers.git)

### Валидация

Функция, которая показывает, что данные с картинки совпадают с данными из *.dat файла.

#validation/validation.py

`validation(img_path, dat_path)`
