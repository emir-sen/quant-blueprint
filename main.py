import sys
import argparse
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run_quant_engine(ticker, period, fast_sma, slow_sma, rsi_thresh, comm_rate, slip_rate):
    print(f"\n================ QUANT BACKTEST ENGINE V3.0 FINAL ================")
    print(f"Hisse: {ticker} | Periyot: {period} | SMA: {fast_sma}/{slow_sma} | RSI Eşik: {rsi_thresh}")
    print(f"====================================================================")

    # 1. VERİ ÇEKME
    df = yf.Ticker(ticker).history(period=period)
    df_bist = yf.Ticker("XU100.IS").history(period=period)

    if df.empty or df_bist.empty:
        print("HATA: Veri çekilemedi! Hisse kodunu veya internet bağlantınızı kontrol edin.")
        return

    df["Günlük_Getiri_%"] = df["Close"].pct_change() * 100
    df["BIST_Getiri_%"] = df_bist["Close"].pct_change() * 100

    # 2. İNDİKATÖR HESAPLAMA
    df["SMA_Fast"] = df["Close"].rolling(window=fast_sma).mean()
    df["SMA_Slow"] = df["Close"].rolling(window=slow_sma).mean()

    delta = df["Close"].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain, index=df.index).rolling(window=14).mean()
    avg_loss = pd.Series(loss, index=df.index).rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # 3. SİNYAL VE POZİSYON
    kosul_al = (df["SMA_Fast"] > df["SMA_Slow"]) & (df["RSI"] > rsi_thresh)
    df["Sinyal"] = np.where(kosul_al, "AL", "SAT")
    df["Pozisyon"] = np.where(df["Sinyal"] == "AL", 1, 0)

    # 4. İŞLEM MALİYETLERİ VE NET GETİRİ
    df["İşlem_Var_mı"] = df["Pozisyon"].diff().abs().fillna(0)
    toplam_maliyet = comm_rate + slip_rate
    
    df["Strateji_Brüt_%"] = df["Pozisyon"].shift(1) * df["Günlük_Getiri_%"]
    df["Strateji_Net_%"] = df["Strateji_Brüt_%"] - (df["İşlem_Var_mı"] * toplam_maliyet * 100)

    # 5. KÜMÜLATİF GETİRİ VE RISK METRİKLERİ
    df["Strateji_Küm"] = (1 + (df["Strateji_Net_%"] / 100)).cumprod()
    df["Hold_Küm"] = (1 + (df["Günlük_Getiri_%"] / 100)).cumprod()

    df["Zirve"] = df["Strateji_Küm"].cummax()
    df["DD_%"] = ((df["Strateji_Küm"] - df["Zirve"]) / df["Zirve"]) * 100

    strat_perf = (df["Strateji_Küm"].iloc[-1] - 1) * 100
    hold_perf = (df["Hold_Küm"].iloc[-1] - 1) * 100
    mdd = df["DD_%"].min()

    daily_ret = df["Strateji_Net_%"] / 100
    annual_ret = daily_ret.mean() * 252
    annual_vol = daily_ret.std() * np.sqrt(252)
    sharpe = (annual_ret - 0.45) / annual_vol if annual_vol > 0 else 0.0

    toplam_islem = int(df["İşlem_Var_mı"].sum())

    # 6. KONSOL ÇIKTISI
    print(f"-> Net Strateji Getirisi : %{strat_perf:.2f}")
    print(f"-> Hisse Al & Yat Getirisi: %{hold_perf:.2f}")
    print(f"-> Maksimum Çekilme (MDD) : %{mdd:.2f}")
    print(f"-> Net Sharpe Ratio       : {sharpe:.2f}")
    print(f"-> Toplam İşlem Sayısı    : {toplam_islem}")
    print(f"====================================================================\n")

if __name__ == "__main__":
    # Command Line Interface (CLI) Parametre Yakalayıcı
    parser = argparse.ArgumentParser(description="Quant Backtest Engine V3.0 Final")
    
    parser.add_argument("--ticker", type=str, default="THYAO.IS", help="BİST Hisse Kodu (Örn: GARAN.IS)")
    parser.add_argument("--period", type=str, default="1y", help="Veri Aralığı (Örn: 6mo, 1y, 2y)")
    parser.add_argument("--fast", type=int, default=5, help="Hızlı SMA")
    parser.add_argument("--slow", type=int, default=20, help="Yavaş SMA")
    parser.add_argument("--rsi", type=int, default=50, help="RSI Eşik Değeri")
    
    args = parser.parse_args()
    
    run_quant_engine(
        ticker=args.ticker, 
        period=args.period, 
        fast_sma=args.fast, 
        slow_sma=args.slow, 
        rsi_thresh=args.rsi,
        comm_rate=0.002,
        slip_rate=0.001
    )