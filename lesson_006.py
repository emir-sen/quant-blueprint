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
        while True:
            try:
                amount = int(input("Çekmek istediğiniz tutarı giriniz: "))

                if amount <= 0:
                    print("Lütfen pozitif bir sayı giriniz.")
                elif amount <= balance:
                    balance = balance - amount
                    print("İşlem başarılı.")
                    print("Yeni bakiyeniz:", balance)
                    break
                else:
                    print("Yeterli bakiye yok!")

            except:
                print("Lütfen geçerli bir sayı giriniz.")

    elif choice == "4":
        print("Program kapandı.")
        break 
    else:
        print("Yanlış seçim!")