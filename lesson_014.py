# Korumalı Kod:
def giris_yap_test():
    try:
        sifre = int(input("Şifrenizi giriniz: "))
        print(f"Girilen şifre: {sifre}")
    except ValueError:
        print("Lütfen geçerli bir sayı giriniz!")

# Fonksiyonu burada tetikliyoruz:
giris_yap_test()