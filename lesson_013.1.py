#Selam döngüsü

isim = input("İsim giriniz: ")

def selam_ver(isim):
    print("Hoşgeldin", isim)

selam_ver(isim)

#Bir sayının küpünü alma

def kup(x):
    return x * x * x

sonuc = kup(3)
print(sonuc)

#Bir sayının 2 katını alma

def iki_kati(sayi):
    return sayi * 2

sayi = int(input("Bir sayı giriniz: "))

sonuc = iki_kati(sayi)

print(sonuc)


#Bir sayının üç katını alma

def uc_kati(uc):
    return uc * 3

uc = int(input("Bir sayı giriniz: "))

deger = uc_kati(uc)

print(deger)


#Alan hesaplama

def dikdortgen_alani(uzunluk, genislik):
    return uzunluk * genislik

uzunluk = int(input("Uzunluk: "))
genislik = int(input("Genişlik: "))

alan = dikdortgen_alani(uzunluk, genislik)

print(alan)

#Hacim hesaplama

def hacim(uzunluk, genislik, yukseklik):
    return uzunluk * genislik * yukseklik

uzunluk = int(input("Uzunluk giriniz: "))
genislik = int(input("Genişlik giriniz: "))
yukseklik = int(input("Yükseklik giriniz: "))

hacim_sonuc = hacim(uzunluk, genislik, yukseklik)
print(hacim_sonuc)

#İndirim oranı

def indirimli_fiyat(fiyat, yuzde):
    return fiyat - (fiyat * yuzde / 100)

fiyat = int(input("Fiyat giriniz: "))
yuzde = int(input("İndirim oranını giriniz: "))

sonuc = indirimli_fiyat(fiyat, yuzde)

print(sonuc)