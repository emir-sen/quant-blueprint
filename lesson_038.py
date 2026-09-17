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
    risk_free_rate=0.45,
    commission_rate=0.002, # BİST Ortalama Komisyon (%0.2)
    slippage_rate=0.001    # Tahmini Kayma Maliyeti (%0.1)
):
    print(f"\n---> {ticker} ({period}) Maliyet Entegreli Backtest Başlatılıyor...")
    
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
    
    # --- GERÇEK DÜNYA İŞLEM MALİYETİ MATEMATİĞİ ---
    # Pozisyon değişimlerini tespit et (0'dan 1'e veya 1'den 0'a geçişler)
    # abs(diff) bize işlem yapılan günlerde 1, yapılmayan günlerde 0 verir
    df["İşlem_Var_mı"] = df["Pozisyon"].diff().abs().fillna(0)
    
    # Toplam İşlem Maliyeti (Komisyon + Kayma)
    toplam_maliyet_orani = commission_rate + slippage_rate
    
    # Brüt Getiri (Maliyetsiz)
    df["Strateji_Brüt_Getiri_%"] = df["Pozisyon"].shift(1) * df["Günlük_Getiri_%"]
    
    # Net Getiri: İşlem yapılan günlerde maliyet düşülür
    # İşlem günü % oranına çevrilmiş maliyet (örn: 0.003 * 100 = %0.3) düşülür
    df["Strateji_Net_Getiri_%"] = df["Strateji_Brüt_Getiri_%"] - (df["İşlem_Var_mı"] * toplam_maliyet_orani * 100)

    # 3. KÜMÜLATİF GETİRİLER VE SHARPE HESAPLAMA (NET GETİRİ İLE)
    df["Strateji_Küm"] = (1 + (df["Strateji_Net_Getiri_%"] / 100)).cumprod()
    df["Hold_Küm"] = (1 + (df["Günlük_Getiri_%"] / 100)).cumprod()
    df["BIST_Küm"] = (1 + (df["BIST_Getiri_%"] / 100)).cumprod()

    # MDD Hesaplama
    df["Strateji_Zirve"] = df["Strateji_Küm"].cummax()
    df["Strateji_DD_%"] = ((df["Strateji_Küm"] - df["Strateji_Zirve"]) / df["Strateji_Zirve"]) * 100
    strat_mdd = df["Strateji_DD_%"].min()

    # Net Sharpe Ratio
    daily_returns = df["Strateji_Net_Getiri_%"] / 100
    mean_daily_return = daily_returns.mean()
    std_daily_return = daily_returns.std()

    annual_return = mean_daily_return * 252
    annual_volatility = std_daily_return * np.sqrt(252)

    if annual_volatility > 0:
        sharpe_ratio = (annual_return - (risk_free_rate / 100)) / annual_volatility
    else:
        sharpe_ratio = 0.0

    # Rapor Metrikleri
    strat_perf = (df["Strateji_Küm"].iloc[-1] - 1) * 100
    hold_perf = (df["Hold_Küm"].iloc[-1] - 1) * 100
    bist_perf = (df["BIST_Küm"].iloc[-1] - 1) * 100
    alfa_vs_bist = strat_perf - bist_perf
    toplam_islem_sayisi = int(df["İşlem_Var_mı"].sum())

    # 4. GÖRSELLEŞTİRME VE KAYDETME
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Strateji_Küm"], label=f"Net Strateji (Maliyet Dâhil)", color="#1f77b4", linewidth=2)
    plt.plot(df.index, df["Hold_Küm"], label=f"{ticker} Al & Yat", color="#d62728", linestyle="--", alpha=0.7)
    plt.plot(df.index, df["BIST_Küm"], label="BIST 100 Benchmark", color="#7f7f7f", linestyle=":", alpha=0.7)
    plt.axhline(y=1.00, color="black", linestyle="-.", alpha=0.4, label="Başlangıç Sermayesi (1.00)")

    info_text = (
        f"Net Strateji Getirisi: %{strat_perf:.2f}\n"
        f"Toplam İşlem Sayısı: {toplam_islem_sayisi}\n"
        f"Net Sharpe Ratio: {sharpe_ratio:.2f}\n"
        f"Strateji MDD: %{strat_mdd:.2f}\n"
        f"-------------------\n"
        f"{ticker} Al & Yat: %{hold_perf:.2f}\n"
        f"BIST 100 Alfa (α): %{alfa_vs_bist:.2f}"
    )
    plt.gca().text(
        0.98, 0.05, info_text, transform=plt.gca().transAxes,
        fontsize=9, verticalalignment='bottom', horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.85, edgecolor='gray')
    )

    plt.title(f"{ticker} ({period}) Gerçek Dünya Maliyetli Backtest Raporu", fontsize=14, fontweight="bold")
    plt.xlabel("Tarih", fontsize=11)
    plt.ylabel("Sermaye Çarpanı", fontsize=11)
    plt.legend(loc="upper left")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()

    output_filename = f"{ticker}_{period}_Net_Report.png"
    plt.savefig(output_filename, dpi=300)
    plt.close()

    return {
        "Hisse": ticker,
        "Net_Getiri_%": round(strat_perf, 2),
        "İşlem_Sayısı": toplam_islem_sayisi,
        "Net_Sharpe": round(sharpe_ratio, 2),
        "MDD_%": round(strat_mdd, 2),
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
    print("\n================ NET PERFORMANS VE İŞLEM MALİYETİ ÖZET TABLOSU ================")
    print(ozet_df.to_string(index=False))
    print("==============================================================================")