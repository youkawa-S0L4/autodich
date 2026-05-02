print('=' * 55)
print('🚀 BẮT ĐẦU DỊCH THUẬT TỰ ĐỘNG')
print('=' * 55)

chapters = parse_chapters(raw_content)
total_chapters = len(chapters)
print(f'📖 Tổng số chương: {total_chapters}')
print(f'⚡ Dịch {SO_CHUONG_MOI_LAN} chương mỗi lần')
print(f'⏳ Delay: {DELAY_GIUA_REQUEST}s/request')
print(f'⏱️  Bắt đầu lúc: {datetime.now().strftime("%H:%M:%S")}')
print('-' * 55)

translated_chapters = []
start_time = time.time()
i = 0
chunk_num = 0
total_chunks = (total_chapters + SO_CHUONG_MOI_LAN - 1) // SO_CHUONG_MOI_LAN

while i < total_chapters:
    chunk_num += 1
    batch = chapters[i:i + SO_CHUONG_MOI_LAN]
    batch_text = '\n\n'.join(batch)

    ch_names = [ch.split('\n')[0].strip()[:50] for ch in batch]
    progress = (chunk_num - 1) / total_chunks * 100
    elapsed = time.time() - start_time
    eta = (elapsed / chunk_num * total_chunks - elapsed) if chunk_num > 1 else 0

    print(f'[{chunk_num:3d}/{total_chunks}] ({progress:5.1f}%) 📝 {" | ".join(ch_names)}')
    if chunk_num > 1:
        print(f'         ⏱️  Đã qua: {elapsed/60:.1f}p | Còn lại: ~{eta/60:.1f}p')

    translated = translate_chunk(batch_text, chunk_num, total_chunks)
    translated_chapters.append(translated)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(translated_chapters))

    i += SO_CHUONG_MOI_LAN
    if i < total_chapters:
        print(f'         ⏳ Chờ {DELAY_GIUA_REQUEST}s...')
        time.sleep(DELAY_GIUA_REQUEST)

total_time = time.time() - start_time
print('=' * 55)
print(f'✅ DỊCH HOÀN TẤT!')
print(f'   Tổng thời gian : {total_time/60:.1f} phút')
print(f'   Số chương dịch : {total_chapters}')
print(f'   Tốc độ TB      : {total_time/total_chapters:.1f}s/chương')
print(f'   File đầu ra    : {OUTPUT_FILE}')
print('=' * 55)
