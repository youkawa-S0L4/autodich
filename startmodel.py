from google import genai
from google.genai import types
import time
from datetime import datetime

client = genai.Client(api_key=GEMINI_API_KEY)

def parse_chapters(content):
    chapters = []
    current_chapter = []
    for line in content.split('\n'):
        if line.strip().startswith('***'):
            if current_chapter:
                chapters.append('\n'.join(current_chapter).strip())
            current_chapter = [line]
        else:
            current_chapter.append(line)
    if current_chapter:
        chapters.append('\n'.join(current_chapter).strip())
    return [ch for ch in chapters if ch.strip()]

def translate_chunk(text, chunk_index, total):
    for attempt in range(MAX_RETRY):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=text,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.3,
                    max_output_tokens=8192,
                )
            )
            return response.text
        except Exception as e:
            err_str = str(e)
            if '429' in err_str:
                wait = 60 * (attempt + 1)
                print(f'     ⚠️  Rate limit! Chờ {wait}s... ({attempt+1}/{MAX_RETRY})')
            elif '404' in err_str:
                print(f'     ❌ Model không tồn tại: {MODEL_NAME}')
                return f'[LỖI MODEL - CHUNK {chunk_index}]\n{text}'
            else:
                wait = 10 * (attempt + 1)
                print(f'     ⚠️  Lỗi (lần {attempt+1}/{MAX_RETRY}): {err_str[:80]}')
            if attempt < MAX_RETRY - 1:
                time.sleep(wait if '429' in err_str else 10 * (attempt + 1))
            else:
                print(f'     ❌ Bỏ qua chunk {chunk_index}')
                return f'[LỖI DỊCH - CHUNK {chunk_index}]\n{text}'

print('✅ Đã khởi tạo model!')
print(f'   Model: {MODEL_NAME}')
