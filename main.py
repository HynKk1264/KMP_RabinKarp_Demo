import sys
import os

# Đảm bảo Python nhận diện được thư mục gốc khi chạy qua Terminal
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ui import AlgorithmApp

def main():
    # Khởi tạo toàn bộ giao diện và các Option (Kịch bản) từ file ui.py
    app = AlgorithmApp()
    
    # Kích hoạt vòng lặp chính của ứng dụng
    app.mainloop()

if __name__ == "__main__":
    main()