import os
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
from matplotlib import cm
import src.ionread_python as ionread
from simple_builder import SimpleIonogramArrayBuilder


def show_ionogram(ionogram, ion_arr, save_dir="data_result", alpha_labels=0.1, format="jpg"):
    # Создаем директорию
    os.makedirs(save_dir, exist_ok=True)

    # Узнаем имя файла
    fname = f"{ionogram.passport.session_date}_{ionogram.passport.session_time}.{format}"
    save_path = os.path.join(save_dir, fname)

    # Белый фон
    cmap = cm.get_cmap('jet').copy()
    cmap.set_under('white')
    
    fig, ax = plt.subplots(figsize=(8, 8))
    norm = Normalize(vmin=1, vmax=np.max(ion_arr))
    im = ax.imshow(ion_arr, origin='lower', cmap=cmap, norm=norm) # origin="lower" - чтобы значения по оси шли вверх

    # Убираем оси
    ax.set_xticks([])
    ax.set_yticks([])

    '''
    min_height_num = min(ionogram.data, key=lambda x: x.num_dist)
    max_height = max(ionogram.data, key=lambda x: x.dist)

    d_ticks = np.linspace(0, ion_arr.shape[0], 20)

    d_ticks_labels = [f'{dn / 300:.2f}' for dn in np.linspace(
        min_height_num.dist - 1, max_height.dist, len(d_ticks))]
    '''

    # Вертикальные тики (задержка, время)
    d_ticks = np.linspace(0, ion_arr.shape[0]-1, 5)
    d_vals = np.linspace(
        min(ionogram.data, key=lambda x: x.dist).dist,
        max(ionogram.data, key=lambda x: x.dist).dist,
        len(d_ticks)
    )
    d_labels = [f'{v/300:.2f}' for v in d_vals]

    '''
    min_freq = ionogram.passport.start_freq
    max_freq = ionogram.passport.end_freq

    f_ticks = np.linspace(0, ion_arr.shape[1], 10)

    f_ticks_labels = [
        f'{fn / 1000:.1f}' for fn in np.linspace(min_freq, max_freq, len(f_ticks))]
    '''

    # Горизонтальные тики (частоты)
    f_ticks = np.linspace(0, ion_arr.shape[1]-1, 5)
    f_vals = np.linspace(
        ionogram.passport.start_freq,
        ionogram.passport.end_freq,
        len(f_ticks)
    )
    f_labels = [f'{v/1000:.1f}' for v in f_vals]

    # Подписи внутри изображения
    for y, label in zip(d_ticks, d_labels):
        ax.text(5, y, label, color='black', alpha=alpha_labels,
                va='center', ha='left', fontsize=8)

    for x, label in zip(f_ticks, f_labels):
        ax.text(x, 5, label, color='black', alpha=alpha_labels,
                va='bottom', ha='left', fontsize=8, rotation=45)

    # Заголовок
    first_line = f'{ionogram.passport.transmitter}-{ionogram.passport.receiver}'
    second_line = f'{ionogram.passport.session_date} {ionogram.passport.session_time}'
    title = f'{first_line}\n{second_line}'

    ax.text(
        ion_arr.shape[1] // 2, ion_arr.shape[0] - 10,
        title,
        color='black',
        alpha=alpha_labels,
        ha='center',
        va='bottom',
        fontsize=10
    )

    # Убираем рамки
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Сохранение
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0.1, format=format)
    plt.close(fig)

# 01_02_07_20_00
# 03_02_05_08_00
ionogram = ionread.read_ionogram('src/ionread_python/test_data/03_02_05_08_00.dat')
ionogram_array_builder = SimpleIonogramArrayBuilder(ionogram=ionogram).process()
ionogram_array = ionogram_array_builder.get_ndarray()

print(ionogram.passport)

show_ionogram(ionogram=ionogram, ion_arr=ionogram_array, alpha_labels=1, format='jpg')