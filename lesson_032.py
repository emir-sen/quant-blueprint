import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. VERİ ÇEKME & GETİRİ HESAPLAMA
# ==========================================
thyao = yf.Ticker("THYAO.IS")
bist = yf.Ticker("XU100.IS")

df = thyao.history(period="3mo")
df_bist = bist.history(period="3mo")

df["Günlük_Getiri_%"] = df["Close"].pct_change() * 100
df["BIST_Getiri_%"] = df_bist["Close"].pct_change() * 100

# ==========================================
# 2. İNDİKATÖRLER VE STRATEJİ SİNYALİ
# ==========================================
df["SMA_5"] = df["Close"].rolling(window=5).mean()
df["SMA_20"] = df["Close"].rolling(window=20).mean()

# RSI (14 Günlük)
delta = df["Close"].diff()
gain = np.where(delta > 0, delta, 0)
loss = np.where(delta < 0, -delta, 0)
avg_gain = pd.Series(gain, index=df.index).rolling(window=14).mean()
avg_loss = pd.Series(loss, index=df.index).rolling(window=14).mean()
rs = avg_gain / avg_loss
df["RSI_14"] = 100 - (100 / (1 + rs))

# Sinyal & Pozisyon
kosul_al = (df["SMA_5"] > df["SMA_20"]) & (df["RSI_14"] > 50)
df["Sinyal"] = np.where(kosul_al, "AL", "SAT")
df["Pozisyon"] = np.where(df["Sinyal"] == "AL", 1, 0)
df["Strateji_Getiri_%"] = df["Pozisyon"].shift(1) * df["Günlük_Getiri_%"]

# ==========================================
# 3. KÜMÜLATİF BİLEŞİK SERİLER (ÇARPANLAR)
# ==========================================
df["Strateji_Küm"] = (1 + (df["Strateji_Getiri_%"] / 100)).cumprod()
df["THYAO_Hold_Küm"] = (1 + (df["Günlük_Getiri_%"] / 100)).cumprod()
df["BIST_Küm"] = (1 + (df["BIST_Getiri_%"] / 100)).cumprod()

# ==========================================
# 4. GETİRİ EĞRİSİ (EQUITY CURVE) GRAFİĞİ
# ==========================================
plt.figure(figsize=(12, 6))

# Çizgileri ekleme
plt.plot(df.index, df["Strateji_Küm"], label="V2.1 Strateji (SMA + RSI)", color="blue", linewidth=2)
plt.plot(df.index, df["THYAO_Hold_Küm"], label="THYAO Al & Yat (Buy & Hold)", color="red", linestyle="--", alpha=0.7)
plt.plot(df.index, df["BIST_Küm"], label="BIST 100 Benchmark", color="gray", linestyle=":", alpha=0.7)

# Referans Başlangıç Çizgisi (1.00 Seviyesi)
plt.axhline(y=1.00, color="black", linestyle="-.", alpha=0.5, label="Başlangıç Sermayesi (1.00)")

# Grafik Detayları ve Süsleme
plt.title("THYAO Stratejisi Getiri Eğrisi (Equity Curve) vs Benchmark", fontsize=14, fontweight="bold")
plt.xlabel("Tarih", fontsize=11)
plt.ylabel("Sermaye Çarpanı (1.00 = Başlangıç)", fontsize=11)
plt.legend(loc="upper left")
plt.grid(True, linestyle="--", alpha=0.5)

# Grafiği Ekrana Basma
plt.tight_layout()
plt.show()