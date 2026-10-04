import warnings
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import yfinance as yf

# 1. UYARILARI BASTIRMA
warnings.filterwarnings("ignore")

# 2. VERİ ÇEKME & İNDEKSİ TEMİZLEME
ticker = "THYAO.IS"
df = yf.Ticker(ticker).history(period="1y")

# Tarih indeksinden kaynaklanan kütüphane hatasını engellemek için
# seriyi saf sayı dizisine (values) dönüştürüyoruz
close_prices = df["Close"].reset_index(drop=True)

# 3. HAM FİYAT İLE BÜTÜNLEŞİK ARIMA(1, 1, 1) MODELİ KURULUMU
model = ARIMA(close_prices, order=(1, 1, 1))
result = model.fit()

# Model Özet Tablosunu Basalım
print("=" * 60)
print(f"--- {ticker} ARIMA(1, 1, 1) MODELİ ÖZETİ ---")
print("=" * 60)
print(result.summary())

# 4. GELECEĞE YÖNELİK TAHMİN (FORECASTING)
forecast_steps = 5
forecast_values = result.forecast(steps=forecast_steps)

print("\n" + "=" * 60)
print(f"--- ÖNÜMÜZDEKİ {forecast_steps} İŞLEM GÜNÜ FİYAT TAHMİNİ ---")
print("=" * 60)

for i, price in enumerate(forecast_values, 1):
    print(f"{i}. Gün Tahmini Fiyat : {price:.2f} TL")