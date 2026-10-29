"""
Generate high-resolution vector/PNG QR codes for Page 1, Page 2, Page 3, and Page 4 of the A3 Poster.
"""

import qrcode
import os

out_dir = '/Users/sahilpanchavishe/Desktop/Domestic-Refrigerator-AR-Explorer/poster/renders'
os.makedirs(out_dir, exist_ok=True)

web_url = "https://sahilpanchavishe.github.io/Domestic-Refrigerator-AR-Explorer/"
ar_url = "https://sahilpanchavishe.github.io/Domestic-Refrigerator-AR-Explorer/#ar"

# QR 1: Web Explorer
qr_web = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=12,
    border=2,
)
qr_web.add_data(web_url)
qr_web.make(fit=True)
img_web = qr_web.make_image(fill_color="#070d1e", back_color="#ffffff")
img_web.save(os.path.join(out_dir, "qr_web_explorer.png"))

# QR 2: AR View
qr_ar = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=12,
    border=2,
)
qr_ar.add_data(ar_url)
qr_ar.make(fit=True)
img_ar = qr_ar.make_image(fill_color="#070d1e", back_color="#ffffff")
img_ar.save(os.path.join(out_dir, "qr_ar_view.png"))

print("Generated QR codes successfully!")
