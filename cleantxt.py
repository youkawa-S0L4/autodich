from google.colab import files
import os
import re

print('📂 Chọn file .txt cần clean...')
uploaded_clean = files.upload()

if not uploaded_clean:
    print('❌ Không có file nào!')
else:
    CLEAN_INPUT = list(uploaded_clean.keys())[0]
    CLEAN_OUTPUT = 'CLEAN_' + os.path.splitext(CLEAN_INPUT)[0] + '.txt'

    raw = None
    for enc in ['utf-8', 'utf-8-sig', 'gb18030', 'gbk', 'shift_jis', 'cp932', 'euc-jp']:
        try:
            with open(CLEAN_INPUT, 'r', encoding=enc) as f:
                raw = f.read()
            print(f'✅ Đọc file thành công (encoding: {enc})')
            break
        except:
            continue

    if raw is None:
        print('❌ Không đọc được file!')
    else:
        lines = raw.split('\n')
        print(f'📊 Tổng: {len(raw):,} ký tự | {len(lines):,} dòng')

        blank_runs = []
        count = 0
        for i, line in enumerate(lines):
            if line.strip() == '':
                count += 1
            else:
                if count >= 4:
                    blank_runs.append((i - count, i - 1, count))
                count = 0

        print(f'\n🔍 Phát hiện {len(blank_runs)} ranh giới chương (4+ dòng trắng):')
        for start, end, n in blank_runs:
            before = lines[start-1].strip()[:60] if start > 0 else ''
            after  = lines[end+1].strip()[:60] if end < len(lines)-1 else ''
            print(f'   Line {start+1}-{end+1} ({n} blanks)')
            print(f'     Trước : [{before}]')
            print(f'     Sau   : [{after}]')

        METADATA_KEYWORDS = [
            '缩略图', '电子书', 'epub', 'ISBN', 'cover', '版权', '©', 'Copyright',
            '本书', '出版', '发行', '印刷', '著作権', '無断転載', '禁止',
            '竖排', '排版', '本电子书', 'calibre', 'kindlegen',
            '目录', '根据您使用', '显示效果', '阅读系统',
            '初版', '发行人', '株式会社', 'kadokawa', '咨询方式',
            '纯属虚构', '禁止未经', '转让给第三方',
        ]

        content_start = 0
        for i, line in enumerate(lines):
            is_meta = any(kw.lower() in line.lower() for kw in METADATA_KEYWORDS)
            if not is_meta and line.strip() and i > 0:
                content_start = i
                break

        toc_end = 0
        for start, end, n in blank_runs:
            if n >= 4 and start < 50:
                toc_end = end + 1
                break

        actual_start = max(content_start, toc_end)

        content_end = len(lines) - 1
        for i in range(len(lines)-1, 0, -1):
            is_meta = any(kw.lower() in lines[i].lower() for kw in METADATA_KEYWORDS)
            if not is_meta and lines[i].strip():
                content_end = i
                break

        print(f'\n📌 Nội dung thực: dòng {actual_start+1} → {content_end+1}')
        print(f'   Đầu: [{lines[actual_start].strip()[:80]}]')
        print(f'   Cuối: [{lines[content_end].strip()[:80]}]')

        chapter_breaks = [
            (start, end) for start, end, n in blank_runs
            if actual_start < start < content_end and n >= 4
        ]

        chapter_ranges = []
        prev = actual_start
        for start, end in chapter_breaks:
            chapter_ranges.append((prev, start))
            prev = end + 1
        chapter_ranges.append((prev, content_end + 1))

        print(f'\n📖 Tổng số chương/phần: {len(chapter_ranges)}')

        ch_pattern = re.compile(
            r'^(第\s*[0-9０-９一二三四五六七八九十百千万]+\s*[章节回話话篇].*'
            r'|序章|尾声|终章|後記|后记|エピローグ|プロローグ'
            r'|(?:Chapter|CHAPTER)\s*\d+.*'
            r'|(?:Chương|CHƯƠNG)\s*\d+.*'
            r'|Prologue|Epilogue|Afterword|Foreword)$',
            re.IGNORECASE
        )

        output_parts = []
        for idx, (start, end) in enumerate(chapter_ranges):
            chunk = lines[start:end]
            while chunk and chunk[0].strip() == '':
                chunk.pop(0)
            while chunk and chunk[-1].strip() == '':
                chunk.pop()
            if not chunk:
                continue

            content_text = '\n'.join(chunk).strip()
            first_line = chunk[0].strip()

            if ch_pattern.match(first_line):
                title = f'*** {first_line}'
                body = '\n'.join(chunk[1:]).strip()
                output_parts.append(f'{title}\n{body}')
            else:
                title = f'*** Phần {idx+1}'
                output_parts.append(f'{title}\n{content_text}')

        result = '\n\n'.join(output_parts)

        with open(CLEAN_OUTPUT, 'w', encoding='utf-8') as f:
            f.write(result)

        chapter_list = [l for l in result.split('\n') if l.startswith('***')]
        print(f'\n✅ CLEAN HOÀN TẤT!')
        print(f'   File đầu ra : {CLEAN_OUTPUT}')
        print(f'   Số chương   : {len(chapter_list)}')
        print(f'   Tổng ký tự  : {len(result):,}')
        print(f'\n📋 Danh sách chương:')
        for ch in chapter_list:
            print(f'   {ch}')

        files.download(CLEAN_OUTPUT)
        print('\n⬇️ Đã tải file sạch về máy!')
