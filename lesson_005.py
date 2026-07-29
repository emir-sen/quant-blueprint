boy = float(input("Boyunuz (metre): "))
kilo = int(input("Kilonuz: "))
vki = kilo / (boy ** 2)

if vki < 18.5:
    print("Zayıfsınız.")
elif vki < 25:
    print("Normal kilodasınız.")
else:
    print("Kilolusunuz.")
print("VKİ endeksiniz: ", round(vki, 1))