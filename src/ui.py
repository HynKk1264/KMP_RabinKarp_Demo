import customtkinter as ctk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import logic từ các module bạn đã tạo
from .kmp import kmp_search
from .rabin_karp import rabin_karp_search
from .utils import run_benchmark, read_text_file

# Cấu hình phong cách
ctk.set_appearance_mode("System")  # Tự động chọn Dark hoặc Light mode theo Windows
ctk.set_default_color_theme("blue") 

class AlgorithmApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PTIT - Phân tích thuật toán KMP & Rabin-Karp")
        self.geometry("1000x800")

        # Cấu hình Layout (Grid)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # 1. Header
        self.label_title = ctk.CTkLabel(self, text="DEMO THUẬT TOÁN TÌM KIẾM CHUỖI", 
                                       font=ctk.CTkFont(size=22, weight="bold"))
        self.label_title.grid(row=0, column=0, padx=20, pady=20)

        # 2. Khung Benchmark (Tự động sinh dữ liệu)
        self.bench_frame = ctk.CTkFrame(self)
        self.bench_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.entry_size = ctk.CTkEntry(self.bench_frame, placeholder_text="Nhập số lượng phần tử (vd: 100000)", width=300)
        self.entry_size.pack(side="left", padx=20, pady=20)

        self.btn_run = ctk.CTkButton(self.bench_frame, text="Chạy Thống Kê 100 Lần", 
                                     fg_color="#2ecc71", hover_color="#27ae60",
                                     command=self.handle_benchmark)
        self.btn_run.pack(side="left", padx=20, pady=20)

        # 3. Khung Tìm kiếm mẫu trên File
        self.file_frame = ctk.CTkFrame(self)
        self.file_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.entry_pattern = ctk.CTkEntry(self.file_frame, placeholder_text="Nhập từ cần tìm...", width=300)
        self.entry_pattern.pack(side="left", padx=20, pady=20)

        self.btn_file = ctk.CTkButton(self.file_frame, text="Chọn File & Tìm Kiếm", 
                                      command=self.handle_file_search)
        self.btn_file.pack(side="left", padx=20, pady=20)

        # 4. Khu vực hiển thị Biểu đồ
        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")
        self.canvas = None

    def handle_benchmark(self):
        try:
            size = int(self.entry_size.get())
            kmp_times, rk_times = run_benchmark(size)
            self.draw_chart(kmp_times, rk_times)
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập một số nguyên hợp lệ!")

    def draw_chart(self, kmp_times, rk_times):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.plot(kmp_times, label='KMP', color='#3498db')
        ax.plot(rk_times, label='Rabin-Karp', color='#e74c3c')
        ax.set_title("So sánh thời gian thực thi")
        ax.set_xlabel("Lần chạy")
        ax.set_ylabel("Thời gian (giây)")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)

        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def handle_file_search(self):
        pattern = self.entry_pattern.get()
        if not pattern:
            messagebox.showwarning("Cảnh báo", "Hãy nhập từ khóa cần tìm trước!")
            return
        
        file_path = filedialog.askopenfilename(filetypes=[("Documents", "*.txt *.pdf")])
        if file_path:
            text = read_text_file(file_path)
            # Chạy thử cả 2 để so sánh vị trí
            res_kmp = kmp_search(text, pattern)
            messagebox.showinfo("Kết quả", f"Tìm thấy {len(res_kmp)} vị trí xuất hiện trong văn bản.")