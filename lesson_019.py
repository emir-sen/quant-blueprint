# 1. DOSYAYA YAZMA ('w' modu dosyayı yoksa otomatik oluşturur)
# encoding="utf-8" Türkçe karakter sorunu yaşanmasını engeller.
# with open yapısı işlem bitince dosyayı otomatik olarak kapatır.
with open("fiyatlar.txt", "w", encoding="utf-8") as dosya:
    dosya.write("THYAO,312.5\n")  # \n bir alt satıra geçmeyi sağlar
    dosya.write("GARAN,105.0\n")
    dosya.write("AKBNK,62.0\n")

print("Veriler fiyatlar.txt dosyasına yazıldı!")

# 2. DOSYADAN OKUMA ('r' okuma modudur)
with open("fiyatlar.txt", "r", encoding="utf-8") as dosya:
    icerik = dosya.read()  # Tüm dosya içeriğini tek string olarak okur
    print("\n--- Fiyatlar Dosyası İçeriği ---")
    print(icerik)