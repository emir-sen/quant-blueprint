import pandas as pd
import numpy as np

hisseler = ["THYAO", "GARAN", "AKBNK"]
gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe"]
coklu_fiyatlar = [
    [100, 102, 105, 103],
    [50,  52,  51,  55],
    [200, 195, 198, 202]
]

df = pd.DataFrame(coklu_fiyatlar, index=hisseler, columns=gunler)
print(df)

# 0. satır (THYAO), 2. sütun (Çarşamba)
fiyat_iloc = df.iloc[0, 2]
print(f"İndeks ile çekilen fiyat: {fiyat_iloc}")

# THYAO hissesinin Çarşamba günkü fiyatını çekelim
fiyat = df.loc["THYAO", "Çarşamba"]
print(f"THYAO Çarşamba Fiyatı: {fiyat}")

# Çarşamba günü 100'den pahalı olan hisseler
pahali_hisseler = df[df["Çarşamba"] > 100]
print(pahali_hisseler)