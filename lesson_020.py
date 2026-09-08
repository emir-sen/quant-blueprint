import math

# 1. DOSYA OLUŞTURMA: Dışarıdan gelen veri seti simülasyonu
veriler = [
    "Tarih,Fiyat\n",
    "2026-09-01,300.0\n",
    "2026-09-02,305.5\n",
    "2026-09-03,302.0\n",
    "2026-09-04,310.0\n",
    "2026-09-05,315.2\n"
]

with open("bist_veri.csv", "w", encoding="utf-8") as dosya:
    dosya.writelines(veriler)

print("1. 'bist_veri.csv' başarıyla oluşturuldu.\n")

# 2. DOSYADAN VERİ OKUMA VE İŞLEME
fiyatlar = []

with open("bist_veri.csv", "r", encoding="utf-8") as dosya:
    satirlar = dosya.readlines()[1:]  # Başlık satırını (Tarih,Fiyat) atla (Slicing)
    
    for satir in satirlar:
        parcalar = satir.strip().split(",")  # Virgülle ayır ve temizle
        fiyat = float(parcalar[1])
        fiyatlar.append(fiyat)

# 3. VERİ ANALİZİ VE İSTATİSTİK
ortalama_fiyat = sum(fiyatlar) / len(fiyatlar)
son_fiyat = fiyatlar[-1]  # Negatif İndeks
ilk_fiyat = fiyatlar[0]

toplam_getiri_yuzde = ((son_fiyat - ilk_fiyat) / ilk_fiyat) * 100

# 4. AŞAMA 1 BİTİRİŞ RAPORU
print("=== BIST100 MINISIMULASYON RAPORU ===")
print(f"Okunan Fiyat Sayısı : {len(fiyatlar)}")
print(f"İlk Gün Fiyatı       : {ilk_fiyat} TL")
print(f"Son Gün Fiyatı       : {son_fiyat} TL")
print(f"Ortalama Fiyat       : {round(ortalama_fiyat, 2)} TL")
print(f"Dönemsel Getiri      : %{round(toplam_getiri_yuzde, 2)}")