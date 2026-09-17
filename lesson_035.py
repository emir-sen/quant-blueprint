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
    rsi_thresh=50
):
    print(f"\n---> {ticker} ({period}) Backtest Analizi Başlatılıyor...")
    
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

    # 3. KÜMÜLATİF GETİRİLER
    df["Strateji_Küm"] = (1 + (df["Strateji_Getiri_%"] / 100)).cumprod()
    df["Hold_Küm"] = (1 + (df["Günlük_Getiri_%"] / 100)).cumprod()
    df["BIST_Küm"] = (1 + (df["BIST_Getiri_%"] / 100)).cumprod()

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

    # Bilgi Kutusu Overlay
    info_text = (
        f"Strateji Getirisi: %{strat_perf:.2f}\n"
        f"{ticker} Al & Yat: %{hold_perf:.2f}\n"
        f"BIST 100 Getirisi: %{bist_perf:.2f}\n"
        f"BIST 100 Alfa (α): %{alfa_vs_bist:.2f}"
    )
    plt.gca().text(
        0.98, 0.05, info_text, transform=plt.gca().transAxes,
        fontsize=10, verticalalignment='bottom', horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='gray')
    )

    plt.title(f"{ticker} ({period}) Backtest Raporu", fontsize=14, fontweight="bold")
    plt.xlabel("Tarih", fontsize=11)
    plt.ylabel("Sermaye Çarpanı", fontsize=11)
    plt.legend(loc="upper left")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()

    # Görsel Dosya Kaydı
    output_filename = f"{ticker}_{period}_batch.png"
    plt.savefig(output_filename, dpi=300)
    plt.close()

    # Özet Veri Sözlüğü Döndürme
    return {
        "Hisse": ticker,
        "Strateji_%": round(strat_perf, 2),
        "Al_Yat_%": round(hold_perf, 2),
        "BIST100_%": round(bist_perf, 2),
        "Alfa_%": round(alfa_vs_bist, 2)
    }

if __name__ == "__main__":
    # Tarama Yapılacak Hisse Portföyü
    portfoy = ["THYAO.IS", "GARAN.IS", "AKBNK.IS", "EREGL.IS", "KCHOL.IS"]
    ozet_sonuclar = []

    # Batch Backtest Döngüsü
    for hisse in portfoy:
        sonuc = run_quant_pipeline(ticker=hisse, period="6mo", fast_sma=5, slow_sma=20, rsi_thresh=50)
        if sonuc:
            ozet_sonuclar.append(sonuc)

    # Tüm Sonuçları Karşılaştırmalı Tablo Olarak Bastırma
    ozet_df = pd.DataFrame(ozet_sonuclar)
    print("\n================ TOPLU BACKTEST ÖZET TABLOSU ================")
    print(ozet_df.to_string(index=False))
    print("=============================================================")