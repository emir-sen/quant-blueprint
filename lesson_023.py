import numpy as np

# 3 Hisse x 3 Gün Fiyat Matrisi
# Satır 0: THYAO [300, 305, 310]
# Satır 1: GARAN [100, 102, 105]
# Satır 2: AKBNK [60,  62,  61]
portfoy = np.array([
    [300, 305, 310],
    [100, 102, 105],
    [60,  62,  61]
])

# 1. MATRİS İNDEKSLERİ (Satır, Sütun)
# Sadece THYAO'nun (0. satır) 3. gün fiyatı (2. sütun)
thyao_son_fiyat = portfoy[0, 2]
print(f"THYAO Son Gün Fiyatı: {thyao_son_fiyat}")

# Sadece GARAN'ın tüm günleri (1. satır, tüm sütunlar)
garan_fiyatlari = portfoy[1, :]
print(f"GARAN Tüm Fiyatlar: {garan_fiyatlari}")

# 2. KOŞULLU MASKELEME (FINANCIAL FILTERING)
# Portföydeki 100 TL üstü tüm fiyatları yakalayalım
yuksek_fiyatlar = portfoy[portfoy > 100]

print("\n--- 100 TL ÜSTÜNDEKİ FİYATLAR ---")
print(yuksek_fiyatlar)