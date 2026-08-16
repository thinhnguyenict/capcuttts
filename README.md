# CapCut Auto TTS

Công cụ Python biến một file truyện thành hàng nghìn đoạn text và tự động paste
từng đoạn vào CapCut Desktop trên Windows. Sau khi chạy xong, bạn có thể chọn
toàn bộ text clip và dùng tính năng **Chuyển văn bản thành giọng nói** của CapCut.

## 1. Cài đặt

1. Cài [Python](https://www.python.org/downloads/) và chọn **Add Python to PATH**.
2. Tải project này, mở CMD trong thư mục project rồi chạy:

   ```bat
   python -m pip install -r requirements.txt
   ```

3. Tạo `truyen.txt`, paste truyện vào và lưu dưới dạng UTF-8.

## 2. Kiểm tra chia đoạn

Nên xem trước các đoạn mà không điều khiển CapCut:

```bat
python auto_capcut.py truyen.txt --dry-run
```

Mặc định mỗi đoạn tối đa 350 ký tự. Có thể đổi bằng `--max-len 500`.

## 3. Chuẩn bị CapCut

1. Mở CapCut Desktop và tạo project.
2. Chọn **Văn bản → Thêm văn bản mặc định**.
3. Click vào ô nhập text, bảo đảm con trỏ đang nhấp nháy.
4. Không chạm chuột hoặc bàn phím trong lúc automation chạy.

## 4. Chạy

```bat
python auto_capcut.py truyen.txt
```

Script kích hoạt cửa sổ có tiêu đề `CapCut`, chờ 5 giây, rồi paste và xác nhận
từng đoạn. Nếu máy yếu hoặc CapCut bỏ sót đoạn, tăng thời gian nghỉ:

```bat
python auto_capcut.py truyen.txt --delay 3
```

Nếu quá trình bị dừng sau đoạn 127, tiếp tục từ đoạn 128 bằng:

```bat
python auto_capcut.py truyen.txt --start-at 128
```

Xem tất cả tùy chọn bằng `python auto_capcut.py --help`.

## Lưu ý

- Automation phụ thuộc giao diện CapCut; cửa sổ không được che hoặc thu nhỏ.
- Nên giữ cố định độ phân giải và Windows display scale.
- Hãy thử với một file ngắn trước khi xử lý toàn bộ truyện.
- Script chỉ paste text. Việc tạo TTS hàng loạt được thực hiện trong CapCut sau đó.
