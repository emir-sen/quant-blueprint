wallet = 2500
print("======ATM======")
print("1- Bakiyeyi Gör")
print("2- Çıkış")

choice = input("Seçiminiz: ")

print(type(choice))

if choice == "1":
    print("Bakiyeniz:", wallet)
else:
    print("Program kapandı.")
