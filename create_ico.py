from PIL import Image

# Mở file hình có sẵn của ní (png hoặc jpg đều được)
img = Image.open("img/_logo.png")

# Lưu lại thành file .ico với kích thước chuẩn 64x64
img.save("_icon.ico", format="ICO", sizes=[(64, 64)])

print("Tạo file _icon.ico thành công rực rỡ!")