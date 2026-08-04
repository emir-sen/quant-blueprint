for i in range(1, 11):
    print(i)

for m in range(0, 11, 2):
    print(m)

for t in range(10, 0, -2):
    print(t)

toplam = 0
for k in range(1, 101):
    toplam = toplam + k
print(toplam)

cifttoplam = 0
for cift in range(0 , 101, 2):
    cifttoplam = cifttoplam + cift
print(cifttoplam)

sayilar = [15, 8, 20, 3, 12]

en_buyuk = sayilar[0]

for sayi in sayilar:
    if sayi > en_buyuk:
        en_buyuk = sayi

print(en_buyuk)