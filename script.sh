#!/bin/bash

mkdir -p data_result/2021/09MCP20150626

find test_data/2021/09MCP20150626 -name "*.dat" | while read file; do
    echo "Обрабатываю: $file"
    python script.py "$file" \
        --save_dir "data_result/2021/09MCP20150626" \
        --alpha_labels 0 \
        --show_grid yes \
        --show_colorbar yes \
        --title_font_size 20 \
        --axis_num_font_size 12 \
        --axis_label_font_size 15 \
        --colorbar_num_font_size 12
done

echo "Готово"