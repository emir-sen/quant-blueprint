import yfinance as yf
import numpy as np
import pandas as pd

# ==========================================
# 1. VERİ ÇEKME
# ==========================================
thyao = yf.Ticker("THYAO.IS")
df = thyao.history(period="3mo")

# Kapanış getirisi (Tam Yüzde % cinsinden)
df["Günlük_Getiri_%"] = df["Close"].pct_change() * 100

# ==========================================
# 2. İNDİKATÖR HESAPLAMALARI (SMA & RSI)
# ==========================================
# Hareketli Ortalamalar
df["SMA_5"] = df["Close"].rolling(window=5).mean()
df["SMA_20"] = df["Close"].rolling(window=20).mean()

# RSI (14 Günlük) Hesaplaması
delta = df["Close"].diff() # Günlük fiyat farkı

# Kazanç (Gain) ve Kayıp (Loss) ayrımları
gain = np.where(delta > 0, delta, 0)
loss = np.where(delta < 0, -delta, 0)

# 14 günlük Ortalama Kazanç ve Kayıp (Wilder's Smoothing / Rolling Mean)
avg_gain = pd.Series(gain, index=df.index).rolling(window=14).mean()
avg_loss = pd.Series(loss, index=df.index).rolling(window=14).mean()

# RS (Relative Strength) ve RSI Formülü
rs = avg_gain / avg_loss
df["RSI_14"] = 100 - (100 / (1 + rs))

# ==========================================
# 3. STRATEJİ SİNYALİ VE POZİSYON (RSI FİLTRELİ)
# ==========================================
# KOŞUL: Hem SMA_5 > SMA_20 olacak HEM DE RSI_14 > 50 olacak (& operatörü ile bağladık)
kosul_al = (df["SMA_5"] > df["SMA_20"]) & (df["RSI_14"] > 50)

df["Sinyal"] = np.where(kosul_al, "AL", "SAT")
df["Pozisyon"] = np.where(df["Sinyal"] == "AL", 1, 0)

# Look-ahead bias engelleme
df["Strateji_Getiri_%"] = df["Pozisyon"].shift(1) * df["Günlük_Getiri_%"]

# ==========================================
# 4. BİLEŞİK GETİRİ VE SHARPE HESAPLAMALARI
# ==========================================
# Risksiz Günlük Faiz (%0.1 Tam Yüzde)
risk_free_rate_daily = 0.1

mean_daily_return = df["Strateji_Getiri_%"].mean()
std_daily_return = df["Strateji_Getiri_%"].std()

daily_sharpe = (mean_daily_return - risk_free_rate_daily) / std_daily_return
annual_sharpe = daily_sharpe * np.sqrt(252)

# Bileşik Kümülatif Getiri (Oran üzerinden)
df["Strateji_Oran"] = df["Strateji_Getiri_%"] / 100
df["Strateji_Küm_Bileşik"] = (1 + df["Strateji_Oran"]).cumprod()

# Drawdown Hesabı
df["Zirve_Bileşik"] = df["Strateji_Küm_Bileşik"].cummax()
df["Drawdown_%"] = ((df["Strateji_Küm_Bileşik"] - df["Zirve_Bileşik"]) / df["Zirve_Bileşik"]) * 100
max_drawdown = df["Drawdown_%"].min()

# Nihai Bilanço
toplam_bileşik_getiri = (df["Strateji_Küm_Bileşik"].iloc[-1] - 1) * 100

# ==========================================
# 5. RAPORLAMA
# ==========================================
print("=== THYAO V2.1 (SMA + RSI FİLTRELİ) BACKTEST RAPORU ===")
print(f"Ortalama Günlük Getiri  : %{mean_daily_return:.4f}")
print(f"Günlük Volatilite (Risk): %{std_daily_return:.4f}")
print(f"Yıllıklandırılmış Sharpe: {annual_sharpe:.2f}")
print("-------------------------------------------------")
print(f"Toplam Bileşik Getiri   : %{toplam_bileşik_getiri:.2f}")
print(f"Maksimum Düşüş (MDD)    : %{max_drawdown:.2f}")