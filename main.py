import tkinter as tk
from tkinter import ttk
import os
import sys
import H2Q_Lib

# Nhúng các Tab từ các file con vào
from tab_rr import TabRR
from tab_rrr_2d import TabRRR2D
from tab_rrr_3d import TabRRR3D
from tab_info import TabInfo


class H2Q_Multi_Robot_GUI_Final:
    def __init__(self, root):
        self.root = root
        self.root.title("H2Q Lab - Mô phỏng cánh tay Robot v2.4")

        icon_path = H2Q_Lib.H2Q_get_resource_path("img/_icon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(default=icon_path)

        style = ttk.Style()
        # Font chữ của thanh Tab
        style.configure('TNotebook.Tab', font=('Segoe UI', 12, 'bold'), padding=[15, 5])

        # ---> LỆNH MỚI: ÉP FONT CHO TIÊU ĐỀ CỦA LABELFRAME <---
        # Tăng lên size 12, in đậm và cho màu xanh navy cực xịn
        style.configure('TLabelframe.Label', font=('Segoe UI', 12, 'bold'), foreground='#1f497d')

        self.vcmd = (self.root.register(self.validate_number), '%P')
        self.LEFT_WIDTH = 320

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Khởi tạo các Tab dưới dạng Class
        self.tab_rr = TabRR(self.notebook, self.vcmd, self.LEFT_WIDTH)
        self.tab_rrr_2d = TabRRR2D(self.notebook, self.vcmd, self.LEFT_WIDTH)
        self.tab_rrr_3d = TabRRR3D(self.notebook, self.vcmd, self.LEFT_WIDTH)
        self.tab_info = TabInfo(self.notebook)

        # Lắp Tab vào giao diện
        self.notebook.add(self.tab_rr, text="RR")
        self.notebook.add(self.tab_rrr_2d, text="RRR (2D)")
        self.notebook.add(self.tab_rrr_3d, text="RRR (3D)")
        self.notebook.add(self.tab_info, text="Thông tin")

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def validate_number(self, P):
        if P in ["", "-", ".", "-."]: return True
        try:
            float(P)
            return True
        except ValueError:
            return False

    def on_closing(self):
        self.root.quit()
        self.root.destroy()
        sys.exit(0)


if __name__ == '__main__':
    import ctypes

    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('h2qlab.robot.v2.4')
    except Exception:
        pass

    root = tk.Tk()
    root.geometry("1200x1000")

    # Font tổng thể của ứng dụng
    root.option_add("*Font", ("Segoe UI", 12))

    app = H2Q_Multi_Robot_GUI_Final(root)
    root.mainloop()