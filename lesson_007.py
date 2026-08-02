def menu():
    print("=====ATM=====")
    print("1. Bakiye Göster")
    print("2. Para Yatır")
    print("3. Para Çek")
    print("4. Çıkış")

def bakiye_goster(balance):
    print("Bakiyeniz: ", balance)

def para_yatir(balance, amount):
    return balance + amount

def para_cek(balance, amount):
    return balance - amount

balance = 1000

menu()
bakiye_goster(balance)

while True:
    menu()
    try:
        choice = int(input("Seçiminiz: "))
    except ValueError:
        print("Lütfen geçerli bir sayı girin.")
        continue

    if choice == 4:
        print("İyi günler.")
        break
    elif choice == 2:
        try:
            amount = int(input("Yatırmak istediğiniz tutar: "))
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")
            continue

        balance = para_yatir(balance, amount)
        print("İşlem başarılı.")

    elif choice == 1:
        bakiye_goster(balance)

    elif choice == 3:
        try:
            amount = int(input("Çekmek istediğiniz tutarı giriniz: "))
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")
            continue
        
        if amount > balance:
            print("Yetersiz bakiye.")
        else:
            balance = para_cek(balance, amount)
            print("İşlem başarılı.")