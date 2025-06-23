import os
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
from matplotlib import cm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

class ShowIonogram:
    def show_ionogram(ionogram, ion_arr, save_dir="data_result", alpha_labels=1, format="jpg",
                    show_grid=True, show_colorbar=True, title_font_size=20, axis_num_font_size=10, 
                    axis_label_font_size=14, colorbar_num_font_size=10):
        os.makedirs(save_dir, exist_ok=True)

        fname = f"{ionogram.passport.session_date}_{ionogram.passport.session_time}.{format}"
        save_path = os.path.join(save_dir, fname)

        # Белый фон
        cmap = cm.get_cmap('jet').copy()
        cmap.set_under('white')

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_axes([0, 0, 1, 1])  # График занимает 100% площади

        norm = Normalize(vmin=1, vmax=np.max(ion_arr))
        im = ax.imshow(ion_arr, origin='lower', cmap=cmap, norm=norm, aspect='auto', extent=[0, 1, 0, 1])

        # Оси
        num_y_ticks = 20
        num_x_ticks = 10
        d_tick_pos = np.linspace(0, 1, num_y_ticks)[1:-1] # [1:-1] - Убираем крайние значения
        f_tick_pos = np.linspace(0, 1, num_x_ticks)[1:-1]
        
        d_vals = np.linspace(
            min(ionogram.data, key=lambda x: x.dist).dist,
            max(ionogram.data, key=lambda x: x.dist).dist,
            num_y_ticks
        )[1:-1]
        d_labels = [f'{v/300:.2f}' for v in d_vals]

        f_vals = np.linspace(
            ionogram.passport.start_freq,
            ionogram.passport.end_freq,
            num_x_ticks
        )[1:-1]
        f_labels = [f'{v/1000:.1f}' for v in f_vals]

        # Отключаем тики
        ax.set_xticks([])
        ax.set_yticks([])

        # Сетка
        if show_grid:
            for pos in f_tick_pos:
                ax.axvline(x=pos, ymin=0, ymax=1, color='black', linestyle='--', alpha=alpha_labels)
            
            for pos in d_tick_pos:
                ax.axhline(y=pos, xmin=0, xmax=1, color='black', linestyle='--', alpha=alpha_labels)
            
            ax.grid(True, which='major', color='black', linestyle='--', alpha=alpha_labels)
        
        # Рисуем тики и подписи вручную поверх данных
        for i, (pos, label) in enumerate(zip(f_tick_pos, f_labels)):
            # Вертикальные линии
            ax.axvline(x=pos, ymin=0, ymax=0.01, color='black', alpha=alpha_labels, linewidth=1)
            # Подписи
            ax.text(pos, 0.02, label, transform=ax.transData, fontsize=axis_num_font_size, 
                    color='black', alpha=alpha_labels, ha='center', va='bottom', rotation=45)
        
        for i, (pos, label) in enumerate(zip(d_tick_pos, d_labels)):
            # Горизонтальные линии
            ax.axhline(y=pos, xmin=0, xmax=0.01, color='black', alpha=alpha_labels, linewidth=1)
            # Подписи
            ax.text(0.02, pos, label, transform=ax.transData, fontsize=axis_num_font_size,
                    color='black', alpha=alpha_labels, ha='left', va='center')

        # Рассчет отступа подписей осей от чисел на осях
        x_axis_y_offset = 0.07 + axis_num_font_size * 0.002
        y_axis_x_offset = 0.07 + axis_num_font_size * 0.002

        # Подписи осей
        ax.text(0.5, x_axis_y_offset, 'Частота, МГц', transform=ax.transAxes,
                fontsize=axis_label_font_size, color='black', ha='center', va='top', alpha=alpha_labels)

        ax.text(y_axis_x_offset, 0.5, 'Задержка, мс', transform=ax.transAxes,
                fontsize=axis_label_font_size, color='black', ha='right', va='center', rotation=90, alpha=alpha_labels)

        # Заголовок
        first_line = f'{ionogram.passport.transmitter}-{ionogram.passport.receiver}'
        second_line = f'{ionogram.passport.session_date} {ionogram.passport.session_time}'
        title = f'{first_line}\n{second_line}'
        ax.text(0.5, 0.97, title, transform=ax.transAxes,
                fontsize=title_font_size, color='black', ha='center', va='top', alpha=alpha_labels)

        # Цветовая шкала
        if show_colorbar:
            cax = inset_axes(ax, width="3%", height="50%", loc='upper right',
                             bbox_to_anchor=(0, 0, 0.95, 0.95), bbox_transform=ax.transAxes)
            cbar = fig.colorbar(im, cax=cax)

            # Устанавливаем прозрачность чисел
            cbar.ax.tick_params(labelsize=colorbar_num_font_size, colors='black')
            for tick in cbar.ax.get_yticklabels():
                tick.set_alpha(alpha_labels)

            # Устанавливаем прозрачность самой шкалы
            cbar.solids.set_alpha(alpha_labels)

            cax.patch.set_facecolor('black')
            cax.patch.set_alpha(0.1)

        # Ограничения осей
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        plt.savefig(save_path, bbox_inches=None, pad_inches=0, format=format, facecolor='black')
        plt.close(fig)

        print(f"Путь: {save_path}")