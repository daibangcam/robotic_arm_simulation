import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle, Wedge
import H2Q_Lib


class TabRR2D(ttk.Frame):
    def __init__(self, parent, vcmd, left_width):
        super().__init__(parent)
        self.vcmd, self.LEFT_WIDTH = vcmd, left_width
        self.l1_var, self.l2_var = tk.StringVar(value="20.0"), tk.StringVar(value="8.0")
        self.t1_min_var, self.t1_max_var = tk.StringVar(value="-180"), tk.StringVar(value="180")
        self.t2_min_var, self.t2_max_var = tk.StringVar(value="-180"), tk.StringVar(value="180")
        self.t1_var, self.t2_var = tk.DoubleVar(value=-20), tk.DoubleVar(value=-63)
        self.x_var, self.y_var = tk.StringVar(), tk.StringVar()
        self.updating = False

        self.build_ui()
        self.x_var.trace_add("write", lambda *args: self.update_from_coords())
        self.y_var.trace_add("write", lambda *args: self.update_from_coords())
        for var in [self.l1_var, self.l2_var]: var.trace_add("write", lambda *args: self.update_from_sliders())
        for var in [self.t1_min_var, self.t1_max_var, self.t2_min_var, self.t2_max_var]:
            var.trace_add("write", lambda *args: self.update_scale_limits())

        self.update_scale_limits()
        self.update_from_sliders()

    def build_ui(self):
        main_frame = ttk.Frame(self, padding="5")
        main_frame.pack(fill=tk.BOTH, expand=True)
        left_container = ttk.Frame(main_frame, width=self.LEFT_WIDTH)
        left_container.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        left_container.pack_propagate(False)

        canvas = tk.Canvas(left_container, width=self.LEFT_WIDTH - 20, highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_container, orient="vertical", command=canvas.yview)
        control_frame = ttk.Frame(canvas, width=self.LEFT_WIDTH - 25)

        control_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=control_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def _on_mousewheel(e):
            try:
                if not canvas.winfo_ismapped(): return
                cx = canvas.winfo_rootx()
                cy = canvas.winfo_rooty()
                cw = canvas.winfo_width()
                ch = canvas.winfo_height()
                if cx <= e.x_root <= cx + cw and cy <= e.y_root <= cy + ch:
                    if control_frame.winfo_reqheight() > ch:
                        canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
            except: pass

        canvas.bind_all("<MouseWheel>", _on_mousewheel, add="+")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        lf1 = ttk.LabelFrame(control_frame, text="Kích thước cánh tay Robot", padding="5")
        lf1.pack(fill=tk.X, pady=3)
        ttk.Label(lf1, text="Link 1 (cm):").grid(row=0, column=0, sticky=tk.W, padx=(0, 15))
        ttk.Entry(lf1, textvariable=self.l1_var, width=10, validate="key", validatecommand=self.vcmd).grid(row=0, column=1, pady=2, sticky=tk.W)
        ttk.Label(lf1, text="Link 2 (cm):").grid(row=1, column=0, sticky=tk.W, padx=(0, 15))
        ttk.Entry(lf1, textvariable=self.l2_var, width=10, validate="key", validatecommand=self.vcmd).grid(row=1, column=1, pady=2, sticky=tk.W)

        lf_limit = ttk.LabelFrame(control_frame, text="Giới hạn khớp", padding="5")
        lf_limit.pack(fill=tk.X, pady=3)
        ttk.Label(lf_limit, text="T1 Min/Max (độ):").grid(row=0, column=0, sticky=tk.W, padx=(0, 15))
        ttk.Entry(lf_limit, textvariable=self.t1_min_var, width=6, validate="key", validatecommand=self.vcmd).grid(row=0, column=1, pady=2, padx=(0, 5), sticky=tk.W)
        ttk.Entry(lf_limit, textvariable=self.t1_max_var, width=6, validate="key", validatecommand=self.vcmd).grid(row=0, column=2, pady=2, sticky=tk.W)
        ttk.Label(lf_limit, text="T2 Min/Max (độ):").grid(row=1, column=0, sticky=tk.W, padx=(0, 15))
        ttk.Entry(lf_limit, textvariable=self.t2_min_var, width=6, validate="key", validatecommand=self.vcmd).grid(row=1, column=1, pady=2, padx=(0, 5), sticky=tk.W)
        ttk.Entry(lf_limit, textvariable=self.t2_max_var, width=6, validate="key", validatecommand=self.vcmd).grid(row=1, column=2, pady=2, sticky=tk.W)

        lf2 = ttk.LabelFrame(control_frame, text="Động học thuận", padding="5")
        lf2.pack(fill=tk.X, pady=3)
        ttk.Label(lf2, text="Theta 1 (độ):").pack(anchor=tk.W)
        self.s1 = tk.Scale(lf2, from_=-180, to=180, orient=tk.HORIZONTAL, variable=self.t1_var, command=lambda e: self.update_from_sliders(), troughcolor='greenyellow')
        self.s1.pack(fill=tk.X)
        ttk.Label(lf2, text="Theta 2 (độ):").pack(anchor=tk.W)
        self.s2 = tk.Scale(lf2, from_=-180, to=180, orient=tk.HORIZONTAL, variable=self.t2_var, command=lambda e: self.update_from_sliders(), troughcolor='greenyellow')
        self.s2.pack(fill=tk.X)

        lf3 = ttk.LabelFrame(control_frame, text="Động học nghịch", padding="5")
        lf3.pack(fill=tk.X, pady=3)
        ttk.Label(lf3, text="Tọa độ X (cm):").grid(row=0, column=0, sticky=tk.W, padx=(0, 15))
        ttk.Entry(lf3, textvariable=self.x_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=0, column=1, pady=2, sticky=tk.W)
        ttk.Label(lf3, text="Tọa độ Y (cm):").grid(row=1, column=0, sticky=tk.W, padx=(0, 15))
        ttk.Entry(lf3, textvariable=self.y_var, width=12, validate="key", validatecommand=self.vcmd).grid(row=1, column=1, pady=2, sticky=tk.W)

        lf4 = ttk.LabelFrame(control_frame, text="Chú thích", padding="5")
        lf4.pack(fill=tk.X, pady=3)
        self.lbl_link1 = tk.Label(lf4, text="▬ Link 1", fg="blue", font=("Segoe UI", 12, "bold"), anchor="w")
        self.lbl_link1.pack(fill=tk.X)
        self.lbl_link2 = tk.Label(lf4, text="▬ Link 2", fg="red", font=("Segoe UI", 12, "bold"), anchor="w")
        self.lbl_link2.pack(fill=tk.X)
        tk.Label(lf4, text="● Gốc tọa độ", fg="green", font=("Segoe UI", 12, "bold"), anchor="w").pack(fill=tk.X)
        tk.Label(lf4, text="★ Đầu công tác", fg="#DAA520", font=("Segoe UI", 12, "bold"), anchor="w").pack(fill=tk.X)
        tk.Label(lf4, text="○ Vùng làm việc", fg="darkorange", font=("Segoe UI", 12, "bold"), anchor="w").pack(fill=tk.X)

        lf5 = ttk.LabelFrame(control_frame, text="Mô tả cánh tay Robot", padding="5")
        lf5.pack(fill=tk.X, pady=3)
        desc_rr = "Cánh tay robot RR 2 bậc tự do (Planar 2-DOF). Ứng dụng phổ biến trong việc định vị mũi công tác tại tọa độ (X, Y) trong không gian làm việc phẳng."
        ttk.Label(lf5, text=desc_rr, style="Desc.TLabel", justify=tk.LEFT, wraplength=self.LEFT_WIDTH - 40).pack(fill=tk.X)

        self.fig, self.ax = plt.subplots(figsize=(9, 8))
        self.fig.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.08)
        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas_plot.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def update_scale_limits(self):
        try:
            t1_min, t1_max = float(self.t1_min_var.get()), float(self.t1_max_var.get())
            t2_min, t2_max = float(self.t2_min_var.get()), float(self.t2_max_var.get())
            if t1_min < t1_max: self.s1.config(from_=t1_min, to=t1_max)
            if t2_min < t2_max: self.s2.config(from_=t2_min, to=t2_max)
        except: pass

    def draw_robot(self, t1, t2):
        self.ax.clear()
        try: L1, L2 = float(self.l1_var.get()), float(self.l2_var.get())
        except ValueError: return 0, 0
        self.lbl_link1.config(text=f"▬ Link 1 ({L1} cm)")
        self.lbl_link2.config(text=f"▬ Link 2 ({L2} cm)")
        r_max, r_min = L1 + L2, abs(L1 - L2)
        self.ax.set_facecolor('orange')
        self.ax.add_patch(Wedge((0, 0), r_max, 0, 360, facecolor='white'))
        if r_min > 0.1: self.ax.add_patch(Circle((0, 0), r_min, color='orange'))
        x0, y0, x1, y1, x2, y2 = H2Q_Lib.H2Q_RR_Forward_Kinematics(L1, L2, t1, t2)
        self.ax.plot([x0, x1], [y0, y1], color='blue', lw=7)
        self.ax.plot([x1, x2], [y1, y2], color='red', lw=7)
        self.ax.plot(x0, y0, 'o', color='green', ms=14)
        self.ax.plot(x1, y1, 'ko', ms=8)
        self.ax.plot(x2, y2, '*', color='yellow', ms=25, mec='goldenrod')
        lim = r_max + 2
        self.ax.set(xlim=(-lim, lim), ylim=(-lim, lim), aspect='equal')
        self.ax.grid(ls=':', alpha=0.6)
        self.canvas_plot.draw()
        return x2, y2

    def update_from_sliders(self):
        if self.updating: return
        self.updating = True
        try:
            x, y = self.draw_robot(self.t1_var.get(), self.t2_var.get())
            self.x_var.set(f"{x:.3f}")
            self.y_var.set(f"{y:.3f}")
        finally: self.updating = False

    def update_from_coords(self):
        if self.updating: return
        self.updating = True
        try:
            L1, L2 = float(self.l1_var.get()), float(self.l2_var.get())
            res = H2Q_Lib.H2Q_RR_Inverse_Kinematics(L1, L2, float(self.x_var.get()), float(self.y_var.get()))
            if res[0] is not None:
                limits = [(float(self.t1_min_var.get()), float(self.t1_max_var.get())),
                          (float(self.t2_min_var.get()), float(self.t2_max_var.get()))]
                if all(l[0] <= r <= l[1] for r, l in zip(res, limits)):
                    self.t1_var.set(round(res[0], 1))
                    self.t2_var.set(round(res[1], 1))
                    self.draw_robot(res[0], res[1])
        except: pass
        finally: self.updating = False