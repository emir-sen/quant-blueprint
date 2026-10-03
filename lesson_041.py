import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

def check_stationarity(series, name="Seri"):
    """
    Augmented Dickey-Fuller (ADF) Testi Modülü
    ------------------------------------------
    Verilen zaman serisinin durağan (stationary) olup olmadığını test eder.
    """
    # NaN değerleri temizle
    clean_series = series.dropna()
    
    # ADF Testini çalıştır
    result = adfuller(clean_series)
    
    adf_statistic = result[0]
    p_value = result[1]
    critical_values = result[4]
    
    print(f"\n--- {name} ADF TEST SONUÇLARI ---")
    print(f"ADF İstatistiği : {adf_statistic:.4f}")
    print(f"p-değeri (p-value): {p_value:.4f}")
    print("Kritik Değerler  :")
    for key, value in critical_values.items():
        print(f"   %{key}: {value:.4f}")
        
    # Karar Mekanizması (0.05 Eşik Değeri)
    if p_value < 0.05:
        print(f"RESULT: {name} DURAĞANDIR (p < 0.05, H0 Reddedildi).")
        return True
    else:
        print(f"RESULT: {name} DURAĞAN DEĞİLDİR (p >= 0.05, H0 Reddedilemedi).")
        return False

if __name__ == "__main__":
    ticker = "THYAO.IS"
    df = yf.Ticker(ticker).history(period="1y")
    
    # 1. Ham Fiyat (Close) Testi
    print("==================================================")
    check_stationarity(df["Close"], name=f"{ticker} Kapanış Fiyatı")
    
    # 2. Günlük Yüzdesel Getiri Testi
    df["Getiri"] = df["Close"].pct_change()
    print("==================================================")
    check_stationarity(df["Getiri"], name=f"{ticker} Günlük Getiri")