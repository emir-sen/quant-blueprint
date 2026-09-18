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
    commission_rate=0.002,
    slippage_rate=0.001
):
    df = yf.Ticker(ticker).history(period=period)
    df_bist = yf.Ticker(benchmark).history(period=period)

    if df.empty or df_bist.empty:
        return None

    df["Günlük_Getiri_%"] = df["Close"].pct_change() * 100
    df["BIST_Getiri_%"] = df_bist["Close"].pct_change() * 100

    # İndikatörler
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

    # Maliyetler & Net Getiri
    df["İşlem_Var_mı"] = df["Pozisyon"].diff().abs().fillna(0)
    toplam_maliyet_orani = commission_rate + slippage_rate
    
    df["Strateji_Brüt_Getiri_%"] = df["Pozisyon"].shift(1) * df["Günlük_Getiri_%"]
    df["Strateji_Net_Getiri_%"] = df["Strateji_Brüt_Getiri_%"] - (df["İşlem_Var_mı"] * toplam_maliyet_orani * 100)

    # Kümülatif & Sharpe
    df["Strateji_Küm"] = (1 + (df["Strateji_Net_Getiri_%"] / 100)).cumprod()
    
    daily_returns = df["Strateji_Net_Getiri_%"] / 100
    mean_daily_return = daily_returns.mean()
    std_daily_return = daily_returns.std()

    annual_return = mean_daily_return * 252
    annual_volatility = std_daily_return * np.sqrt(252)

    sharpe_ratio = (annual_return - (risk_free_rate / 100)) / annual_volatility if annual_volatility > 0 else 0.0
    strat_perf = (df["Strateji_Küm"].iloc[-1] - 1) * 100

    return {
        "Fast_SMA": fast_sma,
        "Slow_SMA": slow_sma,
        "RSI_Thresh": rsi_thresh,
        "Net_Getiri_%": round(strat_perf, 2),
        "Net_Sharpe": round(sharpe_ratio, 2)
    }

def grid_search_optimization(ticker="AKBNK.IS", period="6mo"):
    print(f"\n---> {ticker} İçin En İdeal Parametreler Aranıyor (Grid Search)...")
    
    # Denediğimiz Parametre Kombinasyonları
    fast_sma_list = [3, 5, 10]
    slow_sma_list = [15, 20, 30]
    rsi_thresh_list = [45, 50, 55]

    results = []

    for fast in fast_sma_list:
        for slow in slow_sma_list:
            if fast >= slow:  # Hızlı SMA, Yavaş SMA'dan büyük/eşit olamaz
                continue
            for rsi in rsi_thresh_list:
                res = run_quant_pipeline(
                    ticker=ticker, 
                    period=period, 
                    fast_sma=fast, 
                    slow_sma=slow, 
                    rsi_thresh=rsi
                )
                if res:
                    results.append(res)

    res_df = pd.DataFrame(results)
    # En yüksek Net Sharpe getiren parametreye göre sırala
    res_df = res_df.sort_values(by="Net_Sharpe", ascending=False)
    
    print(f"\n================ {ticker} GRID SEARCH OPTİMİZASYON SONUÇLARI ================")
    print(res_df.head(5).to_string(index=False)) # En iyi 5 kombinasyon
    print("==========================================================================")

if __name__ == "__main__":
    # Zarar ettiğimiz AKBNK üzerinde en iyi parametre kombinasyonunu arayalım
    grid_search_optimization(ticker="AKBNK.IS", period="1y")