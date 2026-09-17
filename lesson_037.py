import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run_quant_pipeline(
    ticker="THYAO.IS", 
    benchmark="XU100.IS", 
    period="6mo",
    fast_sma=5, 
    slow_sma=20, 
    rsi_period=14, 
    rsi_thresh=50,
    risk_free_rate=0.45 # Türkiye yıllık risksiz faiz oranı tahmini (%45)
):
    print(f"\n---> {ticker} ({period}) Sharpe & MDD Analizli Backtest Başlatılıyor...")
    
    # 1. VERİ ÇEKME
    df = yf.Ticker(ticker).history(period=period)
    df_bist = yf.Ticker(benchmark).history(period=period)

    if df.empty or df_bist.empty:
        print(f"HATA: {ticker} veya {benchmark} için veri çekilemedi!")
        return None

    df["Günlük_Getiri_%"] = df["Close"].pct_change() * 100
    df["BIST_Getiri_%"] = df_bist["Close"].pct_change() * 100

    # 2. İNDİKATÖR VE SİNYAL HESAPLAMA
    df["SMA_Fast"] = df["Close"].rolling(window=fast_sma).mean()
    df["SMA_Slow"] = df["Close"].rolling(window=slow_sma).mean()

    delta = df["Close"].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain, index=df.index).rolling(window=rsi_period).mean()
    avg_loss = pd.Series(loss, index=df.index).rolling(window=rsi_period).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # Sinyal & Pozisyon
    kosul_al = (df["SMA_Fast"] > df["SMA_Slow"]) & (df["RSI"] > rsi_thresh)
    df["Sinyal"] = np.where(kosul_al, "AL", "SAT")
    df["Pozisyon"] = np.where(df["Sinyal"] == "AL", 1, 0)
    df["Strateji_Getiri_%"] = df["Pozisyon"].shift(1) * df["Günlük_Getiri_%"]

    # 3. KÜMÜLATİF GETİRİLER, MDD VE SHARPE HESAPLAMA
    df["Strateji_Küm"] = (1 + (df["Strateji_Getiri_%"] / 100)).cumprod()
    df["Hold_Küm"] = (1 + (df["Günlük_Getiri_%"] / 100)).cumprod()
    df["BIST_Küm"] = (1 + (df["BIST_Getiri_%"] / 100)).cumprod()

    # MDD Hesaplama
    df["Strateji_Zirve"] = df["Strateji_Küm"].cummax()
    df["Strateji_DD_%"] = ((df["Strateji_Küm"] - df["Strateji_Zirve"]) / df["Strateji_Zirve"]) * 100
    strat_mdd = df["Strateji_DD_%"].min()

    # --- SHARPE RATIO MATEMATİĞİ ---
    # Günlük getirilerin ortalaması ve standart sapması (yıllıklandırılmış)
    daily_returns = df["Strateji_Getiri_%"] / 100
    mean_daily_return = daily_returns.mean()
    std_daily_return = daily_returns.std()

    # 252 işlem günü üzerinden yıllıklandırma
    annual_return = mean_daily_return * 252
    annual_volatility = std_daily_return * np.sqrt(252)

    # Sharpe Oranı Oranı (Risk-Free Rate çıkarılarak)
    if annual_volatility > 0:
        sharpe_ratio = (annual_return - (risk_free_rate / 100)) / annual_volatility
    else:
        sharpe_ratio = 0.0

    # Rapor Metrikleri
    strat_perf = (df["Strateji_Küm"].iloc[-1] - 1) * 100
    hold_perf = (df["Hold_Küm"].iloc[-1] - 1) * 100
    bist_perf = (df["BIST_Küm"].iloc[-1] - 1) * 100
    alfa_vs_bist = strat_perf - bist_perf

    # 4. GÖRSELLEŞTİRME VE KAYDETME
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Strateji_Küm"], label=f"Strateji (SMA {fast_sma}/{slow_sma} + RSI {rsi_thresh})", color="#1f77b4", linewidth=2)
    plt.plot(df.index, df["Hold_Küm"], label=f"{ticker} Al & Yat", color="#d62728", linestyle="--", alpha=0.7)
    plt.plot(df.index, df["BIST_Küm"], label="BIST 100 Benchmark", color="#7f7f7f", linestyle=":", alpha=0.7)
    plt.axhline(y=1.00, color="black", linestyle="-.", alpha=0.4, label="Başlangıç Sermayesi (1.00)")

    info_text = (
        f"Strateji Getirisi: %{strat_perf:.2f}\n"
        f"Strateji MDD: %{strat_mdd:.2f}\n"
        f"Sharpe Ratio: {sharpe_ratio:.2f}\n"
        f"-------------------\n"
        f"{ticker} Al & Yat: %{hold_perf:.2f}\n"
        f"BIST 100 Alfa (α): %{alfa_vs_bist:.2f}"
    )
    plt.gca().text(
        0.98, 0.05, info_text, transform=plt.gca().transAxes,
        fontsize=9, verticalalignment='bottom', horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.85, edgecolor='gray')
    )

    plt.title(f"{ticker} ({period}) Backtest & Sharpe Raporu", fontsize=14, fontweight="bold")
    plt.xlabel("Tarih", fontsize=11)
    plt.ylabel("Sermaye Çarpanı", fontsize=11)
    plt.legend(loc="upper left")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()

    output_filename = f"{ticker}_{period}_Sharpe_report.png"
    plt.savefig(output_filename, dpi=300)
    plt.close()

    return {
        "Hisse": ticker,
        "Strateji_%": round(strat_perf, 2),
        "Sharpe": round(sharpe_ratio, 2),
        "MDD_%": round(strat_mdd, 2),
        "Al_Yat_%": round(hold_perf, 2),
        "Alfa_%": round(alfa_vs_bist, 2)
    }

if __name__ == "__main__":
    portfoy = ["THYAO.IS", "GARAN.IS", "AKBNK.IS", "EREGL.IS", "KCHOL.IS"]
    ozet_sonuclar = []

    for hisse in portfoy:
        sonuc = run_quant_pipeline(ticker=hisse, period="6mo", fast_sma=5, slow_sma=20, rsi_thresh=50)
        if sonuc:
            ozet_sonuclar.append(sonuc)

    ozet_df = pd.DataFrame(ozet_sonuclar)
    print("\n================ TOPLU QUANT PERFORMANS VE SHARPE TABLOSU ================")
    print(ozet_df.to_string(index=False))
    print("==========================================================================")