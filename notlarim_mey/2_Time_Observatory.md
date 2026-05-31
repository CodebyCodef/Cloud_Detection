# 2. Zaman & Gözlemevi Hesaplamaları

## Genel Bakış
Bu bölümde `astropy.time` ve `astroplan` kütüphanelerini kullanarak zaman hesaplamalarını ve gözlemevi işlemlerini öğreneceğiz.

---

## Kullanılan Kütüphaneler

```python
from datetime import datetime          # Python datetime
from datetime import timedelta          # Zaman farkı hesaplama

from astropy.time import Time           # Astropy zaman nesnesi
from astropy.time import Time as tm     # Kısa alias
from astroplan import Observer          # Gözlemevi yöneticisi
from astroplan import download_IERS_A    # IERS verilerini indir
from math import floor                  # Tam sayı kısmı
```

---

## 1. Time - Zaman Nesnesi

Astronomik zaman hesaplamaları için kullanılır.

### Proje Kodu (ast.py - Time sınıfı):

```python
class Time:
    def __init__(self, logger):
        self.logger = logger

    def str2time(self, time, FORMAT='%Y-%m-%dT%H:%M:%S.%f'):
        """String'i datetime nesnesine dönüştür"""
        datetime_object = datetime.strptime(time, FORMAT)
        return datetime_object

    def time_diff(self, time, time_offset=-3, offset_type="hours"):
        """Zaman farkı hesapla (UTC offset)"""
        if time is not None and time_offset is not None:
            if "HOURS".startswith(offset_type.upper()):
                return time + timedelta(hours=time_offset)
            elif "MINUTES".startswith(offset_type.upper()):
                return time + timedelta(minutes=time_offset)
            elif "SECONDS".startswith(offset_type.upper()):
                return time + timedelta(seconds=time_offset)
        return None

    def jd(self, utc):
        """Julian Date hesapla"""
        t = tm(utc, scale='utc')
        return t.jd

    def jd_r(self, jd):
        """Julian Date'i datetime'a dönüştür"""
        t = tm(jd, format='jd', scale='tai')
        return t.to_datetime()
```

### Kullanım:

```python
from astropy.time import Time

# String'den Time nesnesi
t = Time("2019-11-28 09:52:07")
print(t.jd)  # Julian Date: 2458815.91...

# Time nesnesinden datetime
dt = t.to_datetime()

# Belirli bir format
t2 = Time("2019-11-28T09:52:07", format="iso")
```

---

## 2. Julian Date (JD)

Astronomide kullanılan sürekli zaman sayacı.

### Nedir?
- 1 Ocak 4713 BC, öğlenden itibaren geçen gün sayısı
- Kesirli günler günün saatini gösterir

### Proje Kodu:

```python
def jd(self, utc):
    """JD hesapla"""
    t = tm(utc, scale='utc')
    return t.jd  # Örn: 2458815.91

def jd_r(self, jd):
    """JD'den datetime'a"""
    t = tm(jd, format='jd', scale='tai')
    return t.to_datetime()
```

### Kullanım:

```python
from astropy.time import Time

utc = Time("2019-11-28 12:00:00", scale="utc")
jd = utc.jd  # 2458816.0

# Tersine çevirme
t = Time(jd, format="jd", scale="utc")
print(t.iso)  # 2019-11-28 12:00:00.000
```

---

## 3. Observer - Gözlemevi

Gözlemevi için astronomik hesaplamalar yapar.

### Proje Kodu (ast.py - TimeCalc sınıfı):

```python
class TimeCalc(Time):
    def __init__(self, logger, site):
        super().__init__(logger)
        self._obs_ = site.__observer__()  # Observer nesnesi

    def is_night(self, utc):
        """Gece mi?"""
        return self._obs_.is_night(tm(utc))

    def midnight(self, utc, jd=False):
        """Gece yarısı"""
        if jd:
            return self._obs_.midnight(tm(utc)).jd
        else:
            return self._obs_.midnight(tm(utc)).datetime

    def sun_rise_time(self, utc, which="next", jd=False):
        """Güneş doğuşu"""
        sun_rise = self._obs_.sun_rise_time(tm(utc), which=which)
        return sun_rise.jd if jd else sun_rise.datetime

    def sun_set_time(self, utc, which="next", jd=False):
        """Güneş batışı"""
        sun_set = self._obs_.sun_set_time(tm(utc), which=which)
        return sun_set.jd if jd else sun_set.datetime
```

### Site Sınıfı ile Birlikte:

```python
class Site:
    def __observer__(self):
        """Observer nesnesi oluştur"""
        return Observer(location=self.site, name=self._name_)
```

---

## 4. Gece/Gündüz Tespiti

Projenin en önemli özelliklerinden biri: FITS dosyalarını gece/gündüze göre sınıflandırma.

### Proje Kodu (ast.py - TimeCalc.day_part()):

```python
def day_part(self, utc, gap=30):
    """Günün hangi parçasında (gece/gündüz/alacakaranlık)"""
    try:
        jd_gap = 0.000694444 * gap  # 30 dakika = 0.000694444 gün
        jd = self.jd(utc)
        
        floor_jd = floor(jd)
        floor_date = self.jd_r(floor_jd)

        # Günün astronomik alacakaranlık başlangıcı
        twi_start_jd = self.twilight_evening(floor_date, which="NEXT", jd=True)
        # Günün astronomik alacakaranlık bitişi
        twi_end_jd = self.twilight_morning(floor_date, which="NEXT", jd=True)
        
        if twi_start_jd + jd_gap < jd and jd < twi_end_jd + jd_gap:
            return 1  # GECE
        
        if twi_start_jd - jd_gap > jd or jd > twi_end_jd - jd_gap:
            return 0  # GÜNDÜZ
        
        return -1  # Alacakaranlık (dawn/dusk)
        
    except Exception as excpt:
        self.logger.log(excpt)
```

### Kullanım:

```python
# UTC zaman
utc = datetime(2019, 11, 28, 20, 30, 0)

# Gece/gündüz tespiti
result = timeCalc.day_part(utc, gap=30)

if result == 1:
    print("Gece")
elif result == 0:
    print("Gündüz")
else:
    print("Alacakaranlık")
```

---

## 5. Twilight (Alacakaranlık) Hesaplamaları

### Proje Kodu:

```python
def twilight_morning(self, utc, tp="ASTRONOMICAL", which="next", jd=False):
    """Sabah alacakaranlığı"""
    if "CIVIL".startswith(tp.upper()):
        ret = self._obs_.twilight_morning_civil(tm(utc), which=which)
    elif "NAUTICAL".startswith(tp.upper()):
        ret = self._obs_.twilight_morning_nautical(tm(utc), which=which)
    else:
        ret = self._obs_.twilight_morning_astronomical(tm(utc), which=which)
    
    return ret.jd if jd else ret.datetime

def twilight_evening(self, utc, tp="ASTRONOMICAL", which="next", jd=False):
    """Akşam alacakaranlığı"""
    # Aynı mantık, farklı fonksiyon
```

### Alacakaranlık Türleri:
| Tür | Açıklama | Güneş Altında |
|-----|----------|---------------|
| **Civil** | En parlak | -6° |
| **Nautical** | Denizcilik | -12° |
| **Astronomical** | En karanlık | -18° |

---

## 6. Ay ve Güneş Hesaplamaları

### Proje Kodu:

```python
def moon_rise_time(self, utc, which="next", jd=False):
    """Ay doğuşu"""
    moon_rise = self._obs_.moon_rise_time(tm(utc))
    return moon_rise.jd if jd else moon_rise.datetime

def moon_set_time(self, utc, which="next", jd=False):
    """Ay batışı"""
    moon_set = self._obs_.moon_set_time(tm(utc))
    return moon_set.jd if jd else moon_set.datetime
```

---

## Proje İçinde Kullanım (main.py)

```python
# Zaman ve site oluşturma
from dag_cld import ast

site = ast.Site(logger, lat, lon, 3170)
timeCalc = ast.TimeCalc(logger, site)

# Dosya adından zaman çıkarma
fn = "2019_11_28__09_52_07.fits"
loc_time = asttime.str2time(fn, FORMAT="%Y_%m_%d__%H_%M_%S.fits")

# UTC'ye çevirme (Türkiye UTC+3)
utc = asttime.time_diff(loc_time, time_offset=-3)

# Gece mi gündüz mü?
dp = timeCalc.day_part(utc)

if dp == 1:
    print("Gece - bulut tespiti için uygun")
elif dp == 0:
    print("Gündüz")
```

### main.py'deki day_night_splitter fonksiyonu:

```python
def day_night_splitter(directory):
    files = fop.list_in_path("{}/*.gz".format(directory))
    for it, file in enumerate(files):
        _, fn, _ = fop.split_file_name(file)
        loc_time = asttime.str2time(fn, FORMAT="%Y_%m_%d__%H_%M_%S.fits")
        utc = asttime.time_diff(loc_time)
        dp = timeCalc.day_part(utc)
        
        if dp is not None:
            if dp == 1:
                fop.mv(file, "{}/NIGHT".format(directory))
            elif dp == 0:
                fop.mv(file, "{}/DAY".format(directory))
            else:
                fop.mv(file, "{}/DZ".format(directory))  # Dusk/Zawn
```

---

## Özet Tablo

| Fonksiyon | Kütüphane | İşlev |
|-----------|-----------|-------|
| `Time()` | astropy.time | Zaman nesnesi |
| `.jd` | astropy.time | Julian Date |
| `Observer` | astroplan | Gözlemevi hesaplamaları |
| `.is_night()` | astroplan | Gece mi? |
| `.sun_rise_time()` | astroplan | Güneş doğuşu |
| `.sun_set_time()` | astroplan | Güneş batışı |
| `.twilight_morning()` | astroplan | Sabah alacakaranlığı |
| `.twilight_evening()` | astroplan | Akşam alacakaranlığı |
| `.day_part()` | proje | Gece/gündüz/alacakaranlık |

---

## Kaynaklar

- [Astropy Time](https://docs.astropy.org/en/stable/time/)
- [Astroplan](https://astroplan.readthedocs.io/)
- [Julian Date Wikipedia](https://en.wikipedia.org/wiki/Julian_day)