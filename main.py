import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle, Wedge
from PIL import Image, ImageTk
import os
import sys
import math
import H2Q_Lib

class H2Q_Multi_Robot_GUI_Final:
    def __init__(self, root):
        self.root = root
        self.root.title("H2Q Lab - Mô phỏng cánh tay Robot v2")

        icon_path = H2Q_Lib.H2Q_get_resource_path("img/_icon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(default=icon_path)

        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'), padding=[15, 5])

        self.vcmd = (self.root.register(self.H2Q_validate_number), '%P')

        self.l1_rr_var = tk.StringVar(value="20.0")
        self.l2_rr_var = tk.StringVar(value="8.0")
        self.t1_rr_var = tk.DoubleVar(value=-20)
        self.t2_rr_var = tk.DoubleVar(value=-63)
        self.x_rr_var = tk.StringVar(value="0.0")
        self.y_rr_var = tk.StringVar(value="0.0")
        self.updating_rr = False

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

        self.H2Q_setup_ui()

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

        self.H2Q_update_from_sliders_rr()
        self.H2Q_update_from_sliders_rrr()

        self.root.protocol("WM_DELETE_WINDOW", self.H2Q_on_closing)

    def H2Q_validate_number(self, P):
        if P in ["", "-", ".", "-."]:
            return True
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
        self.tab_info = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_rr, text="RR")
        self.notebook.add(self.tab_rrr, text="RRR")
        self.notebook.add(self.tab_info, text="Thông tin")

        self.H2Q_build_tab_rr()
        self.H2Q_build_tab_rrr()
        self.H2Q_build_tab_info()

    def H2Q_build_tab_rr(self):
        main_frame = ttk.Frame(self.tab_rr, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        control_frame = ttk.Frame(main_frame, padding="5")
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        link_frame = ttk.LabelFrame(control_frame, text="Kích thước robot", padding="10")
        link_frame.pack(fill=tk.X, pady=5)
        ttk.Label(link_frame, text="Link 1 (cm):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(link_frame, textvariable=self.l1_rr_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=0, column=1, pady=2)
        ttk.Label(link_frame, text="Link 2 (cm):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(link_frame, textvariable=self.l2_rr_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=1, column=1, pady=2)

        fk_frame = ttk.LabelFrame(control_frame, text="Động học thuận", padding="10")
        fk_frame.pack(fill=tk.X, pady=5)
        ttk.Label(fk_frame, text="Theta 1 (degree):").pack(anchor=tk.W)
        self.s1_rr = tk.Scale(fk_frame, from_=-180, to=180, orient=tk.HORIZONTAL,
                              variable=self.t1_rr_var, command=lambda e: self.H2Q_update_from_sliders_rr(),
                              troughcolor='greenyellow', activebackground='lawngreen')
        self.s1_rr.pack(fill=tk.X)
        ttk.Label(fk_frame, text="Theta 2 (degree):").pack(anchor=tk.W)
        self.s2_rr = tk.Scale(fk_frame, from_=-180, to=180, orient=tk.HORIZONTAL,
                              variable=self.t2_rr_var, command=lambda e: self.H2Q_update_from_sliders_rr(),
                              troughcolor='greenyellow', activebackground='lawngreen')
        self.s2_rr.pack(fill=tk.X)

        ik_frame = ttk.LabelFrame(control_frame, text="Động học nghịch", padding="10")
        ik_frame.pack(fill=tk.X, pady=5)
        ttk.Label(ik_frame, text="Tọa độ X (cm):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(ik_frame, textvariable=self.x_rr_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=0, column=1, pady=2)
        ttk.Label(ik_frame, text="Tọa độ Y (cm):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(ik_frame, textvariable=self.y_rr_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=1, column=1, pady=2)

        legend_frame = ttk.LabelFrame(control_frame, text="Chú thích", padding="10")
        legend_frame.pack(fill=tk.X, pady=5)
        self.lbl_link1_rr = tk.Label(legend_frame, text="▬ Link 1 (10.0 cm)", fg="blue", font=("Segoe UI", 10, "bold"),
                                     anchor="w")
        self.lbl_link1_rr.pack(fill=tk.X, pady=2)
        self.lbl_link2_rr = tk.Label(legend_frame, text="▬ Link 2 (8.0 cm)", fg="red", font=("Segoe UI", 10, "bold"),
                                     anchor="w")
        self.lbl_link2_rr.pack(fill=tk.X, pady=2)
        tk.Label(legend_frame, text="● Gốc tọa độ", fg="green", font=("Segoe UI", 10), anchor="w").pack(fill=tk.X,
                                                                                                        pady=2)
        tk.Label(legend_frame, text="★ Đầu công tác", fg="#DAA520", font=("Segoe UI", 10, "bold"), anchor="w").pack(
            fill=tk.X, pady=2)
        tk.Label(legend_frame, text="○ Vùng làm việc", fg="darkorange", font=("Segoe UI", 10, "bold"), anchor="w").pack(
            fill=tk.X, pady=2)

        self.fig_rr, self.ax_rr = plt.subplots(figsize=(9, 8))
        self.fig_rr.subplots_adjust(left=0.06, right=0.96, top=0.96, bottom=0.06)
        self.canvas_rr = FigureCanvasTkAgg(self.fig_rr, master=main_frame)
        self.canvas_rr.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def H2Q_build_tab_rrr(self):
        main_frame = ttk.Frame(self.tab_rrr, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        control_frame = ttk.Frame(main_frame, padding="5")
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        link_frame = ttk.LabelFrame(control_frame, text="Kích thước robot", padding="5")
        link_frame.pack(fill=tk.X, pady=3)
        ttk.Label(link_frame, text="Link 1 (cm):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(link_frame, textvariable=self.l1_rrr_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=0, column=1, pady=1)
        ttk.Label(link_frame, text="Link 2 (cm):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(link_frame, textvariable=self.l2_rrr_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=1, column=1, pady=1)
        ttk.Label(link_frame, text="Link 3 (cm):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(link_frame, textvariable=self.l3_rrr_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=2, column=1, pady=1)

        fk_frame = ttk.LabelFrame(control_frame, text="Động học thuận", padding="5")
        fk_frame.pack(fill=tk.X, pady=3)
        ttk.Label(fk_frame, text="Theta 1 (degree):").pack(anchor=tk.W)
        self.s1_rrr = tk.Scale(fk_frame, from_=-180, to=180, orient=tk.HORIZONTAL,
                               variable=self.t1_rrr_var, command=lambda e: self.H2Q_update_from_sliders_rrr(),
                               troughcolor='greenyellow', activebackground='lawngreen')
        self.s1_rrr.pack(fill=tk.X)
        ttk.Label(fk_frame, text="Theta 2 (degree):").pack(anchor=tk.W)
        self.s2_rrr = tk.Scale(fk_frame, from_=-180, to=180, orient=tk.HORIZONTAL,
                               variable=self.t2_rrr_var, command=lambda e: self.H2Q_update_from_sliders_rrr(),
                               troughcolor='greenyellow', activebackground='lawngreen')
        self.s2_rrr.pack(fill=tk.X)
        ttk.Label(fk_frame, text="Theta 3 (degree):").pack(anchor=tk.W)
        self.s3_rrr = tk.Scale(fk_frame, from_=-180, to=180, orient=tk.HORIZONTAL,
                               variable=self.t3_rrr_var, command=lambda e: self.H2Q_update_from_sliders_rrr(),
                               troughcolor='greenyellow', activebackground='lawngreen')
        self.s3_rrr.pack(fill=tk.X)

        ik_frame = ttk.LabelFrame(control_frame, text="Động học nghịch", padding="5")
        ik_frame.pack(fill=tk.X, pady=3)
        ttk.Label(ik_frame, text="Tọa độ X (cm):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(ik_frame, textvariable=self.x_rrr_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=0, column=1, pady=1)
        ttk.Label(ik_frame, text="Tọa độ Y (cm):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(ik_frame, textvariable=self.y_rrr_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=1, column=1, pady=1)
        ttk.Label(ik_frame, text="Góc Phi (degree):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(ik_frame, textvariable=self.phi_rrr_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=2, column=1, pady=1)

        legend_frame = ttk.LabelFrame(control_frame, text="Chú thích", padding="5")
        legend_frame.pack(fill=tk.X, pady=3)
        self.lbl_link1_rrr = tk.Label(legend_frame, text="▬ Link 1 (10.0 cm)", fg="blue", font=("Segoe UI", 10, "bold"),
                                      anchor="w")
        self.lbl_link1_rrr.pack(fill=tk.X, pady=1)
        self.lbl_link2_rrr = tk.Label(legend_frame, text="▬ Link 2 (8.0 cm)", fg="red", font=("Segoe UI", 10, "bold"),
                                      anchor="w")
        self.lbl_link2_rrr.pack(fill=tk.X, pady=1)
        self.lbl_link3_rrr = tk.Label(legend_frame, text="▬ Link 3 (5.0 cm)", fg="magenta",
                                      font=("Segoe UI", 10, "bold"), anchor="w")
        self.lbl_link3_rrr.pack(fill=tk.X, pady=1)
        tk.Label(legend_frame, text="● Gốc tọa độ", fg="green", font=("Segoe UI", 10), anchor="w").pack(fill=tk.X,
                                                                                                        pady=1)
        tk.Label(legend_frame, text="★ Đầu công tác", fg="#DAA520", font=("Segoe UI", 10, "bold"), anchor="w").pack(
            fill=tk.X, pady=1)
        tk.Label(legend_frame, text="○ Vùng làm việc", fg="darkorange", font=("Segoe UI", 10, "bold"), anchor="w").pack(
            fill=tk.X, pady=1)

        self.fig_rrr, self.ax_rrr = plt.subplots(figsize=(9, 8))
        self.fig_rrr.subplots_adjust(left=0.06, right=0.96, top=0.96, bottom=0.06)
        self.canvas_rrr = FigureCanvasTkAgg(self.fig_rrr, master=main_frame)
        self.canvas_rrr.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def H2Q_build_tab_info(self):
        main_info_frame = tk.Frame(self.tab_info)
        main_info_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        left_frame = tk.Frame(main_info_frame)
        left_frame.pack(side=tk.LEFT, padx=30)

        center_text_frame = tk.Frame(main_info_frame)
        center_text_frame.pack(side=tk.LEFT, padx=30)

        right_frame = tk.Frame(main_info_frame)
        right_frame.pack(side=tk.LEFT, padx=30)

        logo_filename = H2Q_Lib.H2Q_get_resource_path("img/_logo.png")
        try:
            if os.path.exists(logo_filename):
                img_logo = Image.open(logo_filename)
                img_logo = img_logo.resize((240, 240), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img_logo)
                lbl_logo = tk.Label(left_frame, image=self.logo_img)
                lbl_logo.pack()
            else:
                lbl_logo = tk.Label(left_frame, text="[_logo.png]", bg="lightgray", fg="gray", width=30, height=15)
                lbl_logo.pack()
        except Exception:
            pass

        tk.Label(center_text_frame, text="Trần Hoàn", font=("Segoe UI", 36, "bold"), fg="#2c3e50").pack(pady=(0, 15))
        tk.Label(center_text_frame, text="Điện thoại: 0978.39.41.43 (Telegram/Whatsapp)", font=("Segoe UI", 16),
                 fg="#34495e").pack(pady=5)
        tk.Label(center_text_frame, text="Website: hano.cf", font=("Segoe UI", 16), fg="#34495e").pack(pady=5)
        tk.Label(center_text_frame, text="Homepage: hoantran205.notion.site", font=("Segoe UI", 16), fg="#34495e").pack(
            pady=5)
        tk.Label(center_text_frame, text="Muốn biết nhiều hơn thì quét mã QR kế bên này nha :3",
                 font=("Segoe UI", 14, "italic"), fg="#7f8c8d").pack(pady=(15, 0))

        qr_filename = H2Q_Lib.H2Q_get_resource_path("img/_qr.jpg")
        try:
            if os.path.exists(qr_filename):
                img_qr = Image.open(qr_filename)
                img_qr = img_qr.resize((240, 240), Image.Resampling.LANCZOS)
                self.qr_img = ImageTk.PhotoImage(img_qr)
                lbl_qr = tk.Label(right_frame, image=self.qr_img)
                lbl_qr.pack()
            else:
                lbl_qr = tk.Label(right_frame, text="[_qr.jpg]", bg="lightgray", fg="gray", width=30, height=15)
                lbl_qr.pack()
        except Exception:
            pass

    def H2Q_draw_robot_rr(self, th1_deg, th2_deg):
        self.ax_rr.clear()
        try:
            L1 = float(self.l1_rr_var.get())
            L2 = float(self.l2_rr_var.get())
            self.lbl_link1_rr.config(text=f"▬ Link 1 ({L1} cm)")
            self.lbl_link2_rr.config(text=f"▬ Link 2 ({L2} cm)")
        except ValueError:
            return 0, 0

        R_max = L1 + L2
        R_min = abs(L1 - L2)

        self.ax_rr.set_facecolor('orange')
        white_workspace = Wedge((0, 0), R_max, 0, 360, facecolor='white', edgecolor='none')
        self.ax_rr.add_patch(white_workspace)

        if R_min > 0.1:
            orange_center = Circle((0, 0), R_min, color='orange', fill=True)
            self.ax_rr.add_patch(orange_center)

        x0, y0, x1, y1, x2, y2 = H2Q_Lib.H2Q_RR_Forward_Kinematics(L1, L2, th1_deg, th2_deg)

        self.ax_rr.plot([x0, x1], [y0, y1], color='blue', linewidth=7)
        self.ax_rr.plot([x1, x2], [y1, y2], color='red', linewidth=7)
        self.ax_rr.plot(x0, y0, 'o', color='green', markersize=14)
        self.ax_rr.plot(x1, y1, 'ko', markersize=8)
        self.ax_rr.plot(x2, y2, '*', color='yellow', markersize=25, markeredgecolor='goldenrod')

        limit = R_max + 2
        self.ax_rr.set_xlim(-limit, limit)
        self.ax_rr.set_ylim(-limit, limit)
        self.ax_rr.grid(True, linestyle=':', alpha=0.6)
        self.ax_rr.set_aspect('equal')

        self.canvas_rr.draw()
        return x2, y2

    def H2Q_draw_robot_rrr(self, th1_deg, th2_deg, th3_deg):
        self.ax_rrr.clear()
        try:
            L1 = float(self.l1_rrr_var.get())
            L2 = float(self.l2_rrr_var.get())
            L3 = float(self.l3_rrr_var.get())
            self.lbl_link1_rrr.config(text=f"▬ Link 1 ({L1} cm)")
            self.lbl_link2_rrr.config(text=f"▬ Link 2 ({L2} cm)")
            self.lbl_link3_rrr.config(text=f"▬ Link 3 ({L3} cm)")
        except ValueError:
            return 0, 0, 0

        R_max = L1 + L2 + L3
        R_min = max(0, L1 - L2 - L3, L2 - L1 - L3, L3 - L1 - L2)

        self.ax_rrr.set_facecolor('orange')
        white_workspace = Wedge((0, 0), R_max, 0, 360, facecolor='white', edgecolor='none')
        self.ax_rrr.add_patch(white_workspace)

        if R_min > 0.1:
            orange_center = Circle((0, 0), R_min, color='orange', fill=True)
            self.ax_rrr.add_patch(orange_center)

        x0, y0, x1, y1, x2, y2, x3, y3, phi_rad = H2Q_Lib.H2Q_RRR_Forward_Kinematics(L1, L2, L3, th1_deg, th2_deg, th3_deg)

        self.ax_rrr.plot([x0, x1], [y0, y1], color='blue', linewidth=7)
        self.ax_rrr.plot([x1, x2], [y1, y2], color='red', linewidth=7)
        self.ax_rrr.plot([x2, x3], [y2, y3], color='magenta', linewidth=7)

        self.ax_rrr.plot(x0, y0, 'o', color='green', markersize=14)
        self.ax_rrr.plot(x1, y1, 'ko', markersize=8)
        self.ax_rrr.plot(x2, y2, 'ko', markersize=8)
        self.ax_rrr.plot(x3, y3, '*', color='yellow', markersize=25, markeredgecolor='goldenrod')

        limit = R_max + 2
        self.ax_rrr.set_xlim(-limit, limit)
        self.ax_rrr.set_ylim(-limit, limit)
        self.ax_rrr.grid(True, linestyle=':', alpha=0.6)
        self.ax_rrr.set_aspect('equal')

        self.canvas_rrr.draw()
        return x3, y3, math.degrees(phi_rad)

    def H2Q_update_from_sliders_rr(self):
        if getattr(self, 'updating_rr', False): return
        self.updating_rr = True
        try:
            t1 = self.t1_rr_var.get()
            t2 = self.t2_rr_var.get()
            x, y = self.H2Q_draw_robot_rr(t1, t2)
            self.x_rr_var.set(f"{x:.3f}")
            self.y_rr_var.set(f"{y:.3f}")
        finally:
            self.updating_rr = False

    def H2Q_update_from_coords_rr(self):
        if getattr(self, 'updating_rr', False): return
        self.updating_rr = True
        try:
            x = float(self.x_rr_var.get())
            y = float(self.y_rr_var.get())
            L1 = float(self.l1_rr_var.get())
            L2 = float(self.l2_rr_var.get())

            t1_deg, t2_deg = H2Q_Lib.H2Q_RR_Inverse_Kinematics(L1, L2, x, y)

            if t1_deg is not None and t2_deg is not None:
                self.t1_rr_var.set(round(t1_deg, 1))
                self.t2_rr_var.set(round(t2_deg, 1))
                self.H2Q_draw_robot_rr(t1_deg, t2_deg)
        except (ValueError, ZeroDivisionError):
            pass
        finally:
            self.updating_rr = False

    def H2Q_update_from_sliders_rrr(self):
        if getattr(self, 'updating_rrr', False): return
        self.updating_rrr = True
        try:
            t1 = self.t1_rrr_var.get()
            t2 = self.t2_rrr_var.get()
            t3 = self.t3_rrr_var.get()
            x, y, phi = self.H2Q_draw_robot_rrr(t1, t2, t3)

            self.x_rrr_var.set(f"{x:.3f}")
            self.y_rrr_var.set(f"{y:.3f}")
            self.phi_rrr_var.set(f"{phi:.1f}")
        finally:
            self.updating_rrr = False

    def H2Q_update_from_coords_rrr(self):
        if getattr(self, 'updating_rrr', False): return
        self.updating_rrr = True
        try:
            x = float(self.x_rrr_var.get())
            y = float(self.y_rrr_var.get())
            phi_deg = float(self.phi_rrr_var.get())
            L1 = float(self.l1_rrr_var.get())
            L2 = float(self.l2_rrr_var.get())
            L3 = float(self.l3_rrr_var.get())

            t1_deg, t2_deg, t3_deg = H2Q_Lib.H2Q_RRR_Inverse_Kinematics(L1, L2, L3, x, y, phi_deg)

            if t1_deg is not None and t2_deg is not None and t3_deg is not None:
                self.t1_rrr_var.set(round(t1_deg, 1))
                self.t2_rrr_var.set(round(t2_deg, 1))
                self.t3_rrr_var.set(round(t3_deg, 1))
                self.H2Q_draw_robot_rrr(t1_deg, t2_deg, t3_deg)
        except (ValueError, ZeroDivisionError):
            pass
        finally:
            self.updating_rrr = False

    def H2Q_on_closing(self):
        self.root.quit()
        self.root.destroy()
        sys.exit(0)

if __name__ == '__main__':
    import ctypes

    try:
        myappid = 'h2qlab.robot.simulator.version2'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    root = tk.Tk()
    root.geometry("1150x860")
    root.option_add("*Font", ("Segoe UI", 10))
    app = H2Q_Multi_Robot_GUI_Final(root)
    root.mainloop()