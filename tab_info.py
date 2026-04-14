import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import H2Q_Lib


class TabInfo(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.build_ui()

    def build_ui(self):
        # Container chính
        self.main_frame = ttk.Frame(self, padding="30")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # ================= 1. PROFILE CARD (CỐ ĐỊNH, CĂN GIỮA) =================
        profile_frame = ttk.Frame(self.main_frame)
        profile_frame.pack(fill=tk.X, pady=(10, 30))

        # Khung chứa để ép căn giữa màn hình
        profile_container = tk.Frame(profile_frame)
        profile_container.pack(anchor=tk.CENTER)

        f1 = tk.Frame(profile_container)
        f1.pack(side=tk.LEFT, padx=30, anchor=tk.N)
        f2 = tk.Frame(profile_container)
        f2.pack(side=tk.LEFT, padx=30, anchor=tk.N)
        f3 = tk.Frame(profile_container)
        f3.pack(side=tk.LEFT, padx=30, anchor=tk.N)

        # --- CỘT 1: LOGO ---
        logo = H2Q_Lib.H2Q_get_resource_path("img/_logo.png")
        try:
            if os.path.exists(logo):
                img = Image.open(logo).resize((220, 220), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
                tk.Label(f1, image=self.logo_img).pack()
        except:
            pass

        # --- CỘT 2: THÔNG TIN ---
        tk.Label(f2, text="Trần Hoàn", font=("Segoe UI", 36, "bold"), fg="#1f497d").pack(pady=(0, 15))
        tk.Label(f2, text="Điện thoại: 0978.39.41.43", font=("Segoe UI", 15), fg="#34495e").pack(pady=5)
        tk.Label(f2, text="Website: hano.cf", font=("Segoe UI", 15), fg="#34495e").pack(pady=5)
        tk.Label(f2, text="Portfolio: hoantran205.notion.site", font=("Segoe UI", 15), fg="#34495e").pack(pady=5)
        tk.Label(f2, text="Quét mã QR để biết thêm chi tiết :3", font=("Segoe UI", 13, "italic"), fg="#7f8c8d").pack(
            pady=(15, 0))

        # --- CỘT 3: QR ---
        qr = H2Q_Lib.H2Q_get_resource_path("img/_qr.jpg")
        try:
            if os.path.exists(qr):
                img = Image.open(qr).resize((220, 220), Image.Resampling.LANCZOS)
                self.qr_img = ImageTk.PhotoImage(img)
                tk.Label(f3, image=self.qr_img).pack()
        except:
            pass

        # ================= 2. CHANGE LOG =================
        log_frame = ttk.Frame(self.main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=40)

        lf_changelog = ttk.LabelFrame(log_frame, text="Change Log", padding="5")
        lf_changelog.pack(fill=tk.BOTH, expand=True)

        # --- Tạo Canvas & Scrollbar ---
        canvas = tk.Canvas(lf_changelog, highlightthickness=0)
        scrollbar = ttk.Scrollbar(lf_changelog, orient="vertical", command=canvas.yview)

        # Khung chứa text bên trong Canvas
        inner_frame = ttk.Frame(canvas)

        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_window = canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Ép khung chứa luôn rộng bằng Canvas để text không bị cắt
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_window, width=e.width))

        # ---> xử lý lăn chuột <---
        def _on_mousewheel(e):
            try:
                if not canvas.winfo_ismapped(): return
                cx, cy, cw, ch = canvas.winfo_rootx(), canvas.winfo_rooty(), canvas.winfo_width(), canvas.winfo_height()
                # Chỉ cuộn nếu chuột nằm TRONG ô Change Log
                if cx <= e.x_root <= cx + cw and cy <= e.y_root <= cy + ch:
                    # Chỉ cuộn nếu nội dung text dài hơn chiều cao của ô hiển thị
                    if inner_frame.winfo_reqheight() > ch:
                        canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
            except:
                pass

        canvas.bind_all("<MouseWheel>", _on_mousewheel, add="+")

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Change Log
        changelog_text = (
            "• v1 - mô phỏng cánh tay robot RR 2 bậc phẳng (Planar 2-DOF)\n\n"
            "• v2 - mô phỏng cánh tay RRR 3 bậc phẳng (Planar 3-DOF)\n\n"
            "• v2.1 - mô phỏng cánh tay RRR không gian (Spatial 3-DOF)\n\n"
            "• v2.2 - đánh dấu vùng không gian làm việc của cánh tay RRR\n\n"
            "• v2.3 - bổ sung chú thích từng loại cánh tay robot\n\n"
            "• v2.4 - tách riêng Style CSS và code, điều chỉnh UI\n\n"
            "• v2.5 - bổ sung chỉnh giới hạn các khớp quay giống thực tế\n\n"
            "• v2.6 - mô phỏng cánh tay RR không gian (Spatial 2-DOF)\n\n"
        )

        # Gắn text vào khung chứa
        lbl_log = tk.Label(inner_frame, text=changelog_text, font=("Segoe UI", 13), justify=tk.LEFT, anchor="nw",
                           fg="#2c3e50")
        lbl_log.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)