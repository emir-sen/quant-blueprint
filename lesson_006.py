balance = 2500

while True:
    print("=====ATM=====")
    print("1-Bakiyeyi Gör")
    print("2-Para Yatır")
    print("3-Çıkış")
    choice = input("Seçiminiz: ")

    if choice == "1":
        print("Bakiyeniz: ", balance)
    if choice == "2":
        amount = int(input("Eklemek istediğiniz tutarı giriniz: "))
        balance = amount + balance
        print("Yeni bakiyeniz: ", balance)
    if choice == "3":
        print("Program kapandı.")
        break 