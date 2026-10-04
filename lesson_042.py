import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import yfinance as yf

# THYAO verisini çekiyoruz ve durağan getiri serimizi oluşturuyoruz
ticker = "THYAO.IS"
df = yf.Ticker(ticker).history(period="1y")

# Getiriyi hesaplayıp kapıdaki NaN değerini siliyoruz
returns = df["Close"].pct_change().dropna()

# 2'li Görselleştirme Alanı Hazırlıyoruz (Sol: ACF, Sağ: PACF)
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 1. GRAFİK: ACF (Otokorelasyon)
# lags=20 -> Son 20 günlük geçmiş gecikmeye bak demek.
plot_acf(returns, lags=20, ax=axes[0], title=f"{ticker} ACF (Otokorelasyon)")

# 2. GRAFİK: PACF (Kısmi Otokorelasyon)
plot_pacf(
    returns, lags=20, ax=axes[1], title=f"{ticker} PACF (Kısmi Otokorelasyon)"
)

plt.tight_layout()
plt.show()