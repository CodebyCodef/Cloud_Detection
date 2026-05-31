# FITS (Flexible Image Transport System)

## Nedir?
FITS, astronomi görüntüleri için standart dosya formatıdır.

**Neden Önemli?**
- Görüntü verisi + Header (meta veri) tek dosyada
- Bilimsel görüntüleme için optimize edilmiş
- Evrensel olarak kabul görmüş format

---

## FITS Dosya Yapısı

### 1. Header (Başlık)
Meta veri bilgilerini içerir:
```
SIMPLE  =                    T / conforms to FITS standard
BITPIX  =                   16 / number of bits per data pixel
NAXIS   =                    2 / number of data axes
NAXIS1  =                 1024 / length of data axis 1
NAXIS2  =                 1024 / length of data axis 2
DATE-OBS= '2019-11-28T09:52:07' / observation date
TELESCOP= 'All Sky Camera'    / telescope name
...
```

### 2. Data (Veri)
- 2D (gri görüntü) veya 3D (RGB) dizi
- Genellikle 16-bit tam sayı veya 32-bit float

---

## Proje Kodu (dag_cld/ast.py)

### Dosya Okuma

```python
from astropy.io import fits as fts

class Fits:
    def data(self, file):
        """Görüntü verisini oku"""
        hdu = fts.open(file, "readonly")
        d = hdu[0].data
        hdu.close()
        return d.astype(float64)  # float64'e dönüştür

    def header(self, file, field="?"):
        """Header bilgilerini oku"""
        hdu = fts.open(file, mode='readonly')
        header = hdu[0].header
        hdu.close()
        
        if field == "*":
            return header  # Tüm key-value çiftleri
        elif field == "?":
            return header  # Tüm header
        else:
            return header[field]  # Belirli bir alan
```

### Dosya Yazma

```python
def write(self, dest, data, header=None, overwrite=True):
    """Veriyi FITS dosyasına yaz"""
    fts.writeto(dest, data, header=header, overwrite=overwrite)
```

---

## Header İşleme (Proje Örneği)

```python
# main.py'den
header = fts.header(file, field="?")

# Header'a yeni bilgi ekle
header["mask"] = ("20,70,45,135", "Altitude range, Azimut range")
header["mask_d"] = ("N", "Mask Description")
header["IMAGETYP"] = ("IH", "Vector, Hog or Image")

# Yeni dosyaya yaz
fts.write("cikti.fits.gz", data, header=header)
```

---

## Sık Kullanılan Header Alanları

| Alan | Açıklama |
|------|----------|
| `SIMPLE` | FITS standard uyumluluğu |
| `BITPIX` | Pixel başına bit sayısı |
| `NAXIS` | Boyut sayısı (2=2D, 3=3D) |
| `DATE-OBS` | Gözlem tarihi |
| `TELESCOP` | Teleskop adı |
| `INSTRUME` | Enstrüman adı |
| `EXPTIME` | Poz süresi (saniye) |
| `RA` / `DEC` | Sağ açıklık / Dik açıklık |
| `ALT` / `AZ` | Yükseklik / Azimut |

---

## Proje Akışı

```python
# 1. Dosyadan veri oku
data = fts.data("görüntü.fits.gz")

# 2. Header'ı oku
header = fts.header("görüntü.fits.gz", "?")

# 3. İşlem yap
gray = ima.rgb2gray(ima.array2rgb(data))

# 4. Sonucu yeni dosyaya yaz
header["IMAGETYP"] = ("V", "Vector")
fts.write("sonuç.fits.gz", vector, header=header)
```

---

## Sıkıştırma

Proje `.fits.gz` formatı kullanır (gzip sıkıştırmalı):
- Daha küçük dosya boyutu
- Aynı `fts.open()` ile açılır

---

## Kaynaklar

- [Astropy FITS](https://docs.astropy.org/en/stable/io/fits/)
- [FITS Standard](https://fits.gsfc.nasa.gov/fits_standard.html)