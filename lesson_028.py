import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

thyao = yf.Ticker("THYAO.IS")
df = thyao.history(period="3mo")

df["Günlük_Getiri_%"] = df["Close"].pct_change() * 100
df["SMA_5"] = df["Close"].rolling(window=5).mean()
df["SMA_20"] = df["Close"].rolling(window=20).mean()

df["Sinyal"] = np.where(df["SMA_5"] > df["SMA_20"], "AL", "SAT")

df["Pozisyon"] = np.where(df["Sinyal"] == "AL", 1, 0)
df["Stratei_Getiri_%"] = df["Pozisyon"].shift(1) * df["Günlük_Getiri_%"]

df["Hisse_Toplam_Getiri"] = df["Günlük_Getiri_%"].cumsum()
df["Stratei_Toplam_Getiri"] = df["Stratei_Getiri_%"].cumsum()

import matplotlib.pyplot as plt

# 2 Katlı Grafik Penceresi Oluşturuyoruz
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# 1. Grafik: Fiyat ve Hareketli Ortalamalar
ax1.plot(df.index, df["Close"], label="THYAO Fiyat", color="gray", alpha=0.5)
ax1.plot(df.index, df["SMA_5"], label="SMA 5 (Hızlı)", color="blue", linewidth=1.5)
ax1.plot(df.index, df["SMA_20"], label="SMA 20 (Yavaş)", color="red", linewidth=1.5)
ax1.set_title("THYAO Fiyatı ve Hareketli Ortalamalar (Golden/Death Cross)")
ax1.set_ylabel("Fiyat (TL)")
ax1.legend()
ax1.grid(True)

# 2. Grafik: Kümülatif Getiriler
ax2.plot(df.index, df["Hisse_Toplam_Getiri"], label="Hisse Getirisi (%)", color="black", linestyle="--")
ax2.plot(df.index, df["Stratei_Toplam_Getiri"], label="Strateji Getirisi (%)", color="green", linewidth=2)
ax2.set_title("Kümülatif Getiri Karşılaştırması (%)")
ax2.set_xlabel("Tarih")
ax2.set_ylabel("Getiri (%)")
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()


