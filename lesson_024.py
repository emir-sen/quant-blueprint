import numpy as np

# 3 Hisse x 3 Gün Fiyat Matrisi
# Satır 0: THYAO, Satır 1: GARAN, Satır 2: AKBNK
portfoy = np.array([
    [300, 305, 310],
    [100, 102, 105],
    [60,  62,  61]
])

# 1. HİSSE BAZLI ORTALAMA (axis=1: Soldan Sağa)
hisse_ortalamalari = portfoy.mean(axis=1)
print("Hisse Bazlı Ortalamalar (THYAO, GARAN, AKBNK):")
print(hisse_ortalamalari)

# 2. HİSSE BAZLI VOLATİLİTE / RİSK (Standart Sapma)
hisse_riski = portfoy.std(axis=1)
print("\nHisse Bazlı Risk / Volatilite (std):")
print(np.round(hisse_riski, 2))

# 3. GÜN BAZLI PORTFÖY TOPLAMI (axis=0: Yukarıdan Aşağıya)
gunluk_toplam_fiyat = portfoy.sum(axis=0)
print("\nGün Gün Portföy Toplam Değerleri (1.Gün, 2.Gün, 3.Gün):")
print(gunluk_toplam_fiyat)