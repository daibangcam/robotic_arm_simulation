import os
import sys
import math

def H2Q_get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

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