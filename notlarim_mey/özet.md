# 🌩️ Proje: Cloud Detection (Bulut Tespiti)

Bu proje, **All Sky Camera (ASC)** kullanarak gökyüzündeki bulutları tespit etmek için geliştirilmiş bir Python kütüphanesidir. Proje, makine öğrenmesi ve derin öğrenme yöntemlerini kullanarak bulut/bulutsuz sınıflandırması yapmaktadır.

---

## 📚 Kullanılan Teknolojiler

### 1. **Makine Öğrenmesi (Machine Learning)**

| Kütüphane | Kullanım Amacı |
|-----------|----------------|
| **scikit-learn** | ML algoritmaları için temel kütüphane |

#### Kullanılan Sınıflandırıcılar:

| Algoritma | Dosya | Amaç |
|-----------|-------|------|
| **SVM** (Support Vector Machine) | `teacher.py` | HOG vektörlerinden bulut tespiti |
| **KNN** (K-Nearest Neighbors) | `teacher.py` | Komşu bazlı sınıflandırma |
| **LR** (Logistic Regression) | `teacher.py` | Lojistik regresyon ile sınıflandırma |
| **NB** (Naive Bayes) | `teacher.py` | 5 farklı tip (Gaussian, Bernoulli, Categorical, Complement, Multinomial) |

---

### 2. **Derin Öğrenme (Deep Learning)**

| Kütüphane | Kullanım Amacı |
|-----------|----------------|
| **TensorFlow/Keras** | CNN (Convolutional Neural Network) modeli |

#### CNN Mimarisi (`teacher.py` içinde):
```
Input → Conv2D(256) → ReLU → MaxPool → Conv2D(256) → ReLU → MaxPool
→ Flatten → Dense(64) → Dense(1) → Sigmoid
```
- **Loss Function:** `binary_crossentropy`
- **Optimizer:** `adam`
- **Epoch:** 50 (varsayılan)

---

### 3. **Görüntü İşleme (Image Processing)**

| Kütüphane | Kullanım Amacı |
|-----------|----------------|
| **OpenCV (cv2)** | Görüntü yeniden boyutlandırma |
| **scikit-image** | RGB→Grayscale, HOG özellik çıkarımı |

#### Önemli Fonksiyonlar:
- `rgb2gray()` - RGB'den gri tonlamaya dönüştürme
- `hog()` - Histogram of Oriented Gradients (HOG) özellik çıkarımı
  - `orientations=8`
  - `pixels_per_cell=(16, 16)`
  - `cells_per_block=(1, 1)`
- `rescale_intensity()` - Histogram eşitleme
- `resize()` - Görüntü boyutlandırma

---

### 4. **Astronomi Kütüphaneleri**

| Kütüphane | Kullanım Amacı |
|-----------|----------------|
| **astropy** | FITS dosyaları, koordinat sistemleri, zaman hesaplamaları |
| **astroplan** | Gözlemevi hesaplamaları (güneş/ay doğuşu, gece zamanı) |

#### Astropy Modülleri:
- `astropy.io.fits` - FITS dosya okuma/yazma
- `astropy.coordinates` - Koordinat sistemleri (AltAz, EarthLocation, SkyCoord)
- `astropy.time` - JD hesaplamaları
- `astropy.stats` - Histogram
- `astroplan.Observer` - Gözlemevi zaman hesaplamaları

---

### 5. **Astronomi Görüntü Formatı**

| Format | Açıklama |
|--------|-----------|
| **FITS** (Flexible Image Transport System) | Astronomi görüntüleri için standart format |

Kullanım: `fts.write()`, `fts.data()`, `fts.header()`

---

### 6. **Bilimsel Hesaplama**

| Kütüphane | Kullanım Amacı |
|-----------|----------------|
| **NumPy** | Diziler, matematiksel işlemler |
| **PIL (Pillow)** | Geometrik mask oluşturma |

---

### 7. **Görselleştirme**

| Kütüphane | Kullanım Amacı |
|-----------|----------------|
| **Matplotlib** | HOG görselleştirme, eğitim grafikleri |

---

### 8. **Diğer Araçlar**

| Kütüphane | Kullanım Amacı |
|-----------|----------------|
| **sep** (Source Extraction and Photometry) | Yıldız tespiti ve fotometri |
| **joblib** | Model kaydetme/yükleme |

---

## 🏗️ Proje Mimarisi

```
cloud_detection/
├── main.py                 # Ana çalıştırma dosyası
├── dag_cld/                # Ana modül
│   ├── __init__.py
│   ├── env.py             # Logger ve dosya işlemleri
│   ├── ast.py             # Astronomi/görüntü işleme sınıfları
│   ├── mask.py            # Polar/Geometrik maske üretimi
│   └── teacher.py         # ML/DL sınıflandırıcılar
├── test_classifiers.ipynb # Sınıflandırıcı testleri
└── test_yetenekler.ipynb   # Yetenek testleri
```

---

## 🔄 Proje Akışı

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  FITS Dosyaları │ -> │  Maskeleme      │ -> │  HOG Özellik    │
│  (Görüntüler)   │    │  (Polar/AltAz)  │    │  Çıkarımı       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                    |
                                                    v
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Sınıflandırma  │ <- │  Eğitim/Test    │ <- │  Veri Hazırlama  │
│  (SVM/CNN/KNN)  │    │  (Train/Test)   │    │  (Shuffle/Split)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 📝 Önemli Sınıflar

| Sınıf | Dosya | İşlev |
|-------|-------|-------|
| `Logger` | env.py | Logging ve sistem bilgisi |
| `File` | env.py | Dosya işlemleri |
| `Image` | ast.py | Görüntü işleme (HOG, grayscale, resize) |
| `Fits` | ast.py | FITS dosya okuma/yazma |
| `Time`, `TimeCalc` | ast.py | Zaman hesaplamaları |
| `Site` | ast.py | Gözlemevi konumu |
| `Polar` | mask.py | Polar koordinat maske üretimi |
| `SVM`, `CNN`, `KNN`, `LR`, `NB` | teacher.py | ML sınıflandırıcılar |

---

