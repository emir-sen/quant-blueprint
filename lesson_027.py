import yfinance as yf
import numpy as np

thyao = yf.Ticker("THYAO.IS")
df = thyao.history(period="1mo")

# 1. Yüzdesel getiri
df["Günlük_Getiri_%"] = df["Close"].pct_change() * 100

# 2. Hareketli Ortalama (5 günlük pencere)
df["SMA_5"] = df["Close"].rolling(window=5).mean()

# 3. Al-Sat Sinyali Üretimi
df["Sinyal"] = np.where(df["Close"] > df["SMA_5"], "AL", "SAT")

# 1. Sinyali sayıya çevirelim: AL ise 1, SAT ise 0
df["Pozisyon"] = np.where(df["Sinyal"] == "AL", 1, 0)

# 2. Sinyali 1 gün kaydıralım (Dün verilen karara göre bugün işlemdeyiz)
# .shift(1) fonksiyonu veriyi 1 satır aşağı kaydırır
df["Strateji_Getiri_%"] = df["Pozisyon"].shift(1) * df["Günlük_Getiri_%"]

# 3. Toplam (Kümülatif) Getirileri Hesaplayalım
# .cumsum() fonksiyonu verileri üst üste toplayarak ilerler (cumulative sum)
df["Hisse_Toplam_Getiri"] = df["Günlük_Getiri_%"].cumsum()
df["Strateji_Toplam_Getiri"] = df["Strateji_Getiri_%"].cumsum()

# Sonuçları inceleyelim
print(df[["Close", "Sinyal", "Hisse_Toplam_Getiri", "Strateji_Toplam_Getiri"]].tail(10))