# 🚀 Auto Dịch Thuật Truyện

> Công cụ dịch thuật tự động cho truyện light novel / web novel  
> Hỗ trợ: 🇨🇳 Trung · 🇯🇵 Nhật · 🇰🇷 Hàn · 🇬🇧 Anh → 🇻🇳 Việt

---

## ✨ Tính năng

- 📖 **Tự động phát hiện chương** — nhận file .txt bất kỳ, tự tìm ranh giới chương
- 🧹 **Clean file thông minh** — loại bỏ metadata, TOC, colophon epub tự động
- 🤖 **Dịch bằng Gemini AI** — prompt văn học chuyên nghiệp, dịch mượt mà tự nhiên
- 💾 **Lưu tiến độ liên tục** — mất điện / ngắt mạng không mất dữ liệu đã dịch
- 🔄 **Retry tự động** — tự xử lý rate limit, lỗi mạng, response rỗng
- 📝 **Dịch lại từng chương** — có thể dịch lại riêng chương bị lỗi

---

## 📋 Yêu cầu

- Tài khoản **Google** (để dùng Google Colab)
- **Gemini API Key** miễn phí tại [aistudio.google.com](https://aistudio.google.com/app/apikey)
- File truyện định dạng `.txt`

---

## 📱 Dùng trên Điện Thoại

### Bước 1 — Lấy API Key
Vào [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) → **Create API Key** → copy key

### Bước 2 — Mở Google Colab
Vào [colab.research.google.com](https://colab.research.google.com) bằng trình duyệt → **New Notebook**

### Bước 3 — Copy từng cell vào Colab
Copy lần lượt 8 cell code từ file `auto_translate.ipynb` dán vào từng ô

### Bước 4 — Nhập API Key
Trong **Cell 3** tìm dòng:
```python
GEMINI_API_KEY = "YOUR_API_KEY_HERE"
```
Thay bằng key vừa copy ở Bước 1

### Bước 5 — Chạy theo thứ tự

| Cell | Chức năng |
|------|-----------|
| Cell 1 | Cài thư viện |
| Cell 2 | **Clean file** gốc → tải về `CLEAN_xxx.txt` |
| Cell 3 | Cấu hình API key, model, ngôn ngữ |
| Cell 4 | Upload file `CLEAN_xxx.txt` |
| Cell 5 | Khởi tạo model Gemini |
| Cell 6 | **Bắt đầu dịch tự động** |
| Cell 7 | Tải file kết quả về máy |
| Cell 8 | _(Tùy chọn)_ Dịch lại chương bị lỗi |

> ⚠️ Nếu Cell 1 báo **"Failed to fetch"** → vào **Runtime → Restart session** rồi chạy lại

---

## 🖥️ Dùng trên Máy Tính (Python)

### Bước 1 — Cài Python
Tải Python tại [python.org/downloads](https://www.python.org/downloads) → cài đặt  
Tick ✅ **"Add Python to PATH"** khi cài

### Bước 2 — Cài thư viện
Mở **Terminal** (Mac/Linux) hoặc **Command Prompt** (Windows):
```bash
pip install google-genai
```

### Bước 3 — Tạo file `translate.py`
Tạo file mới, copy toàn bộ code từ `auto_translate.ipynb` vào (bỏ qua các lệnh `files.upload()` và `files.download()`)

Thay phần upload/download bằng:
```python
# Đọc file trực tiếp
INPUT_FILE = "ten_file_cua_ban.txt"
OUTPUT_FILE = "DICH_" + INPUT_FILE

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    raw_content = f.read()

# Sau khi dịch xong, file tự lưu tại cùng thư mục
```

### Bước 4 — Chạy
```bash
python translate.py
```

---

## 📁 Định dạng file

File `.txt` sau khi clean sẽ có dạng:

```
*** 序章
Nội dung chương...

*** 第一章 入团考试
Nội dung chương...

*** 第二章 在骑士団
Nội dung chương...
```

> Dấu `***` ở đầu dòng = ranh giới chương. Tool tự thêm nếu file chưa có.

---

## ⚙️ Cấu hình

Chỉnh trong **Cell 3** (Colab) hoặc đầu file `translate.py`:

```python
# Model free tier (tháng 5/2026)
MODEL_NAME = "gemini-3.1-flash-lite-preview"  # Nhanh, 15 RPM, 1000/ngày
# MODEL_NAME = "gemini-3-flash"               # Chất lượng hơn, 10 RPM

# Ngôn ngữ
NGON_NGU_NGUON = "Chinese"    # Chinese / Japanese / Korean / English
NGON_NGU_DICH  = "Vietnamese"

# Hiệu suất
SO_CHUONG_MOI_LAN  = 1   # Tăng 2-3 nếu muốn nhanh hơn
DELAY_GIUA_REQUEST = 10  # Giây chờ giữa các request
MAX_RETRY          = 5   # Số lần thử lại khi lỗi
```

---

## 🛠️ Xử lý lỗi thường gặp

| Lỗi | Nguyên nhân | Cách fix |
|-----|-------------|----------|
| `404 NOT_FOUND` | Tên model sai hoặc đã deprecated | Đổi `MODEL_NAME` trong Cell 3 |
| `429 RESOURCE_EXHAUSTED` | Vượt rate limit free tier | Tăng `DELAY_GIUA_REQUEST` lên 30–60s |
| `NoneType` khi lưu file | Model trả về response rỗng | Tool tự retry, hoặc dùng Cell 8 dịch lại |
| `Failed to fetch` | Mất kết nối Colab | Restart session → chạy lại Cell 1 |
| Không phát hiện chương | File không có tiêu đề rõ | Chạy Cell 2, tool tự tách theo đoạn trắng |

---

## 📊 Free Tier Gemini API (tháng 5/2026)

| Model | RPM | RPD | Chất lượng |
|-------|-----|-----|------------|
| `gemini-3.1-flash-lite-preview` | 15 | 1,000 | ⭐⭐⭐ |
| `gemini-3-flash` | 10 | 500 | ⭐⭐⭐⭐ |

> Kiểm tra model mới nhất tại [ai.google.dev/gemini-api/docs/models](https://ai.google.dev/gemini-api/docs/models)

---

## 📤 Lưu trữ trên GitHub

### Lần đầu — Tạo repo & push code

```bash
# 1. Tạo thư mục project
mkdir auto-dich-thuat-gemini
cd auto-dich-thuat-gemini

# 2. Bỏ README.md và auto_translate.ipynb vào thư mục này

# 3. Khởi tạo git
git init
git add .
git commit -m "first commit: auto dich thuat gemini"

# 4. Kết nối repo GitHub (thay YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/auto-dich-thuat-gemini.git
git branch -M main
git push -u origin main
```

> Tạo repo tại [github.com/new](https://github.com/new) trước khi push

### Các lần sau — Cập nhật code

```bash
git add .
git commit -m "cập nhật: mô tả thay đổi"
git push
```

### Xem trên điện thoại
Tải app **GitHub** (iOS/Android) → đăng nhập → vào repo để xem code và README

---

## 📝 System Prompt

Tool dùng prompt dịch thuật văn học chuyên nghiệp:

- Giữ nguyên kính ngữ tiếng Nhật (`-san`, `-chan`, `-sensei`)
- Dịch onomatopoeia sang từ tượng thanh tiếng Việt tương đương
- Giữ nguyên dấu ngoặc kép `「」『』`
- Văn phong phù hợp thể loại (cổ trang / hiện đại / hài)
- Chửi thề dịch sang chửi thề tiếng Việt

---

## 📄 License

MIT License — Tự do sử dụng, chỉnh sửa, chia sẻ.

---

<div align="center">
Made with ❤️ · Powered by sola
</div>
