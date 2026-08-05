sayilar = [3, 8, 5, 12, 7, 20]

for sayi in sayilar:
    if sayi % 2 == 0:
        print(sayi)

for sayi in sayilar:
    if sayi % 2 == 1:
        print(sayi)

x = [15, 8, 20, 3, 12, 7]

for on in x:
    if on > 10:
        print(on)

sayac = 0

nam = [15, 8, 20, 3, 12, 7]

for t in nam:
    if t > 10:
        sayac = sayac + 1
print(sayac)

toplam = 0

toplam1 = [15, 8, 20, 3, 12, 7]

for m in toplam1:
    if m > 10:
        toplam = toplam + m
print(toplam)

haha = [15, 8, 20, 3, 12, 7]

en_kucuk = haha[0]

for kucuk in haha:
    if kucuk < en_kucuk:
        en_kucuk = kucuk
print(en_kucuk)

sayilar = [10, 20, 30, 40]

toplam = 0

for sayi in sayilar:
    toplam = toplam + sayi


ortalama = toplam / len(sayilar)

print(ortalama)

sayilar = [12, 5, 18, 3, 25, 8, 30]
toplam = 0
for sayi in sayilar:
    if sayi < 10:
        toplam = toplam + sayi
print(toplam)

sayac = 0
for sayi in sayilar:
    if sayi % 2 == 0:
        sayac = sayac + 1
print(sayac)

en_buyuk = sayilar[0]
for sayi in sayilar:
    if sayi % 2 == 1 and sayi > en_buyuk:
        en_buyuk = sayi
print(en_buyuk)

        