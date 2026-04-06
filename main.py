import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle, Wedge
from PIL import Image, ImageTk
import os
import H2Q_Lib

class H2Q_RR_Robot_Pro_GUI_Final:
    def __init__(self, root):
        self.root = root
        self.root.title("H2Q Lab - Mô phỏng hoạt động cánh tay Robot v1")

        icon_path = H2Q_Lib.H2Q_get_resource_path("_icon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(default=icon_path)

        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'), padding=[15, 5])

        self.l1_var = tk.StringVar(value="20.0")
        self.l2_var = tk.StringVar(value="8.0")
        self.t1_var = tk.DoubleVar(value=-20)
        self.t2_var = tk.DoubleVar(value=-63)
        self.x_var = tk.StringVar(value="0.0")
        self.y_var = tk.StringVar(value="0.0")

        self.updating = False

        self.H2Q_setup_ui()

        self.x_var.trace_add("write", lambda *args: self.H2Q_update_from_coords())
        self.y_var.trace_add("write", lambda *args: self.H2Q_update_from_coords())
        self.l1_var.trace_add("write", lambda *args: self.H2Q_update_from_sliders())
        self.l2_var.trace_add("write", lambda *args: self.H2Q_update_from_sliders())

        self.H2Q_update_from_sliders()

    def H2Q_setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tab_sim = ttk.Frame(self.notebook)
        self.tab_info = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_sim, text="Mô phỏng")
        self.notebook.add(self.tab_info, text="Thông tin")

        self.H2Q_build_tab_sim()
        self.H2Q_build_tab_info()

    def H2Q_build_tab_sim(self):
        main_frame = ttk.Frame(self.tab_sim, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        control_frame = ttk.Frame(main_frame, padding="5")
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        link_frame = ttk.LabelFrame(control_frame, text="Kích thước robot", padding="10")
        link_frame.pack(fill=tk.X, pady=5)
        ttk.Label(link_frame, text="Link 1 (cm):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(link_frame, textvariable=self.l1_var, width=12).grid(row=0, column=1, pady=2)
        ttk.Label(link_frame, text="Link 2 (cm):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(link_frame, textvariable=self.l2_var, width=12).grid(row=1, column=1, pady=2)

        fk_frame = ttk.LabelFrame(control_frame, text="Động học thuận", padding="10")
        fk_frame.pack(fill=tk.X, pady=5)
        ttk.Label(fk_frame, text="Theta 1 (degree):").pack(anchor=tk.W)
        self.s1 = tk.Scale(fk_frame, from_=-180, to=180, orient=tk.HORIZONTAL,
                           variable=self.t1_var, command=lambda e: self.H2Q_update_from_sliders(),
                           troughcolor='greenyellow', activebackground='lawngreen')
        self.s1.pack(fill=tk.X)
        ttk.Label(fk_frame, text="Theta 2 (degree):").pack(anchor=tk.W)
        self.s2 = tk.Scale(fk_frame, from_=-180, to=180, orient=tk.HORIZONTAL,
                           variable=self.t2_var, command=lambda e: self.H2Q_update_from_sliders(),
                           troughcolor='greenyellow', activebackground='lawngreen')
        self.s2.pack(fill=tk.X)

        ik_frame = ttk.LabelFrame(control_frame, text="Động học nghịch", padding="10")
        ik_frame.pack(fill=tk.X, pady=5)
        ttk.Label(ik_frame, text="Tọa độ X (cm):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(ik_frame, textvariable=self.x_var, width=12).grid(row=0, column=1, pady=2)
        ttk.Label(ik_frame, text="Tọa độ Y (cm):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(ik_frame, textvariable=self.y_var, width=12).grid(row=1, column=1, pady=2)

        legend_frame = ttk.LabelFrame(control_frame, text="Chú thích", padding="10")
        legend_frame.pack(fill=tk.X, pady=5)
        self.lbl_link1 = tk.Label(legend_frame, text="▬ Link 1 (10.0 cm)", fg="blue", font=("Segoe UI", 10, "bold"),
                                  anchor="w")
        self.lbl_link1.pack(fill=tk.X, pady=2)
        self.lbl_link2 = tk.Label(legend_frame, text="▬ Link 2 (8.0 cm)", fg="red", font=("Segoe UI", 10, "bold"),
                                  anchor="w")
        self.lbl_link2.pack(fill=tk.X, pady=2)
        tk.Label(legend_frame, text="● Gốc tọa độ", fg="green", font=("Segoe UI", 10), anchor="w").pack(fill=tk.X,
                                                                                                        pady=2)
        tk.Label(legend_frame, text="★ Đầu công tác", fg="#DAA520", font=("Segoe UI", 10, "bold"), anchor="w").pack(
            fill=tk.X, pady=2)
        tk.Label(legend_frame, text="○ Vùng làm việc", fg="darkorange", font=("Segoe UI", 10, "bold"), anchor="w").pack(
            fill=tk.X, pady=2)

        self.fig, self.ax = plt.subplots(figsize=(9, 8))
        self.fig.subplots_adjust(left=0.06, right=0.96, top=0.96, bottom=0.06)

        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def H2Q_build_tab_info(self):
        main_info_frame = tk.Frame(self.tab_info)
        main_info_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        left_frame = tk.Frame(main_info_frame)
        left_frame.pack(side=tk.LEFT, padx=30)

        center_text_frame = tk.Frame(main_info_frame)
        center_text_frame.pack(side=tk.LEFT, padx=30)

        right_frame = tk.Frame(main_info_frame)
        right_frame.pack(side=tk.LEFT, padx=30)

        logo_filename = H2Q_Lib.H2Q_get_resource_path("_logo.png")
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
        tk.Label(center_text_frame, text="Điện thoại: 0978.39.41.43", font=("Segoe UI", 16), fg="#34495e").pack(pady=5)
        tk.Label(center_text_frame, text="For more information, please scan QR", font=("Segoe UI", 14, "italic"),
                 fg="#7f8c8d").pack(pady=(5, 0))

        qr_filename = H2Q_Lib.H2Q_get_resource_path("_qr.jpg")
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

    def H2Q_draw_robot(self, th1_deg, th2_deg):
        self.ax.clear()
        try:
            L1 = float(self.l1_var.get())
            L2 = float(self.l2_var.get())
            self.lbl_link1.config(text=f"▬ Link 1 ({L1} cm)")
            self.lbl_link2.config(text=f"▬ Link 2 ({L2} cm)")
        except ValueError:
            return 0, 0

        R_max = L1 + L2
        R_min = abs(L1 - L2)

        self.ax.set_facecolor('orange')
        white_workspace = Wedge((0, 0), R_max, 0, 360, facecolor='white', edgecolor='none')
        self.ax.add_patch(white_workspace)

        if R_min > 0.1:
            orange_center = Circle((0, 0), R_min, color='orange', fill=True)
            self.ax.add_patch(orange_center)

        x0, y0, x1, y1, x2, y2 = H2Q_Lib.H2Q_RR_Forward_Kinematics(L1, L2, th1_deg, th2_deg)

        self.ax.plot([x0, x1], [y0, y1], color='blue', linewidth=7)
        self.ax.plot([x1, x2], [y1, y2], color='red', linewidth=7)
        self.ax.plot(x0, y0, 'o', color='green', markersize=14)
        self.ax.plot(x1, y1, 'ko', markersize=8)
        self.ax.plot(x2, y2, '*', color='yellow', markersize=25, markeredgecolor='goldenrod')

        limit = R_max + 2
        self.ax.set_xlim(-limit, limit)
        self.ax.set_ylim(-limit, limit)
        self.ax.grid(True, linestyle=':', alpha=0.6)
        self.ax.set_aspect('equal')

        self.canvas.draw()
        return x2, y2

    def H2Q_update_from_sliders(self):
        if getattr(self, 'updating', False): return
        self.updating = True
        try:
            t1 = self.t1_var.get()
            t2 = self.t2_var.get()
            x, y = self.H2Q_draw_robot(t1, t2)
            self.x_var.set(f"{x:.3f}")
            self.y_var.set(f"{y:.3f}")
        finally:
            self.updating = False

    def H2Q_update_from_coords(self):
        if getattr(self, 'updating', False): return
        self.updating = True
        try:
            x = float(self.x_var.get())
            y = float(self.y_var.get())
            L1 = float(self.l1_var.get())
            L2 = float(self.l2_var.get())

            t1_deg, t2_deg = H2Q_Lib.H2Q_RR_Inverse_Kinematics(L1, L2, x, y)

            if t1_deg is not None and t2_deg is not None:
                self.t1_var.set(round(t1_deg, 1))
                self.t2_var.set(round(t2_deg, 1))
                self.H2Q_draw_robot(t1_deg, t2_deg)
        except (ValueError, ZeroDivisionError):
            pass
        finally:
            self.updating = False

if __name__ == '__main__':
    import ctypes
    try:
        myappid = 'h2qlab.robot.simulator.version1'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    root = tk.Tk()
    root.geometry("1100x750")
    root.option_add("*Font", ("Segoe UI", 10))
    app = H2Q_RR_Robot_Pro_GUI_Final(root)
    root.mainloop()