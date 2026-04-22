import time
import random
import string
import PyPDF2
from .kmp import kmp_search
from .rabin_karp import rabin_karp_search

def read_text_file(file_path):
    if file_path.endswith('.pdf'):
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        return text
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

def run_benchmark(num_elements):
    text = ''.join(random.choices(string.ascii_letters + string.digits, k=num_elements))
    start_idx = random.randint(0, max(0, num_elements - 5))
    pattern = text[start_idx : start_idx + 5]

    kmp_times, rk_times = [], []

    for _ in range(100):
        t0 = time.perf_counter()
        kmp_search(text, pattern)
        kmp_times.append(time.perf_counter() - t0)
        
        t1 = time.perf_counter()
        rabin_karp_search(text, pattern)
        rk_times.append(time.perf_counter() - t1)

    return kmp_times, rk_times