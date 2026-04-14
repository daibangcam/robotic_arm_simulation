import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
import H2Q_Lib


class TabRRR3D(ttk.Frame):
    def __init__(self, parent, vcmd, left_width):
        super().__init__(parent)
        self.vcmd = vcmd
        self.LEFT_WIDTH = left_width

        self.l1_var = tk.StringVar(value="10.0")
        self.l2_var = tk.StringVar(value="15.0")
        self.l3_var = tk.StringVar(value="10.0")
        self.t1_var = tk.DoubleVar(value=45)
        self.t2_var = tk.DoubleVar(value=30)
        self.t3_var = tk.DoubleVar(value=-60)
        self.x_var = tk.StringVar(value="0.0")
        self.y_var = tk.StringVar(value="0.0")
        self.z_var = tk.StringVar(value="0.0")
        self.updating = False

        self.build_ui()

        self.x_var.trace_add("write", lambda *args: self.update_from_coords())
        self.y_var.trace_add("write", lambda *args: self.update_from_coords())
        self.z_var.trace_add("write", lambda *args: self.update_from_coords())
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
        ttk.Label(lf1, text="Trục bệ L1 (cm):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(lf1, textvariable=self.l1_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=0,
                                                                                                           column=1,
                                                                                                           pady=1,
                                                                                                           sticky=tk.E)
        ttk.Label(lf1, text="Khớp vai L2 (cm):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(lf1, textvariable=self.l2_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=1,
                                                                                                           column=1,
                                                                                                           pady=1,
                                                                                                           sticky=tk.E)
        ttk.Label(lf1, text="Khuỷu tay L3 (cm):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(lf1, textvariable=self.l3_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=2,
                                                                                                           column=1,
                                                                                                           pady=1,
                                                                                                           sticky=tk.E)

        lf2 = ttk.LabelFrame(control_frame, text="Động học thuận", padding="5")
        lf2.pack(fill=tk.X, pady=3)
        ttk.Label(lf2, text="Xoay nền T1 (deg):").pack(anchor=tk.W)
        tk.Scale(lf2, from_=-180, to=180, orient=tk.HORIZONTAL, variable=self.t1_var,
                 command=lambda e: self.update_from_sliders(), troughcolor='greenyellow').pack(fill=tk.X)
        ttk.Label(lf2, text="Nâng vai T2 (deg):").pack(anchor=tk.W)
        tk.Scale(lf2, from_=-90, to=90, orient=tk.HORIZONTAL, variable=self.t2_var,
                 command=lambda e: self.update_from_sliders(), troughcolor='greenyellow').pack(fill=tk.X)
        ttk.Label(lf2, text="Gập khuỷu T3 (deg):").pack(anchor=tk.W)
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
        ttk.Label(lf3, text="Tọa độ Z (cm):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(lf3, textvariable=self.z_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=2,
                                                                                                          column=1,
                                                                                                          pady=1,
                                                                                                          sticky=tk.E)

        lf4 = ttk.LabelFrame(control_frame, text="Chú thích", padding="5")
        lf4.pack(fill=tk.X, pady=3)
        self.lbl_link1 = tk.Label(lf4, text="▬ Trục bệ (Base)", fg="blue", font=("Segoe UI", 12, "bold"), anchor="w");
        self.lbl_link1.pack(fill=tk.X)
        self.lbl_link2 = tk.Label(lf4, text="▬ Khớp vai (Shoulder)", fg="red", font=("Segoe UI", 12, "bold"),
                                  anchor="w");
        self.lbl_link2.pack(fill=tk.X)
        self.lbl_link3 = tk.Label(lf4, text="▬ Khuỷu tay (Elbow)", fg="magenta", font=("Segoe UI", 12, "bold"),
                                  anchor="w");
        self.lbl_link3.pack(fill=tk.X)
        tk.Label(lf4, text="★ Đầu công tác", fg="#DAA520", font=("Segoe UI", 12, "bold"), anchor="w").pack(fill=tk.X)
        tk.Label(lf4, text="○ Vùng làm việc (Khối cầu)", fg="darkorange", font=("Segoe UI", 12, "bold"),
                 anchor="w").pack(fill=tk.X)

        lf5 = ttk.LabelFrame(control_frame, text="Mô tả cánh tay Robot", padding="5")
        lf5.pack(fill=tk.X, pady=3)
        desc_rrr2 = "Cánh tay RRR không gian (Spatial 3-DOF). Cơ cấu tương đương robot công nghiệp (như hàn, sơn). Khớp 1 xoay nền, khớp 2 và 3 nâng gập cánh tay trong không gian 3D."
        ttk.Label(lf5, text=desc_rrr2, style="Desc.TLabel", justify=tk.LEFT, wraplength=290).pack(fill=tk.X)

        self.fig = plt.figure(figsize=(9, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def draw_robot(self, t1, t2, t3):
        self.ax.clear()
        try:
            L1, L2, L3 = float(self.l1_var.get()), float(self.l2_var.get()), float(self.l3_var.get())
        except ValueError:
            return 0, 0, 0

        self.lbl_link1.config(text=f"▬ Trục bệ ({L1} cm)")
        self.lbl_link2.config(text=f"▬ Khớp vai ({L2} cm)")
        self.lbl_link3.config(text=f"▬ Khuỷu tay ({L3} cm)")

        p0, p1, p2, p3 = H2Q_Lib.H2Q_RRR_3D_Forward_Kinematics(L1, L2, L3, t1, t2, t3)

        R_max = L2 + L3
        u = np.linspace(0, 2 * np.pi, 30)
        v = np.linspace(0, np.pi, 30)
        X_sphere = R_max * np.outer(np.cos(u), np.sin(v))
        Y_sphere = R_max * np.outer(np.sin(u), np.sin(v))
        Z_sphere = L1 + R_max * np.outer(np.ones(np.size(u)), np.cos(v))
        self.ax.plot_surface(X_sphere, Y_sphere, Z_sphere, color='orange', alpha=0.15, edgecolor='none')

        self.ax.plot([p0[0], p1[0]], [p0[1], p1[1]], [p0[2], p1[2]], color='blue', lw=7)
        self.ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color='red', lw=7)
        self.ax.plot([p2[0], p3[0]], [p2[1], p3[1]], [p2[2], p3[2]], color='magenta', lw=7)

        self.ax.scatter([p0[0], p1[0], p2[0]], [p0[1], p1[1], p2[1]], [p0[2], p1[2], p2[2]], color='green', s=100)
        self.ax.scatter([p3[0]], [p3[1]], [p3[2]], color='yellow', s=300, marker='*', edgecolors='goldenrod')

        limit = L1 + L2 + L3
        self.ax.set_xlim([-limit, limit])
        self.ax.set_ylim([-limit, limit])
        self.ax.set_zlim([0, limit])
        self.ax.set_xlabel('Trục X (cm)')
        self.ax.set_ylabel('Trục Y (cm)')
        self.ax.set_zlabel('Trục Z (cm)')

        self.canvas.draw()
        return p3[0], p3[1], p3[2]

    def update_from_sliders(self):
        if self.updating: return
        self.updating = True
        try:
            x, y, z = self.draw_robot(self.t1_var.get(), self.t2_var.get(), self.t3_var.get())
            self.x_var.set(f"{x:.3f}")
            self.y_var.set(f"{y:.3f}")
            self.z_var.set(f"{z:.3f}")
        except ValueError:
            pass
        finally:
            self.updating = False

    def update_from_coords(self):
        if self.updating: return
        self.updating = True
        try:
            L1, L2, L3 = float(self.l1_var.get()), float(self.l2_var.get()), float(self.l3_var.get())
            X, Y, Z = float(self.x_var.get()), float(self.y_var.get()), float(self.z_var.get())
            t1, t2, t3 = H2Q_Lib.H2Q_RRR_3D_Inverse_Kinematics(L1, L2, L3, X, Y, Z)

            if t1 is not None and t2 is not None and t3 is not None:
                self.t1_var.set(round(t1, 1))
                self.t2_var.set(round(t2, 1))
                self.t3_var.set(round(t3, 1))
                self.draw_robot(t1, t2, t3)
        except ValueError:
            pass
        finally:
            self.updating = False