# DAG Cloud Detection — Bulut Tespit Sistemi

Doğu Anadolu Gözlemevi (DAG) all-sky camera görüntülerinden otomatik bulut tespiti.

---

## 📁 Proje Yapısı

```
cloud_detection/
│
├── dag_cld/                        ← ÇEKİRDEK MODÜL (orijinal DAG kodu)
│   ├── ast.py                      │  Görüntü işleme, HOG, astronomi hesapları
│   ├── mask.py                     │  Gökyüzü bölge maskeleme (altaz koordinatlar)
│   ├── teacher.py                  │  ML modelleri: SVM, KNN, LR, NB, CNN
│   └── env.py                      │  Logger, dosya yardımcıları
│
├── notebooks/                      ← TEST & ANALİZ NOTEBOOK'LARI (yeni eklenen)
│   ├── cloudynight_pipeline.ipynb  │  cloudynight FITS verisiyle pipeline testi
│   ├── almeria_pipeline.ipynb      │  Almería JPEG verisiyle HOG + ML testi
│   ├── test_classifiers.ipynb      │  Orijinal sınıflandırıcı testleri
│   └── test_yetenekler.ipynb       │  Orijinal yetenek testleri
│
├── cloudynight_data/               ← DATASET 1: cloudynight (Local)
│   └── example_data/
│       ├── images/                 │  20 adet FITS gece görüntüsü (.fits.bz2)
│       └── features/               │  Hazır özellik dosyaları
│
├── almeria_data/                   ← DATASET 2: Almería (Local)
│   ├── kontas_2017/
│   │   ├── images/                 │  770 JPEG all-sky gündüz görüntüsü
│   │   └── seg_masks/              │  770 PNG segmentasyon maskesi
│   └── test_set/                   │  48 test görüntüsü
│
├── outputs/                        ← ÇIKTI GÖRSELLERİ 
│   ├── almeria_sonuclar.png        │  Model karşılaştırma grafiği
│   ├── almeria_hog.png             │  HOG görselleştirmesi
│   ├── almeria_ornekler.png        │  Örnek görüntü + maskeler
│   ├── model_karsilastirma.png     │  cloudynight model karşılaştırması
│   └── ...
│
├── scripts/                        ← YARDIMCI SCRIPTLER 
│   └── goruntu_goster.py           │  cloudynight görüntülerini göster
│
├── main.py                         ← ANA PIPELINE (orijinal DAG kodu)
├── requirements.txt                ← Bağımlılıklar
└── README.md                       ← Bu dosya
```

---

## 🧩 Modüller

### `dag_cld/` — Orijinal DAG Sistemi

| Dosya | İçerik |
|-------|--------|
| `ast.py` | HOG özellik çıkarımı, FITS okuma, RGB dönüşümleri, astropy entegrasyonu |
| `mask.py` | Polar koordinat tabanlı gökyüzü bölge maskeleme (E/S/W/N/ZE/ZS/ZW/ZN) |
| `teacher.py` | SVM, KNN, Logistic Regression, Naive Bayes, CNN sınıflandırıcıları |
| `env.py` | Loglama ve dosya işlemleri |

### `notebooks/` — Test Notebook'ları

| Notebook | Veri | Amaç |
|----------|------|-------|
| `cloudynight_pipeline.ipynb` | 20 FITS gece görüntüsü | Pipeline format uyumluluk testi |
| `almeria_pipeline.ipynb` | 818 JPEG gündüz görüntüsü | HOG + ML performans testi |

---

## 📊 Test Sonuçları (Almería Dataset)

> 616 eğitim / 154 test görüntüsü, HOG 128×128 px

| Model | Accuracy | F1 Score |
|-------|----------|----------|
| **LR** (Logistic Regression) | **0.8766** | **0.8769** |
| KNN | 0.8701 | 0.8695 |
| SVM | 0.8506 | 0.8510 |
| NB (Gaussian) | 0.7727 | 0.7783 |

---

## 🌍 Neden DAG Koordinatları?

```python
lat = 41.2333°N  # Enlem
lon = 39.7833°E  # Boylam
ele = 3170 m     # Rakım (Kaçkar Dağları)
```

`astroplan.Observer` bu koordinatları kullanarak her görüntü için:
- Güneş ve Ay'ın ufuk açısını hesaplar
- Gün batımı / astronomik alacakaranlık saatini belirler
- Görüntünün **gece mi / gündüz mü** çekildiğine karar verir

Yanlış koordinat → yanlış gece/gündüz ayrımı → modelin yanlış örneklerle eğitilmesi.

---

## 🚀 Kullanım

```bash
# Sanal ortamı aktive et
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac

# Almería pipeline'ı çalıştır
jupyter notebook notebooks/almeria_pipeline.ipynb

# cloudynight pipeline'ı çalıştır
jupyter notebook notebooks/cloudynight_pipeline.ipynb

# Görüntüleri görselleştir
python scripts/goruntu_goster.py
```

---

## 📚 Kaynaklar

- **DAG Gözlemevi**: https://dag.erzurum.edu.tr
- **cloudynight dataset**: Mommert (2020), *The Astronomical Journal*, 159. [DOI](https://doi.org/10.3847/1538-3881/ab744f)
- **Almería dataset**: Fabel et al. (2022), *Atmospheric Measurement Techniques*, 15. [DOI](https://doi.org/10.5194/amt-15-797-2022)
