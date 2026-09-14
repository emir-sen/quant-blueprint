import yfinance as yf
import numpy as np

# ==========================================
# 1. VERİ ÇEKME & İNDİKATÖR OLUŞTURMA
# ==========================================
thyao = yf.Ticker("THYAO.IS")
df = thyao.history(period="3mo")

# Kapanış fiyatlarından yüzdesel günlük getiriyi hesaplıyoruz [Birim: Tam Yüzde %]
# Örneğin: %2.5 kazanç ise sayı 2.5 olur.
df["Günlük_Getiri_%"] = df["Close"].pct_change() * 100

# Hareketli Ortalamalar (Moving Averages)
df["SMA_5"] = df["Close"].rolling(window=5).mean()
df["SMA_20"] = df["Close"].rolling(window=20).mean()

# ==========================================
# 2. STRATEJİ SİNYALİ VE POZİSYON ALMA
# ==========================================
# SMA 5 > SMA 20 ise AL, değilse SAT
df["Sinyal"] = np.where(df["SMA_5"] > df["SMA_20"], "AL", "SAT")
df["Pozisyon"] = np.where(df["Sinyal"] == "AL", 1, 0)

# Geleceği görme hatasını (Look-ahead bias) engellemek için shift(1) [Birim: Tam Yüzde %]
df["Strateji_Getiri_%"] = df["Pozisyon"].shift(1) * df["Günlük_Getiri_%"]

# ==========================================
# 3. PERFORMANS VE RİSK METRİKLERİ (SHARPE RATIO)
# ==========================================
# Yıllık %40 faiz varsayımıyla günlük faiz oranı [Birim: Tam Yüzde %]
# Strateji getirimiz tam yüzde (%0.15 = 0.15) olduğu için faiz de tam yüzde (%0.1 = 0.1) alınır.
risk_free_rate_daily = 0.1

mean_daily_return = df["Strateji_Getiri_%"].mean()  # [Birim: Tam Yüzde %]
std_daily_return = df["Strateji_Getiri_%"].std()    # [Birim: Tam Yüzde %]

# Günlük ve Yıllıklandırılmış Sharpe Oranı (252 işlem günü)
daily_sharpe = (mean_daily_return - risk_free_rate_daily) / std_daily_return
annual_sharpe = daily_sharpe * np.sqrt(252)

# ==========================================
# 4. BİLEŞİK KÜMÜLATİF GETİRİ VE MAKSİMUM DÜŞÜŞ (MDD)
# ==========================================
# Yüzde formatındaki sayıyı orana (decimal) çeviriyoruz (%2.5 -> 0.025)
df["Strateji_Oran"] = df["Strateji_Getiri_%"] / 100

# Bileşik Büyüme Katsayısı: (1 + Oran) ve Zincirleme Çarpım (.cumprod)
df["Strateji_Küm_Bileşik"] = (1 + df["Strateji_Oran"]).cumprod()

# O ana kadar görülmüş en yüksek bileşik rekor zirve (.cummax)
df["Zirve_Bileşik"] = df["Strateji_Küm_Bileşik"].cummax()

# Zirveden Yüzdesel Düşüş (Drawdown) [Birim: Tam Yüzde %]
df["Drawdown_%"] = ((df["Strateji_Küm_Bileşik"] - df["Zirve_Bileşik"]) / df["Zirve_Bileşik"]) * 100

# En derin çöküş noktası (Maximum Drawdown)
max_drawdown = df["Drawdown_%"].min()

# Nihai Bilanço: Tablonun EN SON SATIRINDAKİ (.iloc[-1]) bileşik katsayıyı çekiyoruz
toplam_bileşik_getiri = (df["Strateji_Küm_Bileşik"].iloc[-1] - 1) * 100

# ==========================================
# 5. RAPORLAMA VE ÇIKTILAR
# ==========================================
print("=== THYAO BACKTEST ENGINE V2 PERFORMANS RAPORU ===")
print(f"Ortalama Günlük Getiri  : %{mean_daily_return:.4f}")
print(f"Günlük Volatilite (Risk): %{std_daily_return:.4f}")
print(f"Yıllıklandırılmış Sharpe: {annual_sharpe:.2f}")
print("-------------------------------------------------")
print(f"Toplam Bileşik Getiri   : %{toplam_bileşik_getiri:.2f}")
print(f"Maksimum Düşüş (MDD)    : %{max_drawdown:.2f}")