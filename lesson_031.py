import yfinance as yf
import numpy as np
import pandas as pd

# ==========================================
# 1. VERİ ÇEKME (HISSE & BENCHMARK)
# ==========================================
thyao = yf.Ticker("THYAO.IS")
bist = yf.Ticker("XU100.IS")

df = thyao.history(period="3mo")
df_bist = bist.history(period="3mo")

# Getiriler (Tam Yüzde % Cinsinden)
df["Günlük_Getiri_%"] = df["Close"].pct_change() * 100
df["BIST_Getiri_%"] = df_bist["Close"].pct_change() * 100

# ==========================================
# 2. İNDİKATÖRLER VE STRATEJİ SİNYALİ (V2.1)
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

# Pozisyon (Look-ahead bias engellenmiş)
kosul_al = (df["SMA_5"] > df["SMA_20"]) & (df["RSI_14"] > 50)
df["Sinyal"] = np.where(kosul_al, "AL", "SAT")
df["Pozisyon"] = np.where(df["Sinyal"] == "AL", 1, 0)
df["Strateji_Getiri_%"] = df["Pozisyon"].shift(1) * df["Günlük_Getiri_%"]

# ==========================================
# 3. KÜMÜLATİF BİLEŞİK GETİRİ HESAPLAMALARI
# ==========================================
# Strateji Kümülatif Getirisi
df["Strateji_Oran"] = df["Strateji_Getiri_%"] / 100
df["Strateji_Küm_Bileşik"] = (1 + df["Strateji_Oran"]).cumprod()
strateji_toplam_getiri = (df["Strateji_Küm_Bileşik"].iloc[-1] - 1) * 100

# BIST 100 (Benchmark) Kümülatif Getirisi (Buy & Hold)
df["BIST_Oran"] = df["BIST_Getiri_%"] / 100
df["BIST_Küm_Bileşik"] = (1 + df["BIST_Oran"]).cumprod()
bist_toplam_getiri = (df["BIST_Küm_Bileşik"].iloc[-1] - 1) * 100

# THYAO Buy & Hold Kümülatif Getirisi (Hisseye dokunmadan tutma)
df["THYAO_Oran"] = df["Günlük_Getiri_%"] / 100
df["THYAO_Küm_Bileşik"] = (1 + df["THYAO_Oran"]).cumprod()
thyao_hold_toplam_getiri = (df["THYAO_Küm_Bileşik"].iloc[-1] - 1) * 100

# Alfa (Ekstra Getiri)
alfa_vs_bist = strateji_toplam_getiri - bist_toplam_getiri
alfa_vs_hold = strateji_toplam_getiri - thyao_hold_toplam_getiri

# ==========================================
# 4. BENCHMARK KARŞILAŞTIRMA RAPORU
# ==========================================
print("=== THYAO V2.2 BENCHMARK PERFORMANS RAPORU ===")
print(f"Strateji Bileşik Getirisi : %{strateji_toplam_getiri:.2f}")
print(f"BIST 100 (Benchmark)      : %{bist_toplam_getiri:.2f}")
print(f"THYAO (Al & Yat)          : %{thyao_hold_toplam_getiri:.2f}")
print("-------------------------------------------------")
print(f"BIST 100'e Göre Alfa (α)  : %{alfa_vs_bist:.2f}")
print(f"Al & Yat'a Göre Alfa (α)   : %{alfa_vs_hold:.2f}")