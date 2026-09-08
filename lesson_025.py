import numpy as np

# 1. Veri Yapısı: 4 Hisse x 5 Günlük Kapanış Fiyatları Matrisi
# Satırlar: THYAO, GARAN, AKBNK, EREGL
fiyat_matrisi = np.array([
    [300.0, 305.0, 302.0, 310.0, 315.0],  # THYAO
    [100.0, 102.0, 101.0, 105.0, 104.0],  # GARAN
    [60.0,  62.0,  61.0,  63.0,  65.0],   # AKBNK
    [45.0,  44.0,  46.0,  45.5,  47.0]    # EREGL
])

print("=== BIST PORTFÖY RİSK VE GETİRİ ANALİZİ ===")

# 2. Hisse Bazlı İstatistikler (axis=1)
ortalama_fiyatlar = fiyat_matrisi.mean(axis=1)
volatilite_risk = fiyat_matrisi.std(axis=1)

# 3. Yüzdesil Getiri Hesaplama (Son Gün Fiyatı / İlk Gün Fiyatı - 1) * 100
ilk_gun = fiyat_matrisi[:, 0]   # 0. sütun (tüm satırlar)
son_gun = fiyat_matrisi[:, -1]  # Son sütun (tüm satırlar)
toplam_getiri_yuzde = ((son_gun - ilk_gun) / ilk_gun) * 100

# 4. Raporlama
hisse_isimleri = ["THYAO", "GARAN", "AKBNK", "EREGL"]

for i in range(len(hisse_isimleri)):
    print(f"\nHisse: {hisse_isimleri[i]}")
    print(f"  Ortalama Fiyat : {np.round(ortalama_fiyatlar[i], 2)} TL")
    print(f"  Risk (Std Dev) : {np.round(volatilite_risk[i], 2)}")
    print(f"  Toplam Getiri  : %{np.round(toplam_getiri_yuzde[i], 2)}")

# 5. Günlük Portföy Toplam Değeri (axis=0)
gunluk_portfoy_toplami = fiyat_matrisi.sum(axis=0)
print("\n-------------------------------------------")
print(f"Günlük Portföy Toplam Değerleri (TL): {gunluk_portfoy_toplami}")