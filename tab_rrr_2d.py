import tkinter as tk
from tkinter import ttk
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle, Wedge
import H2Q_Lib


class TabRRR2D(ttk.Frame):
    def __init__(self, parent, vcmd, left_width):
        super().__init__(parent)
        self.vcmd = vcmd
        self.LEFT_WIDTH = left_width

        self.l1_var = tk.StringVar(value="10.0")
        self.l2_var = tk.StringVar(value="8.0")
        self.l3_var = tk.StringVar(value="5.0")
        self.t1_var = tk.DoubleVar(value=30)
        self.t2_var = tk.DoubleVar(value=-45)
        self.t3_var = tk.DoubleVar(value=-30)
        self.x_var = tk.StringVar(value="0.0")
        self.y_var = tk.StringVar(value="0.0")
        self.phi_var = tk.StringVar(value="0.0")
        self.updating = False

        self.build_ui()

        self.x_var.trace_add("write", lambda *args: self.update_from_coords())
        self.y_var.trace_add("write", lambda *args: self.update_from_coords())
        self.phi_var.trace_add("write", lambda *args: self.update_from_coords())
        self.l1_var.trace_add("write", lambda *args: self.update_from_sliders())
        self.l2_var.trace_add("write", lambda *args: self.update_from_sliders())
        self.l3_var.trace_add("write", lambda *args: self.update_from_sliders())

        self.update_from_sliders()

    def build_ui(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        control_frame = ttk.Frame(main_frame, padding="5", width=self.LEFT_WIDTH)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)
        control_frame.pack_propagate(False)

        lf1 = ttk.LabelFrame(control_frame, text="Kích thước cánh tay Robot", padding="5")
        lf1.pack(fill=tk.X, pady=3)
        ttk.Label(lf1, text="Link 1 (cm):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(lf1, textvariable=self.l1_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=0,
                                                                                                           column=1,
                                                                                                           pady=1,
                                                                                                           sticky=tk.E)
        ttk.Label(lf1, text="Link 2 (cm):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(lf1, textvariable=self.l2_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=1,
                                                                                                           column=1,
                                                                                                           pady=1,
                                                                                                           sticky=tk.E)
        ttk.Label(lf1, text="Link 3 (cm):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(lf1, textvariable=self.l3_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=2,
                                                                                                           column=1,
                                                                                                           pady=1,
                                                                                                           sticky=tk.E)

        lf2 = ttk.LabelFrame(control_frame, text="Động học thuận", padding="5")
        lf2.pack(fill=tk.X, pady=3)
        ttk.Label(lf2, text="Theta 1 (degree):").pack(anchor=tk.W)
        tk.Scale(lf2, from_=-180, to=180, orient=tk.HORIZONTAL, variable=self.t1_var,
                 command=lambda e: self.update_from_sliders(), troughcolor='greenyellow').pack(fill=tk.X)
        ttk.Label(lf2, text="Theta 2 (degree):").pack(anchor=tk.W)
        tk.Scale(lf2, from_=-180, to=180, orient=tk.HORIZONTAL, variable=self.t2_var,
                 command=lambda e: self.update_from_sliders(), troughcolor='greenyellow').pack(fill=tk.X)
        ttk.Label(lf2, text="Theta 3 (degree):").pack(anchor=tk.W)
        tk.Scale(lf2, from_=-180, to=180, orient=tk.HORIZONTAL, variable=self.t3_var,
                 command=lambda e: self.update_from_sliders(), troughcolor='greenyellow').pack(fill=tk.X)

        lf3 = ttk.LabelFrame(control_frame, text="Động học nghịch", padding="5")
        lf3.pack(fill=tk.X, pady=3)
        ttk.Label(lf3, text="Tọa độ X (cm):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(lf3, textvariable=self.x_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=0,
                                                                                                          column=1,
                                                                                                          pady=1,
                                                                                                          sticky=tk.E)
        ttk.Label(lf3, text="Tọa độ Y (cm):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(lf3, textvariable=self.y_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=1,
                                                                                                          column=1,
                                                                                                          pady=1,
                                                                                                          sticky=tk.E)
        ttk.Label(lf3, text="Góc Phi (degree):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(lf3, textvariable=self.phi_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=2,
                                                                                                            column=1,
                                                                                                            pady=1,
                                                                                                            sticky=tk.E)

        lf4 = ttk.LabelFrame(control_frame, text="Chú thích", padding="5")
        lf4.pack(fill=tk.X, pady=3)
        self.lbl_link1 = tk.Label(lf4, text="▬ Link 1", fg="blue", font=("Segoe UI", 12, "bold"), anchor="w");
        self.lbl_link1.pack(fill=tk.X)
        self.lbl_link2 = tk.Label(lf4, text="▬ Link 2", fg="red", font=("Segoe UI", 12, "bold"), anchor="w");
        self.lbl_link2.pack(fill=tk.X)
        self.lbl_link3 = tk.Label(lf4, text="▬ Link 3", fg="magenta", font=("Segoe UI", 12, "bold"), anchor="w");
        self.lbl_link3.pack(fill=tk.X)
        tk.Label(lf4, text="● Gốc tọa độ", fg="green", font=("Segoe UI", 12, "bold"), anchor="w").pack(fill=tk.X)
        tk.Label(lf4, text="★ Đầu công tác", fg="#DAA520", font=("Segoe UI", 12, "bold"), anchor="w").pack(fill=tk.X)
        tk.Label(lf4, text="○ Vùng làm việc", fg="darkorange", font=("Segoe UI", 12, "bold"), anchor="w").pack(
            fill=tk.X)

        lf5 = ttk.LabelFrame(control_frame, text="Mô tả cánh tay Robot", padding="5")
        lf5.pack(fill=tk.X, pady=3)
        desc_rrr1 = "Cánh tay RRR 3 bậc phẳng (Planar 3-DOF). Có khả năng điều khiển tọa độ (X, Y) và tùy chỉnh được góc nghiêng Phi của đầu công tác. Ứng dụng: Gắp nhả (Pick-and-Place)."
        ttk.Label(lf5, text=desc_rrr1, style="Desc.TLabel", justify=tk.LEFT, wraplength=290).pack(fill=tk.X)

        self.fig, self.ax = plt.subplots(figsize=(9, 8))
        self.fig.subplots_adjust(left=0.06, right=0.96, top=0.96, bottom=0.06)
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def draw_robot(self, t1, t2, t3):
        self.ax.clear()
        try:
            L1, L2, L3 = float(self.l1_var.get()), float(self.l2_var.get()), float(self.l3_var.get())
        except ValueError:
            return 0, 0, 0

        self.lbl_link1.config(text=f"▬ Link 1 ({L1} cm)")
        self.lbl_link2.config(text=f"▬ Link 2 ({L2} cm)")
        self.lbl_link3.config(text=f"▬ Link 3 ({L3} cm)")
        r_max = L1 + L2 + L3
        r_min = max(0, L1 - L2 - L3, L2 - L1 - L3, L3 - L1 - L2)

        self.ax.set_facecolor('orange')
        self.ax.add_patch(Wedge((0, 0), r_max, 0, 360, facecolor='white'))
        if r_min > 0.1:
            self.ax.add_patch(Circle((0, 0), r_min, color='orange'))

        x0, y0, x1, y1, x2, y2, x3, y3, phi = H2Q_Lib.H2Q_RRR_Forward_Kinematics(L1, L2, L3, t1, t2, t3)

        self.ax.plot([x0, x1], [y0, y1], color='blue', lw=7)
        self.ax.plot([x1, x2], [y1, y2], color='red', lw=7)
        self.ax.plot([x2, x3], [y2, y3], color='magenta', lw=7)
        self.ax.plot(x0, y0, 'o', color='green', ms=14)
        self.ax.plot(x1, y1, 'ko', ms=8)
        self.ax.plot(x2, y2, 'ko', ms=8)
        self.ax.plot(x3, y3, '*', color='yellow', ms=25, mec='goldenrod')

        lim = r_max + 2
        self.ax.set(xlim=(-lim, lim), ylim=(-lim, lim), aspect='equal')
        self.ax.grid(ls=':', alpha=0.6)
        self.canvas.draw()
        return x3, y3, math.degrees(phi)

    def update_from_sliders(self):
        if self.updating: return
        self.updating = True
        try:
            x, y, phi = self.draw_robot(self.t1_var.get(), self.t2_var.get(), self.t3_var.get())
            self.x_var.set(f"{x:.3f}")
            self.y_var.set(f"{y:.3f}")
            self.phi_var.set(f"{phi:.1f}")
        finally:
            self.updating = False

    def update_from_coords(self):
        if self.updating: return
        self.updating = True
        try:
            L1, L2, L3 = float(self.l1_var.get()), float(self.l2_var.get()), float(self.l3_var.get())
            t1, t2, t3 = H2Q_Lib.H2Q_RRR_Inverse_Kinematics(L1, L2, L3, float(self.x_var.get()),
                                                            float(self.y_var.get()), float(self.phi_var.get()))
            if t1 is not None:
                self.t1_var.set(round(t1, 1))
                self.t2_var.set(round(t2, 1))
                self.t3_var.set(round(t3, 1))
                self.draw_robot(t1, t2, t3)
        except ValueError:
            pass
        finally:
            self.updating = False