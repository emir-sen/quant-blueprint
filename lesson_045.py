import os
import warnings
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from arch import arch_model

# Uyarılardan gelen sarı metinleri temizleyelim
warnings.filterwarnings("ignore")

# visuals klasörü yoksa otomatik oluşturalım
os.makedirs("visuals", exist_ok=True)

# 1. VERİ ÇEKME & GETİRİ HESAPLAMA
ticker = "THYAO.IS"
df = yf.Ticker(ticker).history(period="1y")

# Getiriyi % cinsinden alıp indeksini sıfırlıyoruz
returns = 100 * df["Close"].pct_change().dropna().reset_index(drop=True)

# 2. GARCH(1, 1) MODELİ KURULUMU
model = arch_model(returns, vol="Garch", p=1, q=1, mean="Zero")
result = model.fit(disp="off")

# Model Özet Tablosunu Basalım
print("=" * 60)
print(f"--- {ticker} GARCH(1, 1) VOLATİLİTE MODELİ ÖZETİ ---")
print("=" * 60)
print(result.summary())

# 3. ŞARTLI OYNAKLIK (CONDITIONAL VOLATILITY) ÇIKARTILMASI
conditional_volatility = result.conditional_volatility

# 4. GÖRSELLEŞTİRME
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(df["Close"].values, color="blue", label="THYAO Fiyat (TL)")
plt.title("THYAO Kapanış Fiyatı")
plt.grid(True)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(conditional_volatility, color="red", label="GARCH Tahmini Oynaklık (Risk)")
plt.title("THYAO GARCH(1,1) Günlük Oynaklık (Volatilite Kümelenmesi)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig("visuals/lesson_045_garch_volatility.png")
print("\n[BİLGİ] Volatilite grafiği 'visuals/lesson_045_garch_volatility.png' olarak başarıyla kaydedildi.")