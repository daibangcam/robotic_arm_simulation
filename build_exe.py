import PyInstaller.__main__
import os

print("=======================================")
print(" ĐANG TIẾN HÀNH ĐÓNG GÓI PHẦN MỀM...   ")
print("=======================================")

# Khai báo các tham số
pyinstaller_args = [
    'main.py',                           # File code chính
    '--noconsole',                       # Ẩn cửa sổ CMD đen
    '--onefile',                         # Gom tất cả thành 1 file .exe
    '--name=Robotic_Arm_Simulation',     # Tên file exe xuất ra

    '--add-data=img;img',
    '--icon=img/_icon.ico',              # Icon cho chính cái file .exe
    '--clean'                            # Dọn dẹp cache cũ trước khi build để tránh lỗi
]

# Thực thi PyInstaller
try:
    PyInstaller.__main__.run(pyinstaller_args)
    print("\n======================================")
    print(" ĐÓNG GÓI XONG!                         ")
    print(" Nhớ vào thư mục 'dist' để lấy file nha.")
    print(" =======================================")
except Exception as e:
    print(f"\n[LỖI] Quá trình đóng gói thất bại: {e}")