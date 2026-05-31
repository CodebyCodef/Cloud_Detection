"""
cloudynight Dataset GÃ¶rÃ¼ntÃ¼leyici
TÃ¼m 20 gÃ¶rÃ¼ntÃ¼yÃ¼ etiketiyle birlikte gÃ¶sterir.
Ã‡alÄ±ÅŸtÄ±r: python goruntu_goster.py
"""
import bz2
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from astropy.io import fits

IMAGES_DIR = "../cloudynight_data/example_data/images"
YTRAIN     = os.path.join(IMAGES_DIR, "y_train.dat")

# --- Etiketleri yÃ¼kle ---
labels = {}
with open(YTRAIN) as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 2:
            continue
        img_id = parts[0]
        flags  = [int(x) for x in parts[1:]]
        cloud_ratio = sum(flags) / len(flags)
        labels[img_id] = (0 if cloud_ratio > 0.5 else 1, round(cloud_ratio * 100))

# --- FITS okuma ---
def read_fits_bz2(path):
    with bz2.open(path, "rb") as f:
        with fits.open(f) as hdul:
            data = hdul[0].data
            if data is None and len(hdul) > 1:
                data = hdul[1].data
            return data.astype(np.float64)

def to_display(data):
    """GÃ¶rÃ¼ntÃ¼yÃ¼ ekranda gÃ¶stermek iÃ§in normalize et."""
    if data.ndim == 3:
        layer = data[0]   # ilk kanalÄ± al
    else:
        layer = data
    m, s = layer.mean(), layer.std()
    clipped = np.clip(layer, m - 2*s, m + 2*s)
    norm = (clipped - clipped.min()) / (clipped.max() - clipped.min() + 1e-9)
    return norm

# --- Ã‡iz ---
files = sorted([f for f in os.listdir(IMAGES_DIR) if f.endswith(".fits.bz2")])

cols = 5
rows = 4
fig, axes = plt.subplots(rows, cols, figsize=(18, 14))
fig.suptitle(
    "cloudynight All-Sky Camera Dataset â€” 20 Gece GÃ¶rÃ¼ntÃ¼sÃ¼\n"
    "ğŸŸ¥ = Bulutlu  |  ğŸŸ© = AÃ§Ä±k GÃ¶kyÃ¼zÃ¼",
    fontsize=14, fontweight="bold", y=0.98
)

for idx, fname in enumerate(files):
    ax = axes[idx // cols][idx % cols]
    img_id = fname.replace(".fits.bz2", "")

    try:
        data = read_fits_bz2(os.path.join(IMAGES_DIR, fname))
        display = to_display(data)
        ax.imshow(display, cmap="gray", origin="lower")
    except Exception as e:
        ax.text(0.5, 0.5, f"Hata\n{e}", ha="center", va="center",
                transform=ax.transAxes, fontsize=7, color="red")

    label, ratio = labels.get(img_id, (None, 0))
    if label == 0:
        color  = "#e74c3c"
        status = f"â˜ï¸  BULUTLU ({ratio}%)"
    elif label == 1:
        color  = "#2ecc71"
        status = f"â­ AÃ‡IK ({100-ratio}% aÃ§Ä±k)"
    else:
        color  = "gray"
        status = "?"

    ax.set_title(f"#{img_id}  {status}", fontsize=8, color=color, fontweight="bold")
    ax.axis("off")

    # Renkli Ã§erÃ§eve
    for spine in ax.spines.values():
        spine.set_edgecolor(color)
        spine.set_linewidth(3)
        spine.set_visible(True)

# BoÅŸ hÃ¼creleri gizle
for idx in range(len(files), rows * cols):
    axes[idx // cols][idx % cols].axis("off")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("../outputs/dataset_ozet.png", dpi=120, bbox_inches="tight")
print("âœ… dataset_ozet.png olarak kaydedildi!")
plt.show()

