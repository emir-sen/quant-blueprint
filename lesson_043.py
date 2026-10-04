import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import yfinance as yf

# 1. VERİ ÇEKME & DURAĞANLAŞTIRMA
ticker = "THYAO.IS"
df = yf.Ticker(ticker).history(period="1y")

# Fiyat durağan olmadığı için yüzdesel getiriyi alıyoruz
returns = df["Close"].pct_change().dropna()

# 2. SAF AR(1) MODELİ KURULUMU
# ARIMA(p, d, q) yapısında:
# p = 1 (AR derecesi: Geçmiş 1 günün getirisine bak)
# d = 0 (Fark derecesi: Verimiz zaten returns olduğu için d=0)
# q = 0 (MA derecesi: Şoklara bakma)
ar_model = ARIMA(returns, order=(1, 0, 0))
ar_result = ar_model.fit()

print("=" * 50)
print("--- SAF AR(1) MODELİ ÖZETİ ---")
print(f"AR(1) Katsayısı (phi_1) : {ar_result.params.get('ar.L1', 0):.4f}")
print(f"p-değeri (p-value)      : {ar_result.pvalues.get('ar.L1', 1):.4f}")
print("=" * 50)

# 3. SAF MA(1) MODELİ KURULUMU
# ARIMA(p, d, q) yapısında:
# p = 0 (AR derecesi: Getiriye bakma)
# d = 0 (Fark derecesi: Verimiz durağan)
# q = 1 (MA derecesi: Geçmiş 1 günün şokuna/hatasına bak)
ma_model = ARIMA(returns, order=(0, 0, 1))
ma_result = ma_model.fit()

print("\n" + "=" * 50)
print("--- SAF MA(1) MODELİ ÖZETİ ---")
print(f"MA(1) Katsayısı (theta_1): {ma_result.params.get('ma.L1', 0):.4f}")
print(f"p-değeri (p-value)      : {ma_result.pvalues.get('ma.L1', 1):.4f}")
print("=" * 50)