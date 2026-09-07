# Sistemdeki kullanıcılar (Nested Dictionary)
atm_kullanicilar = {
    "emir": {
        "sifre": 1234,
        "bakiye": 2000
    },
    "umut": {
        "sifre": 5678,
        "bakiye": 5000
    }
}

# --- FONKSİYON TANIMLARI ---

def giris_yap():
    isim = input("İsminiz: ")

    if isim in atm_kullanicilar:
        sifre = int(input("Şifrenizi giriniz: "))

        if sifre == atm_kullanicilar[isim]["sifre"]:
            return isim
        else:
            print("Şifre yanlış.")
            return None
    else:
        print("Kişi bulunamadı.")
        return None

def bakiye_goster(kullanici):
    print(f"Mevcut Bakiyeniz: {atm_kullanicilar[kullanici]['bakiye']} TL")

def para_yatir(kullanici):
    toplam = int(input("Yatırmak istediğiniz tutarı giriniz: "))
    atm_kullanicilar[kullanici]["bakiye"] += toplam
    print("İşlem başarılı, yeni bakiyeniz:", atm_kullanicilar[kullanici]["bakiye"])

def para_cek(kullanici):
    miktar = int(input("Çekmek istediğiniz tutarı giriniz: "))
    
    # Bakiye kontrolü (Mantıksal Koşul)
    if miktar <= atm_kullanicilar[kullanici]["bakiye"]:
        atm_kullanicilar[kullanici]["bakiye"] -= miktar
        print(f"İşlem başarılı. Kalan bakiyeniz: {atm_kullanicilar[kullanici]['bakiye']} TL")
    else:
        print("Yetersiz bakiye!")

# --- ANA PROGRAM AKIŞI ---

kullanici = giris_yap()

if kullanici is not None:
    print(f"\nGiriş başarılı. Hoş geldiniz, {kullanici.capitalize()}!")

    while True:
        print("\n--- İŞLEM MENÜSÜ ---")
        print("1. Bakiyeyi Gör")
        print("2. Para Çek")
        print("3. Para Yatır")
        print("4. Çıkış")
        
        choice = input("Bir seçim yapınız (1-4): ")  # String olarak aldık
        
        if choice == "1":
            bakiye_goster(kullanici)
        elif choice == "2":
            para_cek(kullanici)
        elif choice == "3":
            para_yatir(kullanici)
        elif choice == "4":
            print("Çıkış yapılıyor... İyi günler!")
            break
        else:
            print("Geçersiz seçim! Lütfen 1-4 arasında bir sayı giriniz.")