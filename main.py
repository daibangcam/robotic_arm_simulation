import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle, Wedge
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from PIL import Image, ImageTk
import os
import sys
import math
import H2Q_Lib


class H2Q_Multi_Robot_GUI_Final:
    def __init__(self, root):
        self.root = root
        self.root.title("H2Q Lab - Mô phỏng cánh tay Robot v2.3")

        icon_path = H2Q_Lib.H2Q_get_resource_path("img/_icon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(default=icon_path)

        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'), padding=[15, 5])
        self.vcmd = (self.root.register(self.H2Q_validate_number), '%P')

        self.LEFT_WIDTH = 270

        # --- BIẾN SỐ RR ---
        self.l1_rr_var = tk.StringVar(value="20.0")
        self.l2_rr_var = tk.StringVar(value="8.0")
        self.t1_rr_var = tk.DoubleVar(value=-20)
        self.t2_rr_var = tk.DoubleVar(value=-63)
        self.x_rr_var = tk.StringVar(value="0.0")
        self.y_rr_var = tk.StringVar(value="0.0")
        self.updating_rr = False

        # --- BIẾN SỐ RRR-1 (2D) ---
        self.l1_rrr_var = tk.StringVar(value="10.0")
        self.l2_rrr_var = tk.StringVar(value="8.0")
        self.l3_rrr_var = tk.StringVar(value="5.0")
        self.t1_rrr_var = tk.DoubleVar(value=30)
        self.t2_rrr_var = tk.DoubleVar(value=-45)
        self.t3_rrr_var = tk.DoubleVar(value=-30)
        self.x_rrr_var = tk.StringVar(value="0.0")
        self.y_rrr_var = tk.StringVar(value="0.0")
        self.phi_rrr_var = tk.StringVar(value="0.0")
        self.updating_rrr = False

        # --- BIẾN SỐ RRR-2 (3D) ---
        self.l1_rrr2_var = tk.StringVar(value="10.0")
        self.l2_rrr2_var = tk.StringVar(value="15.0")
        self.l3_rrr2_var = tk.StringVar(value="10.0")
        self.t1_rrr2_var = tk.DoubleVar(value=45)
        self.t2_rrr2_var = tk.DoubleVar(value=30)
        self.t3_rrr2_var = tk.DoubleVar(value=-60)
        self.x_rrr2_var = tk.StringVar(value="0.0")
        self.y_rrr2_var = tk.StringVar(value="0.0")
        self.z_rrr2_var = tk.StringVar(value="0.0")
        self.updating_rrr2 = False

        self.H2Q_setup_ui()

        # --- GẮN TRACE ---
        self.x_rr_var.trace_add("write", lambda *args: self.H2Q_update_from_coords_rr())
        self.y_rr_var.trace_add("write", lambda *args: self.H2Q_update_from_coords_rr())
        self.l1_rr_var.trace_add("write", lambda *args: self.H2Q_update_from_sliders_rr())
        self.l2_rr_var.trace_add("write", lambda *args: self.H2Q_update_from_sliders_rr())

        self.x_rrr_var.trace_add("write", lambda *args: self.H2Q_update_from_coords_rrr())
        self.y_rrr_var.trace_add("write", lambda *args: self.H2Q_update_from_coords_rrr())
        self.phi_rrr_var.trace_add("write", lambda *args: self.H2Q_update_from_coords_rrr())
        self.l1_rrr_var.trace_add("write", lambda *args: self.H2Q_update_from_sliders_rrr())
        self.l2_rrr_var.trace_add("write", lambda *args: self.H2Q_update_from_sliders_rrr())
        self.l3_rrr_var.trace_add("write", lambda *args: self.H2Q_update_from_sliders_rrr())

        self.x_rrr2_var.trace_add("write", lambda *args: self.H2Q_update_from_coords_rrr2())
        self.y_rrr2_var.trace_add("write", lambda *args: self.H2Q_update_from_coords_rrr2())
        self.z_rrr2_var.trace_add("write", lambda *args: self.H2Q_update_from_coords_rrr2())
        self.l1_rrr2_var.trace_add("write", lambda *args: self.H2Q_update_from_sliders_rrr2())
        self.l2_rrr2_var.trace_add("write", lambda *args: self.H2Q_update_from_sliders_rrr2())
        self.l3_rrr2_var.trace_add("write", lambda *args: self.H2Q_update_from_sliders_rrr2())

        self.H2Q_update_from_sliders_rr()
        self.H2Q_update_from_sliders_rrr()
        self.H2Q_update_from_sliders_rrr2()

        self.root.protocol("WM_DELETE_WINDOW", self.H2Q_on_closing)

    def H2Q_validate_number(self, P):
        if P in ["", "-", ".", "-."]: return True
        try:
            float(P)
            return True
        except ValueError:
            return False

    def H2Q_setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tab_rr = ttk.Frame(self.notebook)
        self.tab_rrr = ttk.Frame(self.notebook)
        self.tab_rrr2 = ttk.Frame(self.notebook)
        self.tab_info = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_rr, text="RR")
        self.notebook.add(self.tab_rrr, text="RRR-1 (2D)")
        self.notebook.add(self.tab_rrr2, text="RRR-2 (3D)")
        self.notebook.add(self.tab_info, text="Thông tin")

        self.H2Q_build_tab_rr()
        self.H2Q_build_tab_rrr()
        self.H2Q_build_tab_rrr2()
        self.H2Q_build_tab_info()

    # ==================== GIAO DIỆN TAB RR ====================
    def H2Q_build_tab_rr(self):
        main_frame = ttk.Frame(self.tab_rr, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        control_frame = ttk.Frame(main_frame, padding="5", width=self.LEFT_WIDTH)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)
        control_frame.pack_propagate(False)

        lf1 = ttk.LabelFrame(control_frame, text="Kích thước robot", padding="5")
        lf1.pack(fill=tk.X, pady=3)
        ttk.Label(lf1, text="Link 1 (cm):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(lf1, textvariable=self.l1_rr_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=0,
                                                                                                              column=1,
                                                                                                              pady=2,
                                                                                                              sticky=tk.E)
        ttk.Label(lf1, text="Link 2 (cm):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(lf1, textvariable=self.l2_rr_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=1,
                                                                                                              column=1,
                                                                                                              pady=2,
                                                                                                              sticky=tk.E)

        lf2 = ttk.LabelFrame(control_frame, text="Động học thuận", padding="5")
        lf2.pack(fill=tk.X, pady=3)
        ttk.Label(lf2, text="Theta 1 (degree):").pack(anchor=tk.W)
        tk.Scale(lf2, from_=-180, to=180, orient=tk.HORIZONTAL, variable=self.t1_rr_var,
                 command=lambda e: self.H2Q_update_from_sliders_rr(), troughcolor='greenyellow').pack(fill=tk.X)
        ttk.Label(lf2, text="Theta 2 (degree):").pack(anchor=tk.W)
        tk.Scale(lf2, from_=-180, to=180, orient=tk.HORIZONTAL, variable=self.t2_rr_var,
                 command=lambda e: self.H2Q_update_from_sliders_rr(), troughcolor='greenyellow').pack(fill=tk.X)

        lf3 = ttk.LabelFrame(control_frame, text="Động học nghịch", padding="5")
        lf3.pack(fill=tk.X, pady=3)
        ttk.Label(lf3, text="Tọa độ X (cm):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(lf3, textvariable=self.x_rr_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=0,
                                                                                                             column=1,
                                                                                                             pady=2,
                                                                                                             sticky=tk.E)
        ttk.Label(lf3, text="Tọa độ Y (cm):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(lf3, textvariable=self.y_rr_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=1,
                                                                                                             column=1,
                                                                                                             pady=2,
                                                                                                             sticky=tk.E)

        lf4 = ttk.LabelFrame(control_frame, text="Chú thích", padding="5")
        lf4.pack(fill=tk.X, pady=3)
        self.lbl_link1_rr = tk.Label(lf4, text="▬ Link 1", fg="blue", font=("Segoe UI", 10, "bold"), anchor="w");
        self.lbl_link1_rr.pack(fill=tk.X)
        self.lbl_link2_rr = tk.Label(lf4, text="▬ Link 2", fg="red", font=("Segoe UI", 10, "bold"), anchor="w");
        self.lbl_link2_rr.pack(fill=tk.X)
        tk.Label(lf4, text="● Gốc tọa độ", fg="green", anchor="w").pack(fill=tk.X)
        tk.Label(lf4, text="○ Vùng làm việc", fg="darkorange", font=("Segoe UI", 10, "bold"), anchor="w").pack(
            fill=tk.X)

        # Thêm phần Mô tả
        lf5 = ttk.LabelFrame(control_frame, text="Mô tả Robot", padding="5")
        lf5.pack(fill=tk.X, pady=3)
        desc_rr = "Cánh tay robot RR 2 bậc tự do (Planar 2-DOF). Ứng dụng phổ biến trong việc định vị mũi công tác tại tọa độ (X, Y) trong không gian làm việc phẳng."
        tk.Label(lf5, text=desc_rr, justify=tk.LEFT, wraplength=240, anchor="w").pack(fill=tk.X)

        self.fig_rr, self.ax_rr = plt.subplots(figsize=(9, 8))
        self.fig_rr.subplots_adjust(left=0.06, right=0.96, top=0.96, bottom=0.06)
        self.canvas_rr = FigureCanvasTkAgg(self.fig_rr, master=main_frame)
        self.canvas_rr.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # ==================== GIAO DIỆN TAB RRR-1 (2D) ====================
    def H2Q_build_tab_rrr(self):
        main_frame = ttk.Frame(self.tab_rrr, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        control_frame = ttk.Frame(main_frame, padding="5", width=self.LEFT_WIDTH)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)
        control_frame.pack_propagate(False)

        lf1 = ttk.LabelFrame(control_frame, text="Kích thước robot", padding="5")
        lf1.pack(fill=tk.X, pady=3)
        ttk.Label(lf1, text="Link 1 (cm):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(lf1, textvariable=self.l1_rrr_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=0,
                                                                                                               column=1,
                                                                                                               pady=1,
                                                                                                               sticky=tk.E)
        ttk.Label(lf1, text="Link 2 (cm):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(lf1, textvariable=self.l2_rrr_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=1,
                                                                                                               column=1,
                                                                                                               pady=1,
                                                                                                               sticky=tk.E)
        ttk.Label(lf1, text="Link 3 (cm):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(lf1, textvariable=self.l3_rrr_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=2,
                                                                                                               column=1,
                                                                                                               pady=1,
                                                                                                               sticky=tk.E)

        lf2 = ttk.LabelFrame(control_frame, text="Động học thuận", padding="5")
        lf2.pack(fill=tk.X, pady=3)
        ttk.Label(lf2, text="Theta 1 (degree):").pack(anchor=tk.W)
        tk.Scale(lf2, from_=-180, to=180, orient=tk.HORIZONTAL, variable=self.t1_rrr_var,
                 command=lambda e: self.H2Q_update_from_sliders_rrr(), troughcolor='greenyellow').pack(fill=tk.X)
        ttk.Label(lf2, text="Theta 2 (degree):").pack(anchor=tk.W)
        tk.Scale(lf2, from_=-180, to=180, orient=tk.HORIZONTAL, variable=self.t2_rrr_var,
                 command=lambda e: self.H2Q_update_from_sliders_rrr(), troughcolor='greenyellow').pack(fill=tk.X)
        ttk.Label(lf2, text="Theta 3 (degree):").pack(anchor=tk.W)
        tk.Scale(lf2, from_=-180, to=180, orient=tk.HORIZONTAL, variable=self.t3_rrr_var,
                 command=lambda e: self.H2Q_update_from_sliders_rrr(), troughcolor='greenyellow').pack(fill=tk.X)

        lf3 = ttk.LabelFrame(control_frame, text="Động học nghịch", padding="5")
        lf3.pack(fill=tk.X, pady=3)
        ttk.Label(lf3, text="Tọa độ X (cm):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(lf3, textvariable=self.x_rrr_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=0,
                                                                                                              column=1,
                                                                                                              pady=1,
                                                                                                              sticky=tk.E)
        ttk.Label(lf3, text="Tọa độ Y (cm):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(lf3, textvariable=self.y_rrr_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=1,
                                                                                                              column=1,
                                                                                                              pady=1,
                                                                                                              sticky=tk.E)
        ttk.Label(lf3, text="Góc Phi (degree):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(lf3, textvariable=self.phi_rrr_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=2,
                                                                                                                column=1,
                                                                                                                pady=1,
                                                                                                                sticky=tk.E)

        lf4 = ttk.LabelFrame(control_frame, text="Chú thích", padding="5")
        lf4.pack(fill=tk.X, pady=3)
        self.lbl_link1_rrr = tk.Label(lf4, text="▬ Link 1", fg="blue", font=("Segoe UI", 10, "bold"), anchor="w");
        self.lbl_link1_rrr.pack(fill=tk.X)
        self.lbl_link2_rrr = tk.Label(lf4, text="▬ Link 2", fg="red", font=("Segoe UI", 10, "bold"), anchor="w");
        self.lbl_link2_rrr.pack(fill=tk.X)
        self.lbl_link3_rrr = tk.Label(lf4, text="▬ Link 3", fg="magenta", font=("Segoe UI", 10, "bold"), anchor="w");
        self.lbl_link3_rrr.pack(fill=tk.X)
        tk.Label(lf4, text="● Gốc tọa độ", fg="green", anchor="w").pack(fill=tk.X)
        tk.Label(lf4, text="○ Vùng làm việc", fg="darkorange", font=("Segoe UI", 10, "bold"), anchor="w").pack(
            fill=tk.X)

        # Thêm phần Mô tả
        lf5 = ttk.LabelFrame(control_frame, text="Mô tả Robot", padding="5")
        lf5.pack(fill=tk.X, pady=3)
        desc_rrr1 = "Cánh tay RRR 3 bậc phẳng (Planar 3-DOF). Có khả năng điều khiển tọa độ (X, Y) và tùy chỉnh được góc nghiêng Phi của đầu công tác. Ứng dụng: Gắp nhả (Pick-and-Place)."
        tk.Label(lf5, text=desc_rrr1, justify=tk.LEFT, wraplength=240, anchor="w").pack(fill=tk.X)

        self.fig_rrr, self.ax_rrr = plt.subplots(figsize=(9, 8))
        self.fig_rrr.subplots_adjust(left=0.06, right=0.96, top=0.96, bottom=0.06)
        self.canvas_rrr = FigureCanvasTkAgg(self.fig_rrr, master=main_frame)
        self.canvas_rrr.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # ==================== GIAO DIỆN TAB RRR-2 (3D) ====================
    def H2Q_build_tab_rrr2(self):
        main_frame = ttk.Frame(self.tab_rrr2, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        control_frame = ttk.Frame(main_frame, padding="5", width=self.LEFT_WIDTH)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)
        control_frame.pack_propagate(False)

        lf1 = ttk.LabelFrame(control_frame, text="Kích thước robot 3D", padding="5")
        lf1.pack(fill=tk.X, pady=3)
        ttk.Label(lf1, text="Trục bệ L1 (cm):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(lf1, textvariable=self.l1_rrr2_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=0,
                                                                                                                column=1,
                                                                                                                pady=1,
                                                                                                                sticky=tk.E)
        ttk.Label(lf1, text="Khớp vai L2 (cm):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(lf1, textvariable=self.l2_rrr2_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=1,
                                                                                                                column=1,
                                                                                                                pady=1,
                                                                                                                sticky=tk.E)
        ttk.Label(lf1, text="Khuỷu tay L3 (cm):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(lf1, textvariable=self.l3_rrr2_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=2,
                                                                                                                column=1,
                                                                                                                pady=1,
                                                                                                                sticky=tk.E)

        lf2 = ttk.LabelFrame(control_frame, text="Động học thuận", padding="5")
        lf2.pack(fill=tk.X, pady=3)
        ttk.Label(lf2, text="Xoay nền T1 (deg):").pack(anchor=tk.W)
        tk.Scale(lf2, from_=-180, to=180, orient=tk.HORIZONTAL, variable=self.t1_rrr2_var,
                 command=lambda e: self.H2Q_update_from_sliders_rrr2(), troughcolor='greenyellow').pack(fill=tk.X)
        ttk.Label(lf2, text="Nâng vai T2 (deg):").pack(anchor=tk.W)
        tk.Scale(lf2, from_=-90, to=90, orient=tk.HORIZONTAL, variable=self.t2_rrr2_var,
                 command=lambda e: self.H2Q_update_from_sliders_rrr2(), troughcolor='greenyellow').pack(fill=tk.X)
        ttk.Label(lf2, text="Gập khuỷu T3 (deg):").pack(anchor=tk.W)
        tk.Scale(lf2, from_=-180, to=180, orient=tk.HORIZONTAL, variable=self.t3_rrr2_var,
                 command=lambda e: self.H2Q_update_from_sliders_rrr2(), troughcolor='greenyellow').pack(fill=tk.X)

        lf3 = ttk.LabelFrame(control_frame, text="Động học nghịch", padding="5")
        lf3.pack(fill=tk.X, pady=3)
        ttk.Label(lf3, text="Tọa độ X (cm):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(lf3, textvariable=self.x_rrr2_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=0,
                                                                                                               column=1,
                                                                                                               pady=1,
                                                                                                               sticky=tk.E)
        ttk.Label(lf3, text="Tọa độ Y (cm):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(lf3, textvariable=self.y_rrr2_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=1,
                                                                                                               column=1,
                                                                                                               pady=1,
                                                                                                               sticky=tk.E)
        ttk.Label(lf3, text="Tọa độ Z (cm):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(lf3, textvariable=self.z_rrr2_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=2,
                                                                                                               column=1,
                                                                                                               pady=1,
                                                                                                               sticky=tk.E)

        lf4 = ttk.LabelFrame(control_frame, text="Chú thích", padding="5")
        lf4.pack(fill=tk.X, pady=3)
        tk.Label(lf4, text="▬ Trục bệ (Base)", fg="blue", font=("Segoe UI", 10, "bold"), anchor="w").pack(fill=tk.X)
        tk.Label(lf4, text="▬ Khớp vai (Shoulder)", fg="red", font=("Segoe UI", 10, "bold"), anchor="w").pack(fill=tk.X)
        tk.Label(lf4, text="▬ Khuỷu tay (Elbow)", fg="magenta", font=("Segoe UI", 10, "bold"), anchor="w").pack(
            fill=tk.X)
        tk.Label(lf4, text="○ Vùng làm việc (Khối cầu)", fg="darkorange", font=("Segoe UI", 10, "bold"),
                 anchor="w").pack(fill=tk.X)

        # Thêm phần Mô tả
        lf5 = ttk.LabelFrame(control_frame, text="Mô tả Robot", padding="5")
        lf5.pack(fill=tk.X, pady=3)
        desc_rrr2 = "Cánh tay RRR không gian (Spatial 3-DOF). Cơ cấu tương đương robot công nghiệp (như hàn, sơn). Khớp 1 xoay nền, khớp 2 và 3 nâng gập cánh tay trong không gian 3D."
        tk.Label(lf5, text=desc_rrr2, justify=tk.LEFT, wraplength=240, anchor="w").pack(fill=tk.X)

        self.fig_rrr2 = plt.figure(figsize=(9, 8))
        self.ax_rrr2 = self.fig_rrr2.add_subplot(111, projection='3d')
        self.fig_rrr2.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.canvas_rrr2 = FigureCanvasTkAgg(self.fig_rrr2, master=main_frame)
        self.canvas_rrr2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # ==================== GIAO DIỆN TAB THÔNG TIN ====================
    def H2Q_build_tab_info(self):
        main_info_frame = tk.Frame(self.tab_info)
        main_info_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        f1 = tk.Frame(main_info_frame);
        f1.pack(side=tk.LEFT, padx=30)
        f2 = tk.Frame(main_info_frame);
        f2.pack(side=tk.LEFT, padx=30)
        f3 = tk.Frame(main_info_frame);
        f3.pack(side=tk.LEFT, padx=30)

        logo = H2Q_Lib.H2Q_get_resource_path("img/_logo.png")
        try:
            if os.path.exists(logo):
                img = Image.open(logo).resize((240, 240), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
                tk.Label(f1, image=self.logo_img).pack()
        except:
            pass

        tk.Label(f2, text="Trần Hoàn", font=("Segoe UI", 36, "bold"), fg="#2c3e50").pack(pady=(0, 15))
        tk.Label(f2, text="Điện thoại: 0978.39.41.43 (Telegram/Whatsapp)", font=("Segoe UI", 16), fg="#34495e").pack(
            pady=5)
        tk.Label(f2, text="Website: hano.cf", font=("Segoe UI", 16), fg="#34495e").pack(pady=5)
        tk.Label(f2, text="Homepage: hoantran205.notion.site", font=("Segoe UI", 16), fg="#34495e").pack(pady=5)
        tk.Label(f2, text="Quét mã QR để biết thêm chi tiết :3", font=("Segoe UI", 14, "italic"), fg="#7f8c8d").pack(
            pady=(15, 0))

        qr = H2Q_Lib.H2Q_get_resource_path("img/_qr.jpg")
        try:
            if os.path.exists(qr):
                img = Image.open(qr).resize((240, 240), Image.Resampling.LANCZOS)
                self.qr_img = ImageTk.PhotoImage(img)
                tk.Label(f3, image=self.qr_img).pack()
        except:
            pass

    # ==================== CÁC HÀM VẼ ĐỒ THỊ ====================
    def H2Q_draw_robot_rr(self, t1, t2):
        self.ax_rr.clear()
        try:
            L1, L2 = float(self.l1_rr_var.get()), float(self.l2_rr_var.get())
        except ValueError:
            return 0, 0

        self.lbl_link1_rr.config(text=f"▬ Link 1 ({L1} cm)")
        self.lbl_link2_rr.config(text=f"▬ Link 2 ({L2} cm)")
        r_max, r_min = L1 + L2, abs(L1 - L2)

        self.ax_rr.set_facecolor('orange')
        self.ax_rr.add_patch(Wedge((0, 0), r_max, 0, 360, facecolor='white'))
        if r_min > 0.1:
            self.ax_rr.add_patch(Circle((0, 0), r_min, color='orange'))

        x0, y0, x1, y1, x2, y2 = H2Q_Lib.H2Q_RR_Forward_Kinematics(L1, L2, t1, t2)

        self.ax_rr.plot([x0, x1], [y0, y1], color='blue', lw=7)
        self.ax_rr.plot([x1, x2], [y1, y2], color='red', lw=7)
        self.ax_rr.plot(x0, y0, 'o', color='green', ms=14)
        self.ax_rr.plot(x1, y1, 'ko', ms=8)
        self.ax_rr.plot(x2, y2, '*', color='yellow', ms=25, mec='goldenrod')

        lim = r_max + 2
        self.ax_rr.set(xlim=(-lim, lim), ylim=(-lim, lim), aspect='equal')
        self.ax_rr.grid(ls=':', alpha=0.6)
        self.canvas_rr.draw()

        return x2, y2

    def H2Q_draw_robot_rrr(self, t1, t2, t3):
        self.ax_rrr.clear()
        try:
            L1, L2, L3 = float(self.l1_rrr_var.get()), float(self.l2_rrr_var.get()), float(self.l3_rrr_var.get())
        except ValueError:
            return 0, 0, 0

        self.lbl_link1_rrr.config(text=f"▬ Link 1 ({L1} cm)")
        self.lbl_link2_rrr.config(text=f"▬ Link 2 ({L2} cm)")
        self.lbl_link3_rrr.config(text=f"▬ Link 3 ({L3} cm)")
        r_max = L1 + L2 + L3
        r_min = max(0, L1 - L2 - L3, L2 - L1 - L3, L3 - L1 - L2)

        self.ax_rrr.set_facecolor('orange')
        self.ax_rrr.add_patch(Wedge((0, 0), r_max, 0, 360, facecolor='white'))
        if r_min > 0.1:
            self.ax_rrr.add_patch(Circle((0, 0), r_min, color='orange'))

        x0, y0, x1, y1, x2, y2, x3, y3, phi = H2Q_Lib.H2Q_RRR_Forward_Kinematics(L1, L2, L3, t1, t2, t3)

        self.ax_rrr.plot([x0, x1], [y0, y1], color='blue', lw=7)
        self.ax_rrr.plot([x1, x2], [y1, y2], color='red', lw=7)
        self.ax_rrr.plot([x2, x3], [y2, y3], color='magenta', lw=7)
        self.ax_rrr.plot(x0, y0, 'o', color='green', ms=14)
        self.ax_rrr.plot(x1, y1, 'ko', ms=8)
        self.ax_rrr.plot(x2, y2, 'ko', ms=8)
        self.ax_rrr.plot(x3, y3, '*', color='yellow', ms=25, mec='goldenrod')

        lim = r_max + 2
        self.ax_rrr.set(xlim=(-lim, lim), ylim=(-lim, lim), aspect='equal')
        self.ax_rrr.grid(ls=':', alpha=0.6)
        self.canvas_rrr.draw()

        return x3, y3, math.degrees(phi)

    def H2Q_draw_robot_rrr2(self, t1, t2, t3):
        self.ax_rrr2.clear()
        try:
            L1, L2, L3 = float(self.l1_rrr2_var.get()), float(self.l2_rrr2_var.get()), float(self.l3_rrr2_var.get())
        except ValueError:
            return 0, 0, 0

        p0, p1, p2, p3 = H2Q_Lib.H2Q_RRR_3D_Forward_Kinematics(L1, L2, L3, t1, t2, t3)

        # --- LƯỚI KHỐI CẦU ---
        R_max = L2 + L3
        u = np.linspace(0, 2 * np.pi, 30)
        v = np.linspace(0, np.pi, 30)
        X_sphere = R_max * np.outer(np.cos(u), np.sin(v))
        Y_sphere = R_max * np.outer(np.sin(u), np.sin(v))
        Z_sphere = L1 + R_max * np.outer(np.ones(np.size(u)), np.cos(v))
        self.ax_rrr2.plot_surface(X_sphere, Y_sphere, Z_sphere, color='orange', alpha=0.15, edgecolor='none')
        # ---------------------

        self.ax_rrr2.plot([p0[0], p1[0]], [p0[1], p1[1]], [p0[2], p1[2]], color='blue', lw=7)
        self.ax_rrr2.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color='red', lw=7)
        self.ax_rrr2.plot([p2[0], p3[0]], [p2[1], p3[1]], [p2[2], p3[2]], color='magenta', lw=7)

        self.ax_rrr2.scatter([p0[0], p1[0], p2[0]], [p0[1], p1[1], p2[1]], [p0[2], p1[2], p2[2]], color='green', s=100)
        self.ax_rrr2.scatter([p3[0]], [p3[1]], [p3[2]], color='yellow', s=300, marker='*', edgecolors='goldenrod')

        limit = L1 + L2 + L3
        self.ax_rrr2.set_xlim([-limit, limit])
        self.ax_rrr2.set_ylim([-limit, limit])
        self.ax_rrr2.set_zlim([0, limit])
        self.ax_rrr2.set_xlabel('Trục X (cm)')
        self.ax_rrr2.set_ylabel('Trục Y (cm)')
        self.ax_rrr2.set_zlabel('Trục Z (cm)')

        self.canvas_rrr2.draw()
        return p3[0], p3[1], p3[2]

    # ==================== CÁC HÀM XỬ LÝ (UPDATE) ====================
    def H2Q_update_from_sliders_rr(self):
        if self.updating_rr: return
        self.updating_rr = True
        try:
            x, y = self.H2Q_draw_robot_rr(self.t1_rr_var.get(), self.t2_rr_var.get())
            self.x_rr_var.set(f"{x:.3f}")
            self.y_rr_var.set(f"{y:.3f}")
        finally:
            self.updating_rr = False

    def H2Q_update_from_coords_rr(self):
        if self.updating_rr: return
        self.updating_rr = True
        try:
            L1, L2 = float(self.l1_rr_var.get()), float(self.l2_rr_var.get())
            t1, t2 = H2Q_Lib.H2Q_RR_Inverse_Kinematics(L1, L2, float(self.x_rr_var.get()), float(self.y_rr_var.get()))
            if t1 is not None:
                self.t1_rr_var.set(round(t1, 1))
                self.t2_rr_var.set(round(t2, 1))
                self.H2Q_draw_robot_rr(t1, t2)
        except ValueError:
            pass
        finally:
            self.updating_rr = False

    def H2Q_update_from_sliders_rrr(self):
        if self.updating_rrr: return
        self.updating_rrr = True
        try:
            x, y, phi = self.H2Q_draw_robot_rrr(self.t1_rrr_var.get(), self.t2_rrr_var.get(), self.t3_rrr_var.get())
            self.x_rrr_var.set(f"{x:.3f}")
            self.y_rrr_var.set(f"{y:.3f}")
            self.phi_rrr_var.set(f"{phi:.1f}")
        finally:
            self.updating_rrr = False

    def H2Q_update_from_coords_rrr(self):
        if self.updating_rrr: return
        self.updating_rrr = True
        try:
            L1, L2, L3 = float(self.l1_rrr_var.get()), float(self.l2_rrr_var.get()), float(self.l3_rrr_var.get())
            t1, t2, t3 = H2Q_Lib.H2Q_RRR_Inverse_Kinematics(L1, L2, L3, float(self.x_rrr_var.get()),
                                                            float(self.y_rrr_var.get()), float(self.phi_rrr_var.get()))
            if t1 is not None:
                self.t1_rrr_var.set(round(t1, 1))
                self.t2_rrr_var.set(round(t2, 1))
                self.t3_rrr_var.set(round(t3, 1))
                self.H2Q_draw_robot_rrr(t1, t2, t3)
        except ValueError:
            pass
        finally:
            self.updating_rrr = False

    def H2Q_update_from_sliders_rrr2(self):
        if self.updating_rrr2: return
        self.updating_rrr2 = True
        try:
            x, y, z = self.H2Q_draw_robot_rrr2(self.t1_rrr2_var.get(), self.t2_rrr2_var.get(), self.t3_rrr2_var.get())
            self.x_rrr2_var.set(f"{x:.3f}")
            self.y_rrr2_var.set(f"{y:.3f}")
            self.z_rrr2_var.set(f"{z:.3f}")
        except ValueError:
            pass
        finally:
            self.updating_rrr2 = False

    def H2Q_update_from_coords_rrr2(self):
        if self.updating_rrr2: return
        self.updating_rrr2 = True
        try:
            L1, L2, L3 = float(self.l1_rrr2_var.get()), float(self.l2_rrr2_var.get()), float(self.l3_rrr2_var.get())
            X, Y, Z = float(self.x_rrr2_var.get()), float(self.y_rrr2_var.get()), float(self.z_rrr2_var.get())
            t1, t2, t3 = H2Q_Lib.H2Q_RRR_3D_Inverse_Kinematics(L1, L2, L3, X, Y, Z)

            if t1 is not None and t2 is not None and t3 is not None:
                self.t1_rrr2_var.set(round(t1, 1))
                self.t2_rrr2_var.set(round(t2, 1))
                self.t3_rrr2_var.set(round(t3, 1))
                self.H2Q_draw_robot_rrr2(t1, t2, t3)
        except ValueError:
            pass
        finally:
            self.updating_rrr2 = False

    def H2Q_on_closing(self):
        self.root.quit()
        self.root.destroy()
        sys.exit(0)


if __name__ == '__main__':
    import ctypes

    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('h2qlab.robot.v2.1')
    except Exception:
        pass

    root = tk.Tk()
    root.geometry("1150x860")
    root.option_add("*Font", ("Segoe UI", 10))
    app = H2Q_Multi_Robot_GUI_Final(root)
    root.mainloop()