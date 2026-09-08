import numpy as np

# 1. 3 Farklı Hissenin (Satırlar) 3 Günlük Fiyat Matrisi (Sütunlar)
portfoy = np.array([
    [300, 305, 310],  # THYAO
    [100, 102, 105],  # GARAN
    [60,  62,  61]    # AKBNK
])

print("--- PORTFÖY MATRİSİ ---")
print(portfoy)

# 2. Matris Boyutu (Shape) Kontrolü
print("\nMatris Boyutu (Satır, Sütun):", portfoy.shape)

# 3. Vektörel İşlem: Tüm Portföye %10 Değer Artışı / Enflasyon Ekleme
guncel_portfoy = portfoy * 1.10

print("\n--- %10 DÜZELTİLMİŞ PORTFÖY ---")
print(np.round(guncel_portfoy, 2))