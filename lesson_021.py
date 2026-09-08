import numpy as np

# 1. Standart Python Listesi (5 Günlük Hisse Fiyatları)
fiyat_listesi = [100, 105, 102, 110, 108]

# 2. Listeyi NumPy Vektörüne (ndarray) Dönüştürme
fiyat_vektoru = np.array(fiyat_listesi)

# 3. Vektörel İşlem (Vectorized Operation)
# Hiç for döngüsü kurmadan tüm fiyatlara tek hamlede %5 faiz/getiri ekliyoruz
guncel_fiyatlar = fiyat_vektoru * 1.05

# 4. İstatistiksel Metotlar
ortalama_fiyat = fiyat_vektoru.mean()

print(f"Orijinal Fiyat Vektörü : {fiyat_vektoru}")
print(f"%5 Artırılmış Vektör  : {guncel_fiyatlar}")
print(f"Ortalama Fiyat         : {ortalama_fiyat} TL")