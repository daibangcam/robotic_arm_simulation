import os
import sys
import math


def H2Q_get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ==========================================
# ROBOT RR (2 BẬC 2D)
# ==========================================
def H2Q_RR_Forward_Kinematics(L1, L2, th1_deg, th2_deg):
    th1 = math.radians(th1_deg)
    th2 = math.radians(th2_deg)
    x0, y0 = 0, 0
    x1 = L1 * math.cos(th1)
    y1 = L1 * math.sin(th1)
    x2 = x1 + L2 * math.cos(th1 + th2)
    y2 = y1 + L2 * math.sin(th1 + th2)
    return x0, y0, x1, y1, x2, y2


def H2Q_RR_Inverse_Kinematics(L1, L2, x, y):
    cos_t2 = (x ** 2 + y ** 2 - L1 ** 2 - L2 ** 2) / (2 * L1 * L2)
    if -1.0 <= cos_t2 <= 1.0:
        sin_t2 = math.sqrt(1 - cos_t2 ** 2)
        th2 = math.atan2(sin_t2, cos_t2)
        k1 = L1 + L2 * cos_t2
        k2 = L2 * sin_t2
        th1 = math.atan2(y, x) - math.atan2(k2, k1)
        return math.degrees(th1), math.degrees(th2)
    return None, None


# ==========================================
# ROBOT RRR-1 (3 BẬC MẶT PHẲNG 2D)
# ==========================================
def H2Q_RRR_Forward_Kinematics(L1, L2, L3, th1_deg, th2_deg, th3_deg):
    th1 = math.radians(th1_deg)
    th2 = math.radians(th2_deg)
    th3 = math.radians(th3_deg)
    phi_rad = th1 + th2 + th3

    x0, y0 = 0, 0
    x1 = L1 * math.cos(th1)
    y1 = L1 * math.sin(th1)
    x2 = x1 + L2 * math.cos(th1 + th2)
    y2 = y1 + L2 * math.sin(th1 + th2)
    x3 = x2 + L3 * math.cos(phi_rad)
    y3 = y2 + L3 * math.sin(phi_rad)

    return x0, y0, x1, y1, x2, y2, x3, y3, phi_rad


def H2Q_RRR_Inverse_Kinematics(L1, L2, L3, x, y, phi_deg):
    phi_rad = math.radians(phi_deg)
    xw = x - L3 * math.cos(phi_rad)
    yw = y - L3 * math.sin(phi_rad)

    cos_t2 = (xw ** 2 + yw ** 2 - L1 ** 2 - L2 ** 2) / (2 * L1 * L2)
    if -1.0 <= cos_t2 <= 1.0:
        sin_t2 = math.sqrt(1 - cos_t2 ** 2)
        th2 = math.atan2(sin_t2, cos_t2)
        k1 = L1 + L2 * cos_t2
        k2 = L2 * sin_t2
        th1 = math.atan2(yw, xw) - math.atan2(k2, k1)
        th3 = phi_rad - th1 - th2
        return math.degrees(th1), math.degrees(th2), math.degrees(th3)
    return None, None, None


# ==========================================
# ROBOT RRR-2 (3 BẬC KHÔNG GIAN 3D)
# ==========================================
def H2Q_RRR_3D_Forward_Kinematics(L1, L2, L3, th1_deg, th2_deg, th3_deg):
    th1 = math.radians(th1_deg)
    th2 = math.radians(th2_deg)
    th3 = math.radians(th3_deg)

    # Tọa độ gốc
    x0, y0, z0 = 0, 0, 0
    # Tọa độ khớp vai (Chỉ có chiều cao L1)
    x1, y1, z1 = 0, 0, L1

    # Tọa độ khớp cùi chỏ
    r2 = L2 * math.cos(th2)
    z2 = L1 + L2 * math.sin(th2)
    x2 = r2 * math.cos(th1)
    y2 = r2 * math.sin(th1)

    # Tọa độ đầu công tác
    r3 = r2 + L3 * math.cos(th2 + th3)
    z3 = z2 + L3 * math.sin(th2 + th3)
    x3 = r3 * math.cos(th1)
    y3 = r3 * math.sin(th1)

    return (x0, y0, z0), (x1, y1, z1), (x2, y2, z2), (x3, y3, z3)


def H2Q_RRR_3D_Inverse_Kinematics(L1, L2, L3, x, y, z):
    # Xoay quanh trục Z (Khớp 1)
    th1 = math.atan2(y, x)

    # Bán kính trên mặt phẳng XY
    r = math.sqrt(x ** 2 + y ** 2)
    # Chiều cao tương đối so với khớp vai
    Z = z - L1

    # Giải bài toán 2D cho vai và cùi chỏ
    cos_t3 = (r ** 2 + Z ** 2 - L2 ** 2 - L3 ** 2) / (2 * L2 * L3)
    if -1.0 <= cos_t3 <= 1.0:
        # Chọn nghiệm cùi chỏ hướng xuống
        sin_t3 = -math.sqrt(1 - cos_t3 ** 2)
        th3 = math.atan2(sin_t3, cos_t3)

        k1 = L2 + L3 * cos_t3
        k2 = L3 * sin_t3
        th2 = math.atan2(Z, r) - math.atan2(k2, k1)

        return math.degrees(th1), math.degrees(th2), math.degrees(th3)
    return None, None, None