# 1. SET: Benzersiz Hisse Sembolleri Filtresi
ham_veri = ["THYAO", "GARAN", "THYAO", "AKBNK", "GARAN", "SISE"]
benzersiz_hisseler = set(ham_veri)
print("Benzersiz Hisseler (Set):", benzersiz_hisseler)

# 2. TUPLE: Değiştirilemez Hisse Künyesi (Sembol, Borsa, Kurulduğu Yıl)
hisse_kunye = ("THYAO", "BIST", 1933)
print(f"Hisse: {hisse_kunye[0]}, Borsa: {hisse_kunye[1]}")

# 3. LIST: Fiyat Geçmişi (Son 5 Gün)
fiyat_gecmisi = [305.0, 308.5, 307.0, 310.2, 312.5]
fiyat_gecmisi.append(315.0)  # Yeni gün fiyatı eklendi
print("Güncellenmiş Fiyatlar (List):", fiyat_gecmisi)

# 4. DICTIONARY: Portföy Özeti
portfoy = {
    "sahibi": "Emir Şen",
    "hisseler": list(benzersiz_hisseler),
    "toplam_varlik_tl": 50000
}
print(f"{portfoy['sahibi']} Portföyü: {portfoy['hisseler']}")