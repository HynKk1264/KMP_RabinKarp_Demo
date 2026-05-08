import customtkinter as ctk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import các hàm logic từ các module trong src
from .kmp import kmp_search
from .rabin_karp import rabin_karp_search
from .utils import (
    read_text_file, 
    benchmark_single_word, 
    benchmark_multi_word, 
    benchmark_stress_test
)

# Cấu hình giao diện tổng thể
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AlgorithmApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PTIT - Hệ thống Phân tích & So sánh Thuật toán Tìm kiếm")
        self.geometry("1100x850")

        # Layout chính
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Header ---
        self.label_title = ctk.CTkLabel(
            self, 
            text="PHÂN TÍCH HIỆU NĂNG: KMP vs RABIN-KARP", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.label_title.grid(row=0, column=0, padx=20, pady=25)

        # --- Tabview chứa 3 Kịch bản ---
        self.tabview = ctk.CTkTabview(self, height=180)
        self.tabview.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Cấu hình Tab 1: Single Search
        self.tab_single = self.tabview.add("Option 1: Tìm 1 từ")
        self.entry_single = ctk.CTkEntry(self.tab_single, placeholder_text="Nhập 1 từ khóa (vd: confidential)", width=450)
        self.entry_single.pack(side="left", padx=20, pady=20)
        self.btn_single = ctk.CTkButton(self.tab_single, text="Phân tích File", command=self.handle_option_1)
        self.btn_single.pack(side="left", padx=20, pady=20)

        # Cấu hình Tab 2: Multi Search (DLP)
        self.tab_multi = self.tabview.add("Option 2: Tìm nhiều từ")
        self.entry_multi = ctk.CTkEntry(self.tab_multi, placeholder_text="Nhập danh sách từ khóa, cách nhau bằng dấu phẩy", width=450)
        self.entry_multi.pack(side="left", padx=20, pady=20)
        self.btn_multi = ctk.CTkButton(self.tab_multi, text="Quét DLP", fg_color="#e67e22", hover_color="#d35400", command=self.handle_option_2)
        self.btn_multi.pack(side="left", padx=20, pady=20)

        # Cấu hình Tab 3: Stress Test
        self.tab_stress = self.tabview.add("Option 3: Stress Test")
        self.entry_stress = ctk.CTkEntry(self.tab_stress, placeholder_text="Nhập kích thước dữ liệu (vd: 500000)", width=450)
        self.entry_stress.pack(side="left", padx=20, pady=20)
        self.btn_stress = ctk.CTkButton(self.tab_stress, text="Chạy Stress Test", fg_color="#c0392b", hover_color="#a93226", command=self.handle_option_3)
        self.btn_stress.pack(side="left", padx=20, pady=20)

        # --- Khu vực hiển thị Biểu đồ ---
        self.plot_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.plot_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        self.canvas = None

    def calculate_p99(self, times):
        """Tính toán độ trễ ở phân vị thứ 99."""
        if not times: return 0
        sorted_times = sorted(times)
        index = int(0.99 * len(sorted_times))
        return sorted_times[min(index, len(sorted_times) - 1)]

    def handle_option_1(self):
        pattern = self.entry_single.get()
        if not pattern:
            messagebox.showwarning("Chú ý", "Vui lòng nhập từ khóa!")
            return
            
        path = filedialog.askopenfilename(filetypes=[("Documents", "*.txt *.pdf")])
        if path:
            text = read_text_file(path)
            kmp_t, rk_t = benchmark_single_word(text, pattern)
            self.draw_analytics(kmp_t, rk_t, f"Option 1: Tìm '{pattern}' (Size: {len(text)})")
            self.show_report("Báo cáo Option 1", kmp_t, rk_t)

    def handle_option_2(self):
        raw_patterns = self.entry_multi.get()
        if not raw_patterns:
            messagebox.showwarning("Chú ý", "Vui lòng nhập danh sách từ khóa!")
            return
            
        patterns = [p.strip() for p in raw_patterns.split(",") if p.strip()]
        path = filedialog.askopenfilename(filetypes=[("Documents", "*.txt *.pdf")])
        if path:
            text = read_text_file(path)
            kmp_t, rk_t = benchmark_multi_word(text, patterns)
            self.draw_analytics(kmp_t, rk_t, f"Option 2: Tìm {len(patterns)} từ (Size: {len(text)})")
            self.show_report("Báo cáo Option 2", kmp_t, rk_t)

    def handle_option_3(self):
        try:
            size = int(self.entry_stress.get())
            kmp_t, rk_t = benchmark_stress_test(size)
            self.draw_analytics(kmp_t, rk_t, f"Option 3: Stress Test (Worst-case) - Size: {size}")
            self.show_report("Báo cáo Stress Test", kmp_t, rk_t)
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số nguyên hợp lệ!")

    def show_report(self, title, kmp_t, rk_t):
        avg_kmp, p99_kmp = sum(kmp_t)/len(kmp_t), self.calculate_p99(kmp_t)
        avg_rk, p99_rk = sum(rk_t)/len(rk_t), self.calculate_p99(rk_t)
        
        report = (f"{title}\n" + "="*30 + "\n"
                  f"[KMP]\n- Trung bình: {avg_kmp:.8f}s\n- P99 Latency: {p99_kmp:.8f}s\n\n"
                  f"[Rabin-Karp]\n- Trung bình: {avg_rk:.8f}s\n- P99 Latency: {p99_rk:.8f}s")
        messagebox.showinfo("Kết quả chi tiết", report)

    def draw_analytics(self, kmp_t, rk_t, title):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), dpi=100)
        fig.patch.set_facecolor('#f5f5f5')

        # 1. Biểu đồ đường (Hiệu năng theo thời gian)
        ax1.plot(kmp_t, label='KMP', color='#3498db', marker='o', markersize=3, alpha=0.8)
        ax1.plot(rk_t, label='Rabin-Karp', color='#e74c3c', marker='x', markersize=3, alpha=0.8)
        ax1.set_title("Biến động thời gian phản hồi")
        ax1.set_ylabel("Giây (s)")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # 2. Biểu đồ hộp (Phân phối độ trễ - Stability)
        bp = ax2.boxplot([kmp_t, rk_t], labels=['KMP', 'Rabin-Karp'], patch_artist=True)
        colors = ['#3498db', '#e74c3c']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)
        ax2.set_title("Phân phối độ trễ (Tính ổn định)")
        ax2.set_ylabel("Giây (s)")
        ax2.grid(True, alpha=0.3)

        fig.suptitle(title, fontsize=14, fontweight='bold')
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])

        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)