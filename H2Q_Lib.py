import os
import sys
import math

def H2Q_get_resource_path(relative_path):
    try: base_path = sys._MEIPASS
    except Exception: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ==========================================
# ROBOT RR (2 BẬC MẶT PHẲNG 2D)
# ==========================================
def H2Q_RR_Forward_Kinematics(L1, L2, th1_deg, th2_deg):
    th1, th2 = math.radians(th1_deg), math.radians(th2_deg)
    x0, y0 = 0, 0
    x1, y1 = L1 * math.cos(th1), L1 * math.sin(th1)
    x2, y2 = x1 + L2 * math.cos(th1 + th2), y1 + L2 * math.sin(th1 + th2)
    return x0, y0, x1, y1, x2, y2

def H2Q_RR_Inverse_Kinematics(L1, L2, x, y):
    cos_t2 = (x ** 2 + y ** 2 - L1 ** 2 - L2 ** 2) / (2 * L1 * L2)
    if -1.0 <= cos_t2 <= 1.0:
        sin_t2 = math.sqrt(1 - cos_t2 ** 2)
        th2 = math.atan2(sin_t2, cos_t2)
        k1, k2 = L1 + L2 * cos_t2, L2 * sin_t2
        th1 = math.atan2(y, x) - math.atan2(k2, k1)
        return math.degrees(th1), math.degrees(th2)
    return None, None

# ==========================================
# ROBOT RR-3D (2 BẬC KHÔNG GIAN)
# ==========================================
def H2Q_RR_3D_Forward_Kinematics(L1, L2, th1_deg, th2_deg):
    th1, th2 = math.radians(th1_deg), math.radians(th2_deg)
    # Tọa độ các điểm khớp
    x0, y0, z0 = 0, 0, 0
    x1, y1, z1 = 0, 0, L1

    r2 = L2 * math.cos(th2)
    x2 = r2 * math.cos(th1)
    y2 = r2 * math.sin(th1)
    z2 = L1 + L2 * math.sin(th2)

    return (x0, y0, z0), (x1, y1, z1), (x2, y2, z2)

def H2Q_RR_3D_Inverse_Kinematics(L1, L2, x, y, z):
    # Tính Theta 1
    th1 = math.atan2(y, x)

    # Kiểm tra xem điểm có nằm trên mặt cầu bán kính L2 tâm (0,0,L1) không
    r = math.sqrt(x ** 2 + y ** 2)
    z_rel = z - L1
    dist_sq = r ** 2 + z_rel ** 2

    # Cho phép sai số nhỏ do làm tròn
    if abs(math.sqrt(dist_sq) - L2) > 0.01:
        return None, None

    # Tính Theta 2
    th2 = math.atan2(z_rel, r)

    return math.degrees(th1), math.degrees(th2)

# ==========================================
# ROBOT RRR (3 BẬC MẶT PHẲNG 2D)
# ==========================================
def H2Q_RRR_Forward_Kinematics(L1, L2, L3, th1_deg, th2_deg, th3_deg):
    th1, th2, th3 = math.radians(th1_deg), math.radians(th2_deg), math.radians(th3_deg)
    phi_rad = th1 + th2 + th3
    x0, y0 = 0, 0
    x1, y1 = L1 * math.cos(th1), L1 * math.sin(th1)
    x2, y2 = x1 + L2 * math.cos(th1 + th2), y1 + L2 * math.sin(th1 + th2)
    x3, y3 = x2 + L3 * math.cos(phi_rad), y2 + L3 * math.sin(phi_rad)
    return x0, y0, x1, y1, x2, y2, x3, y3, phi_rad

def H2Q_RRR_Inverse_Kinematics(L1, L2, L3, x, y, phi_deg):
    phi_rad = math.radians(phi_deg)
    xw, yw = x - L3 * math.cos(phi_rad), y - L3 * math.sin(phi_rad)
    cos_t2 = (xw ** 2 + yw ** 2 - L1 ** 2 - L2 ** 2) / (2 * L1 * L2)
    if -1.0 <= cos_t2 <= 1.0:
        sin_t2 = math.sqrt(1 - cos_t2 ** 2)
        th2 = math.atan2(sin_t2, cos_t2)
        k1, k2 = L1 + L2 * cos_t2, L2 * sin_t2
        th1 = math.atan2(yw, xw) - math.atan2(k2, k1)
        th3 = phi_rad - th1 - th2
        return math.degrees(th1), math.degrees(th2), math.degrees(th3)
    return None, None, None

# ==========================================
# ROBOT RRR-3D (3 BẬC KHÔNG GIAN)
# ==========================================
def H2Q_RRR_3D_Forward_Kinematics(L1, L2, L3, th1_deg, th2_deg, th3_deg):
    th1, th2, th3 = math.radians(th1_deg), math.radians(th2_deg), math.radians(th3_deg)
    x0, y0, z0 = 0, 0, 0
    x1, y1, z1 = 0, 0, L1
    r2, z2 = L2 * math.cos(th2), L1 + L2 * math.sin(th2)
    x2, y2 = r2 * math.cos(th1), r2 * math.sin(th1)
    r3, z3 = r2 + L3 * math.cos(th2 + th3), z2 + L3 * math.sin(th2 + th3)
    x3, y3 = r3 * math.cos(th1), r3 * math.sin(th1)
    return (x0, y0, z0), (x1, y1, z1), (x2, y2, z2), (x3, y3, z3)

def H2Q_RRR_3D_Inverse_Kinematics(L1, L2, L3, x, y, z):
    th1 = math.atan2(y, x)
    r, Z_rel = math.sqrt(x ** 2 + y ** 2), z - L1
    cos_t3 = (r ** 2 + Z_rel ** 2 - L2 ** 2 - L3 ** 2) / (2 * L2 * L3)
    if -1.0 <= cos_t3 <= 1.0:
        sin_t3 = -math.sqrt(1 - cos_t3 ** 2)
        th3 = math.atan2(sin_t3, cos_t3)
        k1, k2 = L2 + L3 * cos_t3, L3 * sin_t3
        th2 = math.atan2(Z_rel, r) - math.atan2(k2, k1)
        return math.degrees(th1), math.degrees(th2), math.degrees(th3)
    return None, None, None