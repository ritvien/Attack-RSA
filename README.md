# 🔐 RSA Simulation & Attack Toolkit - Project Mật mã
## 📘 Giới thiệu

Chương trình Python mô phỏng toàn diện quá trình **sinh khóa**, **mã hóa**, **giải mã** bằng RSA, đồng thời tích hợp giao diện để **mô phỏng tấn công** nhằm minh họa các điểm yếu nếu tham số RSA không đủ an toàn.

> 📌 Dành cho học phần Mật mã - Đại học Bách Khoa Hà Nội  
> 👨‍🎓 Sinh viên thực hiện:
- Nguyễn Việt Hoàng - 20227019---

## ⚙️ Tính năng chính

### 1️⃣ RSA: Sinh khóa, Mã hóa, Giải mã (`display.py`)
- 🔑 Tạo khóa RSA với độ dài bit tùy chọn (khuyên dùng >= 2048 bit).
- 🔍 Hiển thị chi tiết quá trình sinh khóa: `p`, `q`, `n`, `φ(n)`, `e`, `d`.
- 🔒 Mã hóa số nguyên `M` với khóa công khai `(e, n)`.
- 🔓 Giải mã bản mã `C` với khóa bí mật `(d, n)` nhập từ người dùng.
- ✅ So sánh kết quả giải mã với bản rõ gốc (nếu có).
- ⚠️ Cảnh báo nếu `M > n`, tự động mã hóa `M mod n`.
- 🖼️ Giao diện người dùng thân thiện sử dụng `Tkinter`.

### 2️⃣ Mô phỏng Tấn công RSA (`attack_ui.py`, `attack_src.py`)
- ✅ **Nhập liệu:** `e`, `n`, và bản mã `c`.
- 🔨 **Tấn công Trial Division:** Phân tích `n = p × q` bằng thử chia.
- 📉 **Tấn công Wiener:** Tìm `d` nhỏ thỏa mãn `d < (1/3) * n^(1/4)` thông qua liên phân số.
- 🧪 **Tấn công Brute-force M:** Thử từng giá trị `M` nhỏ để tìm khớp với `c`.
- 📊 Hiển thị trạng thái tấn công, kết quả và thời gian chạy.
- 🖥️ Giao diện riêng biệt bằng `Tkinter + ttk`.

---

## 📁 Cấu trúc Dự án

├── display.py # GUI chính: sinh khóa, mã hóa, giải mã  
├── src.py # Hàm cốt lõi RSA (modular inverse, Miller-Rabin, etc.)  
├── attack_ui.py # Giao diện mô phỏng tấn công  
├── attack_src.py # Logic của các cuộc tấn công  
└── README.md # Tài liệu hướng dẫn



---

## ▶️ Hướng dẫn sử dụng

### 🔧 Yêu cầu
- Python 3.6+
- Mặc định có sẵn: `tkinter`, `math`, `random`, `time`, `textwrap`

### 🧪 Khởi chạy mã hóa / giải mã
```bash
python display.py
```
Nhập số nguyên cần mã hóa → nhấn Xác nhận số

Nhập độ dài khóa (ví dụ: 1024) → nhấn Sinh khóa

Nhấn Mã hóa số đã nhập → bản mã sẽ hiển thị

Nhấn Bắt đầu giải mã >>, sau đó nhập d và n

Nhấn Giải mã để nhận kết quả giải mã
 ### 🧨 Khởi chạy mô phỏng tấn công
```bash
python attack_ui.py
```
Nhập giá trị: e, n, c

Chọn loại tấn công:

🧩 Phân tích thừa số

📉 Wiener (khi d nhỏ)

🔍 Brute-force M (chỉ nên dùng khi M nhỏ)

Kết quả hiển thị ở phần khung kết quả
