#!/usr/bin/env python3
import os
import re
from PIL import Image, ImageDraw, ImageFont

# 字体大小已增大两号
try:
    font_size = 20
    font = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', font_size)
    font_bold = font
except Exception as e:
    print(f"字体加载失败: {e}")
    font = ImageFont.load_default()
    font_bold = font

def parse_markdown_table(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')
    table_lines = []
    in_table = False
    for line in lines:
        if line.strip().startswith('|') and '|' in line:
            table_lines.append(line)
            in_table = True
        elif in_table and not line.strip():
            break
        elif in_table:
            table_lines.append(line)
    raw_data = []
    for line in table_lines:
        if line.strip().startswith('|---') or line.strip().startswith('|--'):
            continue
        cells = [cell.strip() for cell in line.split('|')]
        if len(cells) > 2:
            raw_data.append(cells[1:-1])
    return raw_data

def parse_cell(cell_text):
    """解析单元格，返回类别-菜品对列表"""
    paragraphs = cell_text.split('<br>')
    cat_dishes = {}
    order = ['主食', '配菜', '面点', '副食', '汤品']
    for para in paragraphs:
        para = para.strip()
        if not para or para == '<br>':
            continue
        start = para.find('**')
        end = para.find('**', start + 2) if start != -1 else -1
        if start != -1 and end != -1:
            category = para[start+2:end].strip().replace('：', '').replace(':', '').strip()
            content = para[end+2:].strip()
            if content.startswith(':') or content.startswith('：'):
                content = content[1:].strip()
            content = content.replace('**', '').replace('<br>', '').strip()
            dishes = [d.strip() for d in re.split(r'[、，,]', content) if d.strip()]
            if dishes:
                if category in cat_dishes:
                    # 合并重复类别
                    cat_dishes[category].extend(dishes)
                else:
                    cat_dishes[category] = dishes
            continue
        clean = para.replace('**', '').replace('<br>', '').strip()
        if clean:
            cat_dishes.setdefault('其他', []).append(clean)
    # 修改：如果'主食'类别存在且包含'甑糕'，则将其移至'副食'
    if '主食' in cat_dishes and '甑糕' in cat_dishes['主食']:
        cat_dishes['主食'].remove('甑糕')
        if '副食' not in cat_dishes:
            cat_dishes['副食'] = []
        cat_dishes['副食'].append('甑糕')
    lines = []
    for cat in order:
        if cat in cat_dishes:
            dish_str = '、'.join(cat_dishes[cat])
            lines.append((cat, dish_str))
    if '其他' in cat_dishes:
        for dish in cat_dishes['其他']:
            lines.append(('', dish))
    return lines

def wrap_text(text, font, max_width):
    """将文本按最大宽度换行，返回行列表"""
    lines = []
    current = ''
    for char in text:
        test = current + char
        w = font.getlength(test) if hasattr(font, 'getlength') else font.getsize(test)[0]
        if w <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            if font.getlength(char) > max_width:
                lines.append(char)
                current = ''
            else:
                current = char
    if current:
        lines.append(current)
    return lines

# 解析表格
markdown_file = os.path.expanduser('~/FoodMenue/2026-03-13.md')
raw_data = parse_markdown_table(markdown_file)

# 初始列宽（可调整）
col_widths = [80, 380, 380, 360]
cell_padding_x = 10
cell_padding_y = 10
line_spacing = 24

# 预处理：计算每个单元格需要多少行，并自适应列宽
max_lines_per_cell = 0
processed_data = []
col_content_widths = [0] * len(col_widths)  # 记录每列内容最大宽度

for row_idx, row in enumerate(raw_data):
    proc_row = []
    for col_idx, cell in enumerate(row):
        if row_idx == 0:
            lines = [cell]
            # 表头宽度
            w = font_bold.getlength(cell) if hasattr(font_bold, 'getlength') else font_bold.getsize(cell)[0]
            if w > col_content_widths[col_idx]:
                col_content_widths[col_idx] = w
        else:
            pairs = parse_cell(cell)
            lines = []
            for cat, dishes in pairs:
                if cat:
                    line_str = f"{cat}：{dishes}"
                else:
                    line_str = dishes
                # 检查是否需要换行
                wrapped = wrap_text(line_str, font, col_widths[col_idx] - 2*cell_padding_x)
                lines.extend(wrapped)
            # 更新列内容宽度
            for line in lines:
                w = font.getlength(line) if hasattr(font, 'getlength') else font.getsize(line)[0]
                if w > col_content_widths[col_idx]:
                    col_content_widths[col_idx] = w
        proc_row.append(lines)
        if len(lines) > max_lines_per_cell:
            max_lines_per_cell = len(lines)
    processed_data.append(proc_row)

# 根据内容调整列宽（最小宽度 + padding）
final_col_widths = []
for i, base_width in enumerate(col_widths):
    needed = int(col_content_widths[i] + 2 * cell_padding_x)
    final_col_widths.append(max(base_width, needed))

# 尺寸计算
header_row_h = 50
content_row_h = cell_padding_y * 2 + max_lines_per_cell * line_spacing
start_y = 30
padding_bottom = 30
total_h = start_y + header_row_h + (len(raw_data)-1) * content_row_h + padding_bottom
total_w = sum(final_col_widths) + 40

img = Image.new('RGB', (total_w, total_h), 'white')
draw = ImageDraw.Draw(img)

# 绘制
for row_idx, row in enumerate(processed_data):
    y = start_y if row_idx == 0 else start_y + header_row_h + (row_idx-1) * content_row_h
    row_h = header_row_h if row_idx == 0 else content_row_h
    x = 20
    for col_idx, lines in enumerate(row):
        col_w = final_col_widths[col_idx]
        fill_color = '#4CAF50' if row_idx == 0 else 'white'
        draw.rectangle([x, y, x+col_w, y+row_h], fill=fill_color, outline='black')
        
        # 垂直居中：计算实际行高
        total_text_h = len(lines) * line_spacing
        text_y = y + (row_h - total_text_h) // 2 + 4
        
        for i, line in enumerate(lines):
            text_x = x + cell_padding_x
            # 表头加粗，其他正常
            use_font = font_bold if row_idx == 0 else font
            draw.text((text_x, text_y + i * line_spacing), line, fill='white' if row_idx==0 else 'black', font=use_font)
        x += col_w

output_path = os.path.expanduser('~/FoodMenue/2026-03-13-table.png')
img.save(output_path)
print(f'图片已保存 (尺寸: {total_w}x{total_h}, 最大行数: {max_lines_per_cell}, 列宽: {final_col_widths})')