CHUONG_CAN_DICH_LAI = [1, 2]  # ← Sửa số chương cần dịch lại

for ch_num in CHUONG_CAN_DICH_LAI:
    idx = ch_num - 1
    if 0 <= idx < len(chapters):
        print(f'🔄 Dịch lại chương {ch_num}: {chapters[idx].split(chr(10))[0][:40]}')
        time.sleep(DELAY_GIUA_REQUEST)
        translated_chapters[idx] = translate_chunk(chapters[idx], ch_num, total_chapters)
        print(f'✅ Xong chương {ch_num}!')
    else:
        print(f'❌ Chương {ch_num} không tồn tại!')

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(translated_chapters))
print('✅ Đã lưu!')
files.download(OUTPUT_FILE)
