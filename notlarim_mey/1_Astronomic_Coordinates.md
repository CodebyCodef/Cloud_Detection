# 1. Astronomik Koordinatlar

## Genel Bakış
Bu bölümde `astropy.coordinates` modülünü kullanarak astronomik koordinat sistemlerini ve proje içinde nasıl kullanıldığını öğreneceğiz.

---

## Kullanılan Kütüphaneler

```python
from astropy.coordinates import EarthLocation    # Gözlemevi konumu
from astropy.coordinates import SkyCoord         # Gökyüzü nesnesi koordinatı
from astropy.coordinates import AltAz            # Yükseklik-Azimut sistemi
from astropy.coordinates import Angle             # Açısal değerler
from astropy import units                         # Birim sistemi
```

---

## 1. Angle - Açısal Değerler

Açısal değerleri temsil etmek için kullanılır.

### Proje Kodu (ast.py - Coordinates sınıfı):

```python
class Coordinates:
    def __init__(self, logger):
        self.logger = logger

    def create(self, angle):
        """String olarak verilen açıyı Angle nesnesine dönüştür"""
        return Angle(angle)
```

### Kullanım:

```python
coord = Coordinates(logger)

# Farklı formatlarda açı tanımlama
lat = coord.create("41.2333 degree")    # Derece
lon = coord.create("39.7833 degree")

# Ya da doğrudan
lat = Angle("41.2333 degree")
lon = Angle("39.7833 degree")
```

### Desteklenen Formatlar:
- `"41.2333 degree"` → Derece
- `"41:14:00 deg"` → Saat:dakika:saniye
- `"41.2333"` → Varsayılan derece
- `"5h 30m 30s"` → Saat formatı

---

## 2. EarthLocation - Dünya Konumu

Gözlemevinin Dünya üzerindeki konumunu tanımlar.

### Proje Kodu (ast.py - Site sınıfı):

```python
class Site:
    def __init__(self, logger, lati, long, alti, name="Observatory"):
        self._lati_ = lati      # Enlem
        self._long_ = long      # Boylam
        self._alti_ = alti      # Yükseklik (metre)
        self._name_ = name
        self.site = self.create()

    def create(self):
        """EarthLocation nesnesi oluştur"""
        s = EarthLocation(lat=self._lati_, 
                         lon=self._long_,
                         height=self._alti_ * units.m)
        return s
```

### Kullanım:

```python
from astropy.coordinates import EarthLocation
from astropy import units

# Erzurum örneği (proje kodundan)
lat = Angle("41.2333 degree")
lon = Angle("39.7833 degree")
ele = 3170  # metre

site = EarthLocation(lat=lat, lon=lon, height=ele * units.m)

# Özelliklerine erişim
print(site.lat)      # Enlem
print(site.lon)      # Boylam
print(site.height)   # Yükseklik
```

---

## 3. SkyCoord - Gökyüzü Koordinatları

Yıldız, gezegen gibi gökyüzü nesnelerinin koordinatlarını temsil eder.

### Proje Kodu (ast.py - Obj sınıfı):

```python
class Obj:
    def __init__(self, logger, ra, dec):
        self.logger = logger
        self._ra_ = ra      # Sağ Açıklık (Right Ascension)
        self._dec_ = dec   # Dik Açıklık (Declination)
        self.obj = self.create()

    def create(self):
        """SkyCoord nesnesi oluştur"""
        return SkyCoord(ra=self._ra_, dec=self._dec__)

    def altaz(self, site, utc):
        """Nesnenin AltAz koordinatlarını hesapla"""
        frame_of_sire = AltAz(obstime=utc, location=site)
        object_alt_az = self.obj.transform_to(frame_of_sire)
        return object_alt_az
```

### Kullanım:

```python
from astropy.coordinates import SkyCoord
from astropy import units

# Bir yıldızın koordinatları
ra = Angle("10h 45m 32s")      # Sağ açıklık
dec = Angle("-1° 23' 45\"")   # Dik açıklık

star = SkyCoord(ra=ra, dec=dec)

# Özellikler
print(star.ra)    # Sağ açıklık
print(star.dec)   # Dik açıklık
```

---

## 4. AltAz - Yükseklik/Azimut Sistemi

Gözlemciye göre yerel koordinat sistemi:
- **Altitude (Yükseklik)**: Ufuktan yukarı açı (0° - 90°)
- **Azimuth (Azimut)**: Kuzeyden doğuya açı (0° - 360°)

### Proje Kodu (ast.py - Obj.altaz()):

```python
def altaz(self, site, utc):
    """Nesnenin AltAz koordinatlarını hesapla"""
    frame_of_sire = AltAz(obstime=utc, location=site.site)
    object_alt_az = self.obj.transform_to(frame_of_sire)
    return object_alt_az
```

### Kullanım:

```python
from astropy.time import Time

# Belirli bir zaman
utc = Time("2019-11-28 20:00:00", scale="utc")

# Nesnenin konumunu hesapla
altaz = star.altaz(site, utc)

print(altaz.alt.degree)   # Yükseklik (derece)
print(altaz.az.degree)    # Azimut (derece)
```

---

## 5. get_sun & get_moon

Güneş ve Ay'ın koordinatlarını hesaplama.

### Proje Kodu (ast.py):

```python
class Sun(Obj):
    def __init__(self, logger, time):
        self._time_ = time
        self.obj = self.create()

    def create(self):
        return get_sun(self._time_)

class Moon(Obj):
    def __init__(self, logger, time):
        self._time_ = time
        self.obj = self.create()

    def create(self):
        return get_moon(self._time_)
```

### Kullanım:

```python
from astropy.coordinates import get_sun, get_moon
from astropy.time import Time

utc = Time("2019-11-28 20:00:00", scale="utc")

sun = get_sun(utc)
moon = get_moon(utc)

print(sun.ra, sun.dec)    # Güneşin koordinatları
print(moon.ra, moon.dec) # Ay'ın koordinatları
```

---

## Proje İçinde Kullanım (main.py)

```python
from dag_cld import ast

# Koordinat sistemi oluştur
coord = ast.Coordinates(logger)
lat = coord.create("41.2333 degree")
lon = coord.create("39.7833 degree")

# Site oluştur (Erzurum)
site = ast.Site(logger, lat, lon, 3170)

# Güneş konumu
sun = ast.Sun(logger, utc)
```

---

## Özet Tablo

| Sınıf/Fonksiyon | Modül | Kullanım |
|-----------------|-------|----------|
| `Angle` | astropy.coordinates | Açısal değerler |
| `EarthLocation` | astropy.coordinates | Gözlemevi konumu |
| `SkyCoord` | astropy.coordinates | Gökyüzü nesnesi |
| `AltAz` | astropy.coordinates | Yerel koordinat sistemi |
| `get_sun` | astropy.coordinates | Güneş pozisyonu |
| `get_moon` | astropy.coordinates | Ay pozisyonu |
| `units` | astropy | Birim sistemi |

---

## Kaynaklar

- [Astropy Coordinates](https://docs.astropy.org/en/stable/coordinates/)
- [Coordinates Cookbook](https://docs.astropy.org/en/stable/coordinates/definitions.html)