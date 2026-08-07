kullanici = {
    "isim": "Emir",
    "sehir": "Ankara",
    "yas": 21
}
print(kullanici["sehir"])

kullanici["sehir"] = "İstanbul"
print(kullanici["sehir"])

kullanici["yas"] = 22
print(kullanici["yas"])

kullanici["universite"] = "Yildiz Teknik Universitesi"
print(kullanici["universite"])

for bilgi in kullanici:
    print(bilgi, ":", kullanici[bilgi])

kullanici = {
    "isim": "Emir",
    "yas": 21
}
for anahtar, deger in kullanici.items():
    print(anahtar)
    print(deger)

atm_kullanicilar = {
    "emir": {
        "sifre": 1234,
        "bakiye": 2000
    },
    "ahmet": {
        "sifre": 5678,
        "bakiye": 3000
    }
}

isim = input("İsminiz: ")

if isim in atm_kullanicilar:
    sifre = int(input("Şifreniz: "))

    if sifre == atm_kullanicilar[isim]["sifre"]:
        print("Giriş başarılı.")

        while True:
            print("\n1. Bakiyeyi Gör")
            print("2. Çıkış")
            print("3. Para Yatır")
            print("4. Para Çek")

            choice = input("Seçiminiz: ")

            if choice == "1":
                print("Bakiyeniz:", atm_kullanicilar[isim]["bakiye"])

            elif choice == "2":
                print("Çıkış yapılıyor...")
                break

            elif choice == "3":
                toplam = int(input("Yatırmak istediğiniz tutarı giriniz: "))
                atm_kullanicilar[isim]["bakiye"] += toplam
                print("Yeni Bakiyeniz:", atm_kullanicilar[isim]["bakiye"])

            elif choice == "4":
                tutar = int(input("Çekmek istediğiniz tutarı giriniz: "))

                if tutar <= atm_kullanicilar[isim]["bakiye"]:
                    atm_kullanicilar[isim]["bakiye"] -= tutar
                    print("İşleminiz tamamlandı.")
                    print("Yeni Bakiyeniz:", atm_kullanicilar[isim]["bakiye"])
                else:
                    print("Yetersiz bakiye.")

            else:
                print("Geçersiz seçim yaptınız.")

    else:
        print("Şifre yanlış.")

else:
    print("Kullanıcı bulunamadı.")