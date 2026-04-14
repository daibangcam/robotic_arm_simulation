import tkinter as tk
from tkinter import ttk
import os
import sys
import ctypes
import H2Q_Lib

from tab_info import TabInfo
from tab_rr_2d import TabRR2D
from tab_rr_3d import TabRR3D
from tab_rrr_2d import TabRRR2D
from tab_rrr_3d import TabRRR3D



class H2Q_Multi_Robot_GUI_Final:
    def __init__(self, root):
        self.root = root
        self.root.title("H2Q Lab - Mô phỏng cánh tay Robot v2.5")

        icon_path = H2Q_Lib.H2Q_get_resource_path("img/_icon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(default=icon_path)

        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'), padding=[15, 5])
        style.configure('TLabelframe.Label', font=('Segoe UI', 11, 'bold'), foreground='#1f497d')
        style.configure('Desc.TLabel', font=('Segoe UI', 11))

        self.vcmd = (self.root.register(self.validate_number), '%P')
        self.LEFT_WIDTH = 380

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tab_rr_2d = TabRR2D(self.notebook, self.vcmd, self.LEFT_WIDTH)
        self.tab_rr_3d = TabRR3D(self.notebook, self.vcmd, self.LEFT_WIDTH)
        self.tab_rrr_2d = TabRRR2D(self.notebook, self.vcmd, self.LEFT_WIDTH)
        self.tab_rrr_3d = TabRRR3D(self.notebook, self.vcmd, self.LEFT_WIDTH)
        self.tab_info = TabInfo(self.notebook)

        self.notebook.add(self.tab_rr_2d, text="RR (2D)")
        self.notebook.add(self.tab_rr_3d, text="RR (3D)")
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


if __name__ == '__main__':
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('h2qlab.robot.v2.5')
    except Exception:
        pass

    root = tk.Tk()
    root.geometry("1300x950")
    root.option_add("*Font", ("Segoe UI", 11))
    app = H2Q_Multi_Robot_GUI_Final(root)

    root.mainloop()
    sys.exit(0)