import tkinter as tk
from tkinter import ttk
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle, Wedge
from PIL import Image, ImageTk
import os
import sys


# Hàm bùa chú giúp file exe tìm được ảnh đang bị nhồi bên trong nó
def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class RRR_Robot_Pro_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("H2Q Lab - Mô phỏng hoạt động cánh tay robot RRR (3 Bậc)")

        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'), padding=[15, 5])

        # Khởi tạo kích thước 3 khâu
        self.l1_var = tk.StringVar(value="10.0")
        self.l2_var = tk.StringVar(value="8.0")
        self.l3_var = tk.StringVar(value="5.0")

        # Khởi tạo 3 góc Theta
        self.t1_var = tk.DoubleVar(value=30)
        self.t2_var = tk.DoubleVar(value=-45)
        self.t3_var = tk.DoubleVar(value=-30)

        # Khởi tạo tọa độ X, Y và góc hướng Phi
        self.x_var = tk.StringVar(value="0.0")
        self.y_var = tk.StringVar(value="0.0")
        self.phi_var = tk.StringVar(value="0.0")

        self.updating = False

        self.setup_ui()

        # Gắn trigger cho IK (khi gõ X, Y, Phi)
        self.x_var.trace_add("write", lambda *args: self.update_from_coords())
        self.y_var.trace_add("write", lambda *args: self.update_from_coords())
        self.phi_var.trace_add("write", lambda *args: self.update_from_coords())

        # Gắn trigger cập nhật hình khi đổi độ dài Link
        self.l1_var.trace_add("write", lambda *args: self.update_from_sliders())
        self.l2_var.trace_add("write", lambda *args: self.update_from_sliders())
        self.l3_var.trace_add("write", lambda *args: self.update_from_sliders())

        self.update_from_sliders()

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tab_sim = ttk.Frame(self.notebook)
        self.tab_info = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_sim, text="Mô phỏng")
        self.notebook.add(self.tab_info, text="Thông tin")

        self.build_tab_sim()
        self.build_tab_info()

    def build_tab_sim(self):
        main_frame = ttk.Frame(self.tab_sim, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        control_frame = ttk.Frame(main_frame, padding="5")
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        # 0. Kích thước robot
        link_frame = ttk.LabelFrame(control_frame, text="Kích thước robot", padding="10")
        link_frame.pack(fill=tk.X, pady=5)
        ttk.Label(link_frame, text="Link 1 (cm):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(link_frame, textvariable=self.l1_var, width=12).grid(row=0, column=1, pady=2)
        ttk.Label(link_frame, text="Link 2 (cm):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(link_frame, textvariable=self.l2_var, width=12).grid(row=1, column=1, pady=2)
        ttk.Label(link_frame, text="Link 3 (cm):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(link_frame, textvariable=self.l3_var, width=12).grid(row=2, column=1, pady=2)

        # 1. Động học thuận
        fk_frame = ttk.LabelFrame(control_frame, text="Động học thuận", padding="10")
        fk_frame.pack(fill=tk.X, pady=5)

        ttk.Label(fk_frame, text="Theta 1 (degree):").pack(anchor=tk.W)
        self.s1 = tk.Scale(fk_frame, from_=-180, to=180, orient=tk.HORIZONTAL,
                           variable=self.t1_var, command=lambda e: self.update_from_sliders(),
                           troughcolor='greenyellow', activebackground='lawngreen')
        self.s1.pack(fill=tk.X)

        ttk.Label(fk_frame, text="Theta 2 (degree):").pack(anchor=tk.W)
        self.s2 = tk.Scale(fk_frame, from_=-180, to=180, orient=tk.HORIZONTAL,
                           variable=self.t2_var, command=lambda e: self.update_from_sliders(),
                           troughcolor='greenyellow', activebackground='lawngreen')
        self.s2.pack(fill=tk.X)

        ttk.Label(fk_frame, text="Theta 3 (degree):").pack(anchor=tk.W)
        self.s3 = tk.Scale(fk_frame, from_=-180, to=180, orient=tk.HORIZONTAL,
                           variable=self.t3_var, command=lambda e: self.update_from_sliders(),
                           troughcolor='greenyellow', activebackground='lawngreen')
        self.s3.pack(fill=tk.X)

        # 2. Động học nghịch
        ik_frame = ttk.LabelFrame(control_frame, text="Động học nghịch", padding="10")
        ik_frame.pack(fill=tk.X, pady=5)
        ttk.Label(ik_frame, text="Tọa độ X (cm):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(ik_frame, textvariable=self.x_var, width=12).grid(row=0, column=1, pady=2)
        ttk.Label(ik_frame, text="Tọa độ Y (cm):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(ik_frame, textvariable=self.y_var, width=12).grid(row=1, column=1, pady=2)
        ttk.Label(ik_frame, text="Góc Phi (degree):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(ik_frame, textvariable=self.phi_var, width=12).grid(row=2, column=1, pady=2)

        # 3. Chú thích
        legend_frame = ttk.LabelFrame(control_frame, text="Chú thích", padding="10")
        legend_frame.pack(fill=tk.X, pady=5)
        self.lbl_link1 = tk.Label(legend_frame, text="▬ Link 1 (10.0 cm)", fg="blue", font=("Segoe UI", 10, "bold"),
                                  anchor="w")
        self.lbl_link1.pack(fill=tk.X, pady=2)
        self.lbl_link2 = tk.Label(legend_frame, text="▬ Link 2 (8.0 cm)", fg="red", font=("Segoe UI", 10, "bold"),
                                  anchor="w")
        self.lbl_link2.pack(fill=tk.X, pady=2)
        self.lbl_link3 = tk.Label(legend_frame, text="▬ Link 3 (5.0 cm)", fg="magenta", font=("Segoe UI", 10, "bold"),
                                  anchor="w")
        self.lbl_link3.pack(fill=tk.X, pady=2)
        tk.Label(legend_frame, text="● Gốc tọa độ", fg="green", font=("Segoe UI", 10), anchor="w").pack(fill=tk.X,
                                                                                                        pady=2)
        tk.Label(legend_frame, text="★ Đầu công tác", fg="#DAA520", font=("Segoe UI", 10, "bold"), anchor="w").pack(
            fill=tk.X, pady=2)

        # --- CỘT PHẢI: ĐỒ THỊ ---
        self.fig, self.ax = plt.subplots(figsize=(9, 8))
        self.fig.subplots_adjust(left=0.06, right=0.96, top=0.96, bottom=0.06)

        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def build_tab_info(self):
        center_frame = tk.Frame(self.tab_info)
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        img_filename = get_resource_path("avatar.png")

        try:
            if os.path.exists(img_filename):
                img = Image.open(img_filename)
                img = img.resize((250, 250), Image.Resampling.LANCZOS)
                self.avatar_img = ImageTk.PhotoImage(img)
                lbl_img = tk.Label(center_frame, image=self.avatar_img)
                lbl_img.pack(pady=10)
            else:
                lbl_img = tk.Label(center_frame,
                                   text="[Vui lòng đặt file ảnh\ntên 'avatar.png'\nvào cùng thư mục code]",
                                   bg="lightgray", fg="gray", width=25, height=10, font=("Segoe UI", 10, "italic"))
                lbl_img.pack(pady=10)
        except Exception as e:
            tk.Label(center_frame, text=f"Lỗi load ảnh: {e}", fg="red").pack(pady=10)

        tk.Label(center_frame, text="Trần Hoàn", font=("Segoe UI", 28, "bold"), fg="#2c3e50").pack(pady=10)
        info_font = ("Segoe UI", 14)
        tk.Label(center_frame, text="Điện thoại: 0978.39.41.43 (Telegram/Whatsapp)", font=info_font, fg="#34495e").pack(
            pady=5)
        lbl_web = tk.Label(center_frame, text="Website: hano.cf", font=("Segoe UI", 14, "underline"), fg="#2980b9",
                           cursor="hand2")
        lbl_web.pack(pady=5)

    def draw_robot(self, th1_deg, th2_deg, th3_deg):
        self.ax.clear()
        try:
            L1 = float(self.l1_var.get())
            L2 = float(self.l2_var.get())
            L3 = float(self.l3_var.get())
            self.lbl_link1.config(text=f"▬ Link 1 ({L1} cm)")
            self.lbl_link2.config(text=f"▬ Link 2 ({L2} cm)")
            self.lbl_link3.config(text=f"▬ Link 3 ({L3} cm)")
        except ValueError:
            return 0, 0, 0

            # Vùng hoạt động cực đại
        R_max = L1 + L2 + L3
        # Vùng điểm mù ở tâm
        R_min = max(0, L1 - L2 - L3, L2 - L1 - L3, L3 - L1 - L2)

        self.ax.set_facecolor('orange')
        white_workspace = Wedge((0, 0), R_max, 0, 360, facecolor='white', edgecolor='none')
        self.ax.add_patch(white_workspace)

        if R_min > 0.1:
            orange_center = Circle((0, 0), R_min, color='orange', fill=True)
            self.ax.add_patch(orange_center)

        th1 = math.radians(th1_deg)
        th2 = math.radians(th2_deg)
        th3 = math.radians(th3_deg)
        phi_rad = th1 + th2 + th3

        # Tính tọa độ các khớp
        x0, y0 = 0, 0
        x1 = L1 * math.cos(th1)
        y1 = L1 * math.sin(th1)
        x2 = x1 + L2 * math.cos(th1 + th2)
        y2 = y1 + L2 * math.sin(th1 + th2)
        x3 = x2 + L3 * math.cos(phi_rad)
        y3 = y2 + L3 * math.sin(phi_rad)

        # Vẽ 3 khâu
        self.ax.plot([x0, x1], [y0, y1], color='blue', linewidth=7)
        self.ax.plot([x1, x2], [y1, y2], color='red', linewidth=7)
        self.ax.plot([x2, x3], [y2, y3], color='magenta', linewidth=7)  # Khâu 3 màu hồng

        # Vẽ các khớp
        self.ax.plot(x0, y0, 'o', color='green', markersize=14)
        self.ax.plot(x1, y1, 'ko', markersize=8)
        self.ax.plot(x2, y2, 'ko', markersize=8)

        # Vẽ đầu công tác
        self.ax.plot(x3, y3, '*', color='yellow', markersize=25, markeredgecolor='goldenrod')

        limit = R_max + 2
        self.ax.set_xlim(-limit, limit)
        self.ax.set_ylim(-limit, limit)
        self.ax.grid(True, linestyle=':', alpha=0.6)
        self.ax.set_aspect('equal')

        self.canvas.draw()
        return x3, y3, math.degrees(phi_rad)

    def update_from_sliders(self):
        if getattr(self, 'updating', False): return
        self.updating = True
        try:
            t1 = self.t1_var.get()
            t2 = self.t2_var.get()
            t3 = self.t3_var.get()
            x, y, phi = self.draw_robot(t1, t2, t3)

            self.x_var.set(f"{x:.3f}")
            self.y_var.set(f"{y:.3f}")
            self.phi_var.set(f"{phi:.1f}")
        finally:
            self.updating = False

    def update_from_coords(self):
        if getattr(self, 'updating', False): return
        self.updating = True
        try:
            x = float(self.x_var.get())
            y = float(self.y_var.get())
            phi_deg = float(self.phi_var.get())

            L1 = float(self.l1_var.get())
            L2 = float(self.l2_var.get())
            L3 = float(self.l3_var.get())

            phi_rad = math.radians(phi_deg)

            # Tách riêng cụm cổ tay (Wrist)
            xw = x - L3 * math.cos(phi_rad)
            yw = y - L3 * math.sin(phi_rad)

            # Giải IK cho cơ cấu 2R còn lại
            cos_t2 = (xw ** 2 + yw ** 2 - L1 ** 2 - L2 ** 2) / (2 * L1 * L2)
            if -1.0 <= cos_t2 <= 1.0:
                sin_t2 = math.sqrt(1 - cos_t2 ** 2)
                th2 = math.atan2(sin_t2, cos_t2)

                k1 = L1 + L2 * cos_t2
                k2 = L2 * sin_t2
                th1 = math.atan2(yw, xw) - math.atan2(k2, k1)

                th3 = phi_rad - th1 - th2

                t1_deg = math.degrees(th1)
                t2_deg = math.degrees(th2)
                t3_deg = math.degrees(th3)

                self.t1_var.set(round(t1_deg, 1))
                self.t2_var.set(round(t2_deg, 1))
                self.t3_var.set(round(t3_deg, 1))

                self.draw_robot(t1_deg, t2_deg, t3_deg)
        except (ValueError, ZeroDivisionError):
            pass  # Lờ đi nếu người dùng đang nhập dở chữ số
        finally:
            self.updating = False


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1050x780")  # Chỉnh cửa sổ dài ra tí để chứa đủ các control mới
    root.option_add("*Font", ("Segoe UI", 10))
    app = RRR_Robot_Pro_GUI(root)
    root.mainloop()