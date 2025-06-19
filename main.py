import os
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
from matplotlib import cm
import src.ionread_python as ionread
from simple_builder import SimpleIonogramArrayBuilder
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

ionogram = ionread.read_ionogram('src/ionread_python/test_data/03_02_05_08_00.dat')
print(ionogram.passport)

def show_ionogram(ionogram, ion_arr, save_dir="data_result", alpha_labels=1, format="jpg"):
    os.makedirs(save_dir, exist_ok=True)

    fname = f"{ionogram.passport.session_date}_{ionogram.passport.session_time}.{format}"
    save_path = os.path.join(save_dir, fname)

    # Белый фон
    cmap = cm.get_cmap('jet').copy()
    cmap.set_under('white')

    fig = plt.figure(figsize=(10, 8), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])  # График занимает 100% площади

    norm = Normalize(vmin=1, vmax=np.max(ion_arr))
    im = ax.imshow(ion_arr, origin='lower', cmap=cmap, norm=norm, aspect='auto', extent=[0, 1, 0, 1])

    # Оси 
    # Доработать, их не видно
    num_y_ticks = 20
    num_x_ticks = 10
    d_tick_pos = np.linspace(0, 1, num_y_ticks)
    f_tick_pos = np.linspace(0, 1, num_x_ticks)
    
    d_vals = np.linspace(
        min(ionogram.data, key=lambda x: x.dist).dist,
        max(ionogram.data, key=lambda x: x.dist).dist,
        num_y_ticks
    )
    d_labels = [f'{v/300:.2f}' for v in d_vals]

    f_vals = np.linspace(
        ionogram.passport.start_freq,
        ionogram.passport.end_freq,
        num_x_ticks
    )
    f_labels = [f'{v/100:.1f}' for v in f_vals]

    ax.set_yticks(d_tick_pos)
    ax.set_yticklabels(d_labels, fontsize=10, color='black', alpha=alpha_labels)

    ax.set_xticks(f_tick_pos)
    ax.set_xticklabels(f_labels, fontsize=10, color='black', rotation=45, alpha=alpha_labels)

    # Сетка
    ax.grid(True, which='major', color='black', linestyle='--', linewidth=0.8, alpha=0.5)

    # Подписи осей
    ax.text(0.5, 0.03, 'Частота, МГц', transform=ax.transAxes,
            fontsize=13, color='black', ha='center', va='top', alpha=alpha_labels)

    ax.text(0.03, 0.5, 'Задержка, мс', transform=ax.transAxes,
            fontsize=13, color='black', ha='right', va='center', rotation=90, alpha=alpha_labels)

    # Заголовок
    first_line = f'{ionogram.passport.transmitter}-{ionogram.passport.receiver}'
    second_line = f'{ionogram.passport.session_date} {ionogram.passport.session_time}'
    title = f'{first_line}\n{second_line}'
    ax.text(0.5, 0.97, title, transform=ax.transAxes,
            fontsize=14, color='black', ha='center', va='top', alpha=alpha_labels)

    # Цветовая шкала
    cax = inset_axes(ax, width="3%", height="50%", loc='upper right',
                     bbox_to_anchor=(0, 0, 0.95, 0.95), bbox_transform=ax.transAxes)
    cbar = fig.colorbar(im, cax=cax)
    cbar.ax.tick_params(labelsize=9, colors='black')
    cax.patch.set_facecolor('black')
    cax.patch.set_alpha(0.8)

    # Ограничения осей
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    plt.savefig(save_path, bbox_inches=None, pad_inches=0, format=format, facecolor='black')
    plt.close(fig)

    print(f"Путь: {save_path}")

# 01_02_07_20_00
# 03_02_05_08_00
ionogram_array_builder = SimpleIonogramArrayBuilder(ionogram=ionogram).process()
ionogram_array = ionogram_array_builder.get_ndarray()

show_ionogram(ionogram=ionogram, ion_arr=ionogram_array, alpha_labels=1, format='jpg')