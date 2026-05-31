# 3. Görüntü İşleme Araçları

## Genel Bakış
Bu bölümde projede kullanılan görüntü işleme kütüphanelerini öğreneceğiz:
- **PIL (Pillow)**: Maskeleme
- **OpenCV (cv2)**: Boyutlandırma
- **Matplotlib**: Görselleştirme
- **sep**: Yıldız tespiti

---

## 1. PIL (Pillow) - Maskeleme

Görüntü oluşturma ve çizim işlemleri için kullanılır.

### Proje Kodu (mask.py):

```python
from PIL.ImageDraw import Draw as PIDraw
from PIL.Image import new as PInew
```

### Geometric Mask (Poligon):

```python
class Geometric(Mask):
    def polygon(self, shape, points, rev=False):
        """Poligonal maske oluştur"""
        # Boş siyah görüntü oluştur
        img = PInew('L', (shape[1], shape[0]), 0)
        
        # Poligon çiz
        PIDraw(img).polygon(points, outline=1, fill=1)
        
        # Numpy dizisine çevir
        mask = ar(img)
        
        # Boolean maske
        the_mask = mask == 1
        
        if rev:
            return lnot(the_mask)  # Tersine çevir
        else:
            return the_mask
```

### Kullanım:

```python
from PIL import Image, ImageDraw

# 100x100 siyah görüntü
img = Image.new('L', (100, 100), 0)

# Üçgen çiz
draw = ImageDraw.Draw(img)
draw.polygon([(50, 0), (0, 100), (100, 100)], fill=1)

# Numpy dizisine çevir
import numpy as np
mask = np.array(img)
```

---

## 2. OpenCV (cv2) - Boyutlandırma

Görüntü yeniden boyutlandırma için kullanılır.

### Proje Kodu (ast.py):

```python
from cv2 import resize as cvresize

class Image:
    def resize(self, array, new_size):
        """2D diziyi yeniden boyutlandır"""
        
        if "%" in new_size:
            # Yüzde ile boyutlandırma
            h, w = array.shape
            multiplier = int(new_size.replace("%", "").strip()) / 100
            new_size = (int(w * multiplier), int(h * multiplier))
            return cvresize(array, new_size)
        
        else:
            # Sabit boyut
            if type(new_size) == int:
                new_size = (new_size, new_size)
            return cvresize(array, new_size)
```

### Kullanım:

```python
import cv2

# Görüntüyü yükle
img = cv2.imread('gorsel.jpg', cv2.IMREAD_GRAYSCALE)

# Boyutlandırma yöntemleri

# 1. Yüzde ile
# 25% boyutuna küçült
boyut = (int(img.shape[1] * 0.25), int(img.shape[0] * 0.25))
kucuk = cv2.resize(img, boyut)

# 2. Sabit boyut
# 64x64 piksel
kucuk = cv2.resize(img, (64, 64))

# 3. Belirli bir genişlik (yükseklik otomatik)
genislik = 100
oran = genislik / img.shape[1]
yukseklik = int(img.shape[0] * oran)
yeniden = cv2.resize(img, (genislik, yukseklik))
```

### Proje Kullanımı:

```python
# main.py'den
gray = ima.resize(ima.rgb2gray(ima.array2rgb(data)), "25%")
# Görüntüyü %25 boyutuna küçült
```

---

## 3. Matplotlib - Görselleştirme

Görüntüleri ve grafikleri göstermek için kullanılır.

### Proje Kodu (ast.py - Image.show()):

```python
from matplotlib import pyplot as plt

class Image:
    def show(self, array, add_points=None):
        """Görüntüyü göster"""
        m, s = mean(array), std(array)
        
        if add_points is not None:
            colors = ["red", "green", "blue", "cyan"]
            for it, point in enumerate(add_points):
                plt.scatter(point[0], point[1], s=20, c=colors[it])
        
        plt.imshow(array, cmap="Greys_r", interpolation='nearest',
                   vmin=m - s, vmax=m + s, origin='lower')
        plt.axis('off')
        plt.show()
```

### Proje Kodu (ast.py - HOG görselleştirme):

```python
def hog(self, image, show=False, mchannel=True):
    """HOG görselleştirme"""
    if show:
        _, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4),
                                     sharex=True, sharey=True)
        
        ax1.axis('off')
        ax1.imshow(self.normalize(image), cmap=plt.cm.gray)
        ax1.set_title('Input image')
        
        # Histogramı daha iyi göstermek için yeniden ölçekle
        hog_image_rescaled = ri(hog_image, in_range=(0, 10))
        
        ax2.axis('off')
        ax2.imshow(hog_image_rescaled, cmap=plt.cm.gray)
        ax2.set_title('Histogram of Oriented Gradients')
        plt.show()
```

### Kullanım:

```python
import matplotlib.pyplot as plt

# Basit görüntü gösterme
plt.imshow(goruntu, cmap='gray')
plt.show()

# Renkli görüntü
plt.imshow(goruntu)  # Varsayılan cmap
plt.colorbar()       # Renk çubuğu ekle
plt.title("Başlık")
plt.axis('off')      # Eksenleri gizle
plt.show()

# Alt çizimler (subplot)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
ax1.imshow(img1, cmap='gray')
ax2.imshow(img2, cmap='gray')
plt.show()
```

---

## 4. sep - Yıldız Tespiti

Source Extraction and Photometry - Yıldız/kaynak tespiti.

### Proje Kodu (ast.py):

```python
import sep

class Fits:
    def star_finder(self, data, threshold=10, bkgext=True):
        """Görüntüdeki yıldızları bul"""
        
        # Arka plan çıkarma
        if bkgext:
            bkg = self.background(data)
            data = data - bkg
        
        # Kaynak çıkarma
        coords = extract(data, threshold)
        
        # Tablo oluştur ve parlaklığa göre sırala
        t = Table(coords)
        t.sort("flux", reverse=True)
        
        return t
```

### Kullanım:

```python
import sep
import numpy as np

# Veri (2D numpy dizisi)
data = np.random.rand(100, 100)

# Arka plan tahmini
bkg = sep.Background(data)
print(bkg.globalback)  # Global arka plan seviyesi
print(bkg.globalrms)   # Global RMS

# Arka plan çıkarılmış veri
data_sub = data - bkg

# Yıldız tespiti (eşik değeri 10)
objects = sep.extract(data_sub, 10)

# Sonuçları incele
print(len(objects))  # Bulunan yıldız sayısı
print(objects['x'], objects['y'])  # Koordinatlar
print(objects['flux'])  # Parlaklıklar
```

### Çıktı Alanları:

| Alan | Açıklama |
|------|----------|
| `x`, `y` | Piksel koordinatları |
| `flux` | Parlaklık |
| `peak` | Tepe değeri |
| `xc`, `yc` | Merkez koordinatları |
| `a`, `b` | Yarı eksenler |
| `theta` | Yönelim açısı |

---

## 5. NumPy - Temel İşlemler

Projede sık kullanılan NumPy işlemleri.

### Proje Kodu (ast.py - find_window):

```python
def find_window(self, array):
    """Maskelenmiş veride en iyi pencereyi bul"""
    result = where(array > 0)
    x_min = result[0].min()
    x_max = result[0].max()
    y_min = result[1].min()
    y_max = result[1].max()
    return array[x_min:x_max, y_min:y_max]
```

### Proje Kodu (mask.py - Polar maske):

```python
from numpy import deg2rad, rad2deg, arctan2, arccos
from numpy import cos, sin, sqrt, power, pi
from numpy import ogrid
from numpy import logical_not as lnot

class Polar(Mask):
    def pizza(self, shape, angle_range, ...):
        """Pizza dilimi şeklinde maske"""
        
        # Koordinat ızgarası oluştur
        w, h = shape
        x, y = ogrid[:w, :h]
        
        # Polar koordinatlara dönüşüm
        r2 = (x - cx) * (x - cx) + (y - cy) * (y - cy)
        theta = arctan2(x - cx, y - cy) - tmin
        
        # Maske oluştur
        circmask = r2 <= radius * radius
        anglemask = theta <= (tmax - tmin)
        the_mask = circmask * anglemask
```

---

## 6. scikit-image - Görüntü İşleme

HOG, RGB dönüşümü, histogram eşitleme.

### Proje Kodu (ast.py):

```python
from skimage.color import rgb2gray as r2g
from skimage.feature import hog as the_hog
from skimage.exposure import rescale_intensity as ri

class Image:
    def rgb2gray(self, rgb):
        """RGB'den gri tonlamaya"""
        return r2g(rgb)
    
    def hog(self, image, ...):
        """HOG özellik çıkarımı"""
        return the_hog(image, ...)
```

### Kullanım:

```python
from skimage import data
from skimage.color import rgb2gray
from skimage.feature import hog
from skimage.exposure import rescale_intensity

# Görüntü yükle
img = data.astronaut()

# Gri tonlama
gray = rgb2gray(img)

# HOG özellik çıkarımı
features, hog_image = hog(gray, orientations=8,
                          pixels_per_cell=(16, 16),
                          cells_per_block=(1, 1),
                          visualize=True)

# Histogram eşitleme
equalized = rescale_intensity(hog_image, in_range=(0, 10))
```

---

## Proje İçinde Kullanım (main.py)

```python
# Maskeleme
mask_coordinates = {"N": ((20, 70), (315, 405))}
the_mask = pmask.altaz(gray.shape, coordinates[0], coordinates[1], rev=True)
masked_data = pmask.apply(gray, the_mask)

# Pencere bulma
windowed_masked_data = ima.find_window(masked_data)

# Boyutlandırma
gray = ima.resize(gray, "25%")

# HOG özellik çıkarımı
vec, hog_im = ima.hog(windowed_masked_data, mchannel=False)

# Gösterme
ima.show(hog_im)

# Yıldız tespiti
stars = fts.star_finder(data, threshold=10)
```

---

## Özet Tablo

| Kütüphane | Sınıf/Fonksiyon | İşlev |
|-----------|-----------------|-------|
| **PIL** | `Image.new`, `ImageDraw` | Maskeleme, poligon çizimi |
| **OpenCV** | `cv2.resize` | Görüntü boyutlandırma |
| **Matplotlib** | `plt.imshow`, `plt.show` | Görselleştirme |
| **sep** | `sep.Background`, `sep.extract` | Arka plan, yıldız tespiti |
| **scikit-image** | `rgb2gray`, `hog`, `rescale_intensity` | Dönüşümler, HOG |
| **NumPy** | `where`, `ogrid`, `sin/cos` | Temel dizi işlemleri |

---

## Kaynaklar

- [Pillow Documentation](https://pillow.readthedocs.io/)
- [OpenCV Python Tutorial](https://docs.opencv.org/4.5.2/d6/d00/tutorial_py_root.html)
- [Matplotlib Tutorial](https://matplotlib.org/stable/tutorials/introductory/pyplot.html)
- [sep Documentation](https://sep.readthedocs.io/)
- [scikit-image](https://scikit-image.org/)