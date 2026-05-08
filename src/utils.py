import time
import random
import string
import PyPDF2
from .kmp import kmp_search
from .rabin_karp import rabin_karp_search

def read_text_file(file_path):
    """Đọc nội dung từ file TXT hoặc PDF."""
    if file_path.endswith('.pdf'):
        text = ""
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted
        except Exception as e:
            print(f"Lỗi đọc file PDF: {e}")
        return text
    else:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Lỗi đọc file TXT: {e}")
            return ""

# --- KỊCH BẢN 1: TÌM 1 TỪ KHÓA ---
def benchmark_single_word(text, pattern, iterations=50):
    """Đo thời gian tìm 1 từ khóa lặp lại nhiều lần."""
    kmp_times, rk_times = [], []
    for _ in range(iterations):
        # Đo KMP
        t0 = time.perf_counter()
        kmp_search(text, pattern)
        kmp_times.append(time.perf_counter() - t0)
        
        # Đo Rabin-Karp
        t1 = time.perf_counter()
        rabin_karp_search(text, pattern)
        rk_times.append(time.perf_counter() - t1)
        
    return kmp_times, rk_times

# --- KỊCH BẢN 2: TÌM NHIỀU TỪ KHÓA CÙNG LÚC (DLP SCANNER) ---
def benchmark_multi_word(text, patterns, iterations=50):
    """Đo thời gian tìm kiếm MỘT DANH SÁCH từ khóa."""
    kmp_times, rk_times = [], []
    for _ in range(iterations):
        # Đo KMP: Phải lặp qua từng từ và quét lại từ đầu
        t0 = time.perf_counter()
        for pat in patterns:
            if pat.strip():
                kmp_search(text, pat.strip())
        kmp_times.append(time.perf_counter() - t0)
        
        # Đo Rabin-Karp: (Trong thực tế RK có thể tối ưu gom nhóm băm, 
        # ở đây chạy cơ bản để làm mốc so sánh chuẩn)
        t1 = time.perf_counter()
        for pat in patterns:
            if pat.strip():
                rabin_karp_search(text, pat.strip())
        rk_times.append(time.perf_counter() - t1)
        
    return kmp_times, rk_times

# --- KỊCH BẢN 3: STRESS TEST (TẤN CÔNG HIỆU NĂNG) ---
def benchmark_stress_test(size, iterations=30):
    """
    Sinh văn bản lặp lại ác ý để ép Rabin-Karp đụng độ băm.
    Ví dụ: Văn bản toàn chữ 'A', từ khóa là 'A' lặp lại 50 lần rồi kết thúc bằng 'B'.
    """
    text = "A" * size
    pattern = ("A" * 50) + "B" 
    
    kmp_times, rk_times = [], []
    for _ in range(iterations):
        # Đo KMP
        t0 = time.perf_counter()
        kmp_search(text, pattern)
        kmp_times.append(time.perf_counter() - t0)
        
        # Đo Rabin-Karp
        t1 = time.perf_counter()
        rabin_karp_search(text, pattern)
        rk_times.append(time.perf_counter() - t1)
        
    return kmp_times, rk_times