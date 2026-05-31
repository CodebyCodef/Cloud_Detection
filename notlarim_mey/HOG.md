# HOG (Histogram of Oriented Gradients)

## Nedir?
HOG, görüntüdeki kenarları ve yönelimleri analiz ederek özellik çıkaran bir tekniktir. 

**Neden Önemli?**
- Bulutların kenarları düzgün olmayan şekiller oluşturur
- Gökyüzü (bulutsuz) düzgün gradyanlara sahiptir
- Bu fark, sınıflandırma için güçlü bir özellik sağlar

---

## Nasıl Çalışır?

### Adım 1: Ön İşleme
- Görüntüyü gri tonlamaya çevir
- Boyutu normalize et

### Adım 2: Gradyan Hesaplama
- Her piksel için yatay (Gx) ve dikey (Gy) gradyanları hesapla
- `Gx = I(x+1, y) - I(x-1, y)`
- `Gy = I(x, y+1) - I(x, y-1)`

### Adım 3: Magnitude ve Yön
- **Magnitude**: `sqrt(Gx² + Gy²)` - Kenar gücü
- **Yön**: `atan2(Gy, Gx)` - Kenar yönelimi (0-180° veya 0-360°)

### Adım 4: Hücrelere Bölme
- Görüntüyü hücrelere böl (örn: 16x16 piksel)
- Her hücrede yön histogramı oluştur

### Adım 5: Blok Normalizasyon
- Komşu hücreleri birleştir
- L2 norm ile normalizasyon yap

---

## Proje Kodu (dag_cld/ast.py)

```python
from skimage.feature import hog

def hog(self, image, show=False, mchannel=True):
    """Histogram of Oriented Gradients"""
    fd, hog_image = the_hog(image, 
                            orientations=8,          # 8 yönelim (0°, 45°, 90°, ...)
                            pixels_per_cell=(16, 16), # Hücre boyutu
                            cells_per_block=(1, 1),   # Blok boyutu
                            visualize=True,
                            multichannel=mchannel)
    
    if show:
        # Görselleştirme için matplotlib kullan
        _, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
        ax1.imshow(self.normalize(image), cmap=plt.cm.gray)
        ax2.imshow(hog_image, cmap=plt.cm.gray)
        plt.show()
    
    return fd, hog_image
```

### Parametreler:
| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| `orientations` | 8 | Gradyan yönü sayısı |
| `pixels_per_cell` | (16, 16) | Her hücredeki piksel sayısı |
| `cells_per_block` | (1, 1) | Normalizasyon için blok boyutu |
| `multichannel` | False | Gri tonlama için False |

---

## HOG Özellik Vektörü

Çıktı olarak bir vektör elde edilir:
- **Boyut**: (orientations × cells_per_block × hücre_sayısı)
- Bu vektör, ML modellerine girdi olarak verilir

---

## Bulut Tespitte Kullanım

```python
# main.py'den
gray = ima.rgb2gray(ima.array2rgb(data))  # Gri tonlama
masked_data = pmask.apply(gray, mask)     # Maskeleme
windowed_masked_data = ima.find_window(masked_data)  # Pencereleme
vec, hog_im = ima.hog(windowed_masked_data, mchannel=False)  # HOG
```

### Akış:
1. FITS dosyasından veri oku
2. Polar maske uygula (sadece ilgilenilen bölge)
3. Pencerele (sınırı belirle)
4. HOG özelliklerini çıkar
5. ML modeline ver

---

## Kaynaklar

- [scikit-image HOG](https://scikit-image.org/docs/stable/auto_examples/features_detection/plot_hog.html)
- [Dalal & Triggs (2005)](https://ieeexplore.ieee.org/document/1565186/) - HOG'un orijinal makalesi