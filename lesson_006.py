balance = 2500

while True:
    print("=====ATM=====")
    print("1-Bakiyeyi Gör")
    print("2-Para Yatır")
    print("3-Para Çek")
    print("4-Çıkış")
    choice = input("Seçiminiz: ")

    if choice == "1":
        print("Bakiyeniz: ", balance)
    elif choice == "2":
        amount = int(input("Eklemek istediğiniz tutarı giriniz: "))
        balance = amount + balance
        print("Yeni bakiyeniz: ", balance)
    elif choice == "3":
        amount = int(input("Çekek istediğiniz tutarı girin: "))
        if 0 < amount <= balance:
            balance = balance - amount
            print("Yeni bakiyeniz: ", balance)
        elif amount <= 0:
            print("Lütfen pozitif bir sayı girin.")
        else:
            print("Yeterli bakiye yok!")
    elif choice == "4":
        print("Program kapandı.")
        break 
    else:
        print("Yanlış seçim!")