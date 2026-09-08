import math
import random

# 1. Başlangıç Fiyatı
fiyat = 100.0

# 2. -5.0 ile +5.0 Arasında Rastgele Günlük Değişim Yüzdesi (Float)
degisim_yuzdesi = random.uniform(-5.0, 5.0)

# 3. Finansal Büyüme Çarpanı ile Yeni Fiyat Hesaplama
yeni_fiyat = fiyat * (1 + degisim_yuzdesi / 100)

print(f"Günlük Değişim Oranı: %{round(degisim_yuzdesi, 2)}")
print(f"Hissenin Yeni Fiyatı: {round(yeni_fiyat, 2)} TL")

# 4. Yıllık Varyans Üzerinden Risk (Volatilite) Hesaplama
varyans = 256
volatilite = math.sqrt(varyans)

print(f"Hissenin Yıllık Riski (Volatilite): %{volatilite}")