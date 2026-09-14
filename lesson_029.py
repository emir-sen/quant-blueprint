import yfinance as yf
import numpy as np

# 1. Veri Çekme
thyao = yf.Ticker("THYAO.IS")
df = thyao.history(period="3mo")

# 2. İndikatör ve Getiri Hesaplama
df["Günlük_Getiri_%"] = df["Close"].pct_change() * 100
df["SMA_5"] = df["Close"].rolling(window=5).mean()
df["SMA_20"] = df["Close"].rolling(window=20).mean()

# 3. Sinyal ve Pozisyon
df["Sinyal"] = np.where(df["SMA_5"] > df["SMA_20"], "AL", "SAT")
df["Pozisyon"] = np.where(df["Sinyal"] == "AL", 1, 0)

# 4. Strateji Getirisi (Look-ahead bias engellenmiş)
df["Strateji_Getiri_%"] = df["Pozisyon"].shift(1) * df["Günlük_Getiri_%"]

# --- SHARPE RATIO HESAPLAMA ---

# 1. Günlük Risksiz Faiz Oranı (Yıllık %40 varsayımı ile günlük ~0.1%)
risk_free_rate_daily = 0.1 / 100

# 2. Stratejinin Ortalama Günlük Getirisi ve Standart Sapması
mean_daily_return = df["Strateji_Getiri_%"].mean()
std_daily_return = df["Strateji_Getiri_%"].std()

# 3. Günlük Sharpe Oranı
daily_sharpe = (mean_daily_return - risk_free_rate_daily) / std_daily_return

# 4. Yıllıklandırılmış Sharpe Oranı (Yılda 252 işlem günü var)
annual_sharpe = daily_sharpe * np.sqrt(252)

print(f"Strateji Ortalama Günlük Getiri: %{mean_daily_return:.4f}")
print(f"Strateji Günlük Standart Sapma (Risk): %{std_daily_return:.4f}")
print(f"Yıllıklandırılmış Sharpe Oranı: {annual_sharpe:.2f}")

# --- MAXIMUM DRAWDOWN (MAKSİMUM DÜŞÜŞ) HESAPLAMA ---

# 1. Stratejinin kümülatif (toplam) getiri serisi
df["Strateji_Küm_Getiri"] = df["Strateji_Getiri_%"].cumsum()

# 2. Zirve Noktası (Cumulative Max): O güne kadar görülen EN YÜKSEK kümülatif getiri
df["Zirve"] = df["Strateji_Küm_Getiri"].cummax()

# 3. Düşüş (Drawdown): Şu anki değerin zirveden ne kadar aşağıda olduğu
df["Drawdown"] = df["Strateji_Küm_Getiri"] - df["Zirve"]

# 4. En derin düşüş noktası (Maximum Drawdown)
max_drawdown = df["Drawdown"].min()

print(f"Maksimum Düşüş (Maximum Drawdown): %{max_drawdown:.2f}")