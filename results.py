from google.colab import files

with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
    preview = f.read()

print('📄 XEM TRƯỚC (500 ký tự đầu):')
print('-' * 55)
print(preview[:500])
print('-' * 55)
print(f'📊 Tổng ký tự bản dịch: {len(preview):,}')
files.download(OUTPUT_FILE)
print('✅ Tải xong!')
