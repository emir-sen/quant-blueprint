# TL Cinsinden
portfoy_tl = [1000, 2500, 5000, 10000]

# Dolar cinsinden (Güncel 48 TL yaklaşık)
portfoy_dolar = [round(fiyat / 48, 2) for fiyat in portfoy_tl]

print(f"Dolar portföyü: {portfoy_dolar}")