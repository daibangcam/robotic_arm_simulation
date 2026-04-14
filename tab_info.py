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
        # ================= PHẦN TRÊN: LOGO, INFO, QR =================
        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP, pady=(40, 20))

        # anchor=tk.N giúp các cột luôn dính lên mép trên
        f1 = tk.Frame(top_frame);
        f1.pack(side=tk.LEFT, padx=30, anchor=tk.N)
        f2 = tk.Frame(top_frame);
        f2.pack(side=tk.LEFT, padx=30, anchor=tk.N)
        f3 = tk.Frame(top_frame);
        f3.pack(side=tk.LEFT, padx=30, anchor=tk.N)

        # --- CỘT 1: LOGO ---
        logo = H2Q_Lib.H2Q_get_resource_path("img/_logo.png")
        try:
            if os.path.exists(logo):
                img = Image.open(logo).resize((240, 240), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
                tk.Label(f1, image=self.logo_img).pack()
        except:
            pass

        # --- CỘT 2: THÔNG TIN (Ép cứng font bự để chống lỗi UI) ---
        tk.Label(f2, text="Trần Hoàn", font=("Segoe UI", 36, "bold"), fg="#2c3e50").pack(pady=(0, 15))
        tk.Label(f2, text="Điện thoại: 0978.39.41.43", font=("Segoe UI", 16), fg="#34495e").pack(
            pady=5)
        tk.Label(f2, text="Website: hano.cf", font=("Segoe UI", 16), fg="#34495e").pack(pady=5)
        tk.Label(f2, text="Portfolio: hoantran205.notion.site", font=("Segoe UI", 16), fg="#34495e").pack(pady=5)
        tk.Label(f2, text="Quét mã QR để biết thêm chi tiết :3", font=("Segoe UI", 14, "italic"), fg="#7f8c8d").pack(
            pady=(15, 0))

        # --- CỘT 3: QR ---
        qr = H2Q_Lib.H2Q_get_resource_path("img/_qr.jpg")
        try:
            if os.path.exists(qr):
                img = Image.open(qr).resize((240, 240), Image.Resampling.LANCZOS)
                self.qr_img = ImageTk.PhotoImage(img)
                tk.Label(f3, image=self.qr_img).pack()
        except:
            pass

        # ================= PHẦN DƯỚI: CHANGE LOG (2 CỘT) =================
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=50, pady=(10, 40))

        lf_changelog = ttk.LabelFrame(bottom_frame, text="Change Log", padding="20")
        lf_changelog.pack(fill=tk.BOTH, expand=True)

        # Tạo 2 frame con bên trong để chia cột
        col1 = tk.Frame(lf_changelog)
        col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))

        col2 = tk.Frame(lf_changelog)
        col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))

        # Nội dung cột trái
        changelog_col1 = (
            "• v1 - mô phỏng cánh tay robot RR 2 bậc tự do (Planar 2-DOF).\n\n"
            "• v2 - mô phỏng cánh tay RRR 3 bậc phẳng (Planar 3-DOF).\n\n"
            "• v2.1 - mô phỏng cánh tay RRR không gian (Spatial 3-DOF)."
            "• v2.2 - đánh dấu vùng không gian làm việc của cánh tay RRR.\n\n"
            "• v2.3 - bổ sung chú thích từng loại cánh tay robot.\n\n"
            "• v2.4 - tách riêng Style CSS và code, điều chỉnh UI 2 cột trực quan."
        )

        # Nội dung cột phải
        changelog_col2 = (
            # "• v3.2 - đánh dấu vùng không gian làm việc của cánh tay RRR.\n\n"
            # "• v2.3 - bổ sung chú thích từng loại cánh tay robot.\n\n"
            # "• v2.4 - tách riêng Style CSS và code, điều chỉnh UI 2 cột trực quan."
        )

        # anchor="nw" (North-West) ép chữ dính sát góc trên bên trái
        tk.Label(col1, text=changelog_col1, font=("Segoe UI", 13), justify=tk.LEFT, anchor="nw").pack(fill=tk.BOTH,
                                                                                                      expand=True)
        tk.Label(col2, text=changelog_col2, font=("Segoe UI", 13), justify=tk.LEFT, anchor="nw").pack(fill=tk.BOTH,
                                                                                                      expand=True)