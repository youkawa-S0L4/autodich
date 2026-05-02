from google.colab import files
import os
import re

print('📂 Chọn file CLEAN_.txt để dịch...')
uploaded = files.upload()

if not uploaded:
    print('❌ Không có file nào được chọn!')
else:
    INPUT_FILE = list(uploaded.keys())[0]
    OUTPUT_FILE = 'DICH_' + os.path.splitext(INPUT_FILE)[0] + '.txt'
    print(f'✅ File đầu vào : {INPUT_FILE}')
    print(f'✅ File đầu ra  : {OUTPUT_FILE}')

    raw = None
    for enc in ['utf-8', 'utf-8-sig', 'gb18030', 'gbk', 'shift_jis', 'cp932', 'euc-jp']:
        try:
            with open(INPUT_FILE, 'r', encoding=enc) as f:
                raw = f.read()
            print(f'✅ Encoding: {enc}')
            break
        except:
            continue

    if raw is None:
        print('❌ Không đọc được file!')
    else:
        raw_content = raw
        print(f'📊 Tổng ký tự: {len(raw_content):,}')
        chapter_lines = [l for l in raw_content.split('\n') if l.strip().startswith('***')]
        print(f'\n📖 Tổng số chương: {len(chapter_lines)}')
        for i, ch in enumerate(chapter_lines):
            print(f'   {i+1}. {ch.strip()}')
