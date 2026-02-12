import pandas as pd
from pathlib import Path

    # 3) nacteni inputu
def main():
    data = Path(__file__).with_name("ChallengeTask_data.xlsx") #nacteni souboru
    sp = pd.read_excel(data, sheet_name="SHARE_PRICE") # nacteni listu share_price
    sph = pd.read_excel(data, sheet_name="SHARE_PRICE_HIST") # nacteni listu share_price_hist


    #  4) sjednotim den, mesic a rok s_from do jednho parametru s_from
    sp["S_FROM"]  = pd.to_datetime(dict(year=sp["S_FROM_YR"],  month=sp["S_FROM_MT"],  day=sp["S_FROM_DAY"]))
    sph["S_FROM"] = pd.to_datetime(dict(year=sph["S_FROM_YR"], month=sph["S_FROM_MT"], day=sph["S_FROM_DAY"]))

    # 5) upravim ts_from na format zahrnujici az sekundy pro posouzeni, jaky zaznam je aktualni (nejnovejsi oprava)
    sp["TS_FROM"]  = pd.to_datetime(sp["TS_FROM"],  format="%Y-%m-%d-%H.%M.%S.%f")
    sph["TS_FROM"] = pd.to_datetime(sph["TS_FROM"], format="%Y-%m-%d-%H.%M.%S.%f")

    # 6) sjednotim nazvy tabulek share_price a share_price_hist pro cenu)
    sp_u  = sp.rename(columns={"SHARE_PRICE": "PRICE"})
    sph_u = sph.rename(columns={"AMOUNT": "PRICE"})

    # 7) vynecham sloupce, se kterymi dal nechci pracovat, a spojim share_price a share_price_hist do jednoho dataframu a znovu oindexuji
    df = pd.concat(
    [sp_u[["COMPANY","CURRENCY","S_FROM","TS_FROM","PRICE"]],
     sph_u[["COMPANY","CURRENCY","S_FROM","TS_FROM","PRICE"]]],
    ignore_index=True
)

    # 8) zbaveni se duplikatu - pro stejna s_from se necha to s nejnovejsim ts_from
    df = df.sort_values(["S_FROM", "TS_FROM"])
    df = df.drop_duplicates(subset=["S_FROM"], keep="last")

    # ------------------------ NEW pro reseni 3 ---------------------------------------------------

    # 9) seradim vsechny ceny do seznamu podle data s_from
    df = df.sort_values("S_FROM") #serazeni
    prices = df["PRICE"].astype(float).to_list() # vezmu jen ceny jako seznam hodnot.

    # 10)  stav bohatstvi v prubehu obchdoovani
    start_cash = 100_000.0
    start = start_cash          # stav pred transakcemi (kpital mam u sebe)
    trans1  = float("-inf")       # pocet akcii po 1. transakci, all in nakupu.
    trans2 = float("-inf")       # pocet financi po 2. transakci, all out prodeji
    trans3  = float("-inf")       # pocet akcii po 3. transakci, all in nakupu

    # 11) iterace pres ceny v seznamu
    for p in prices:                # prochazim ceny v seznamu

        trans1  = max(trans1,  start / p)   # aktualizuju trans1 jako to vetsi dvojice trans1 predesleho p a start/p:nakupu akcii za aktualni jmeni.
        trans2 = max(trans2, trans1 * p)    # stejne jako trans1, ale akcie naopak prodavam a merim finance.
        trans3  = max(trans3,  trans2 / p)   # analogicky k trans1

    p_today = prices[-1]  # cena akcii v oslednim datu ("dnes").

    wealth0 = start                  # pocatecni stav financi
    wealth1 = trans1 * p_today       # pocet financi po prvni transakci (v prepoctu podle "dnesni" ceny akcii)
    wealth2 = trans2                 # pocet financi po druhe transakci
    wealth3 = trans3 * p_today       # pocet financi po treti transakci (v prepoctu podle "dnesni" ceny akcii)

    best = max(wealth0, wealth1, wealth2, wealth3) #hleda nejlepsi kombinaci pro nejvetsi pozustatek pri stavek pred a po kazde transakci.
    print(f"Max wealth: {best:.2f} EUR") # vypise celkovy stav financi na konci
    print(f"Max profit: {best - start_cash:.2f} EUR") # vypise zisk tim, ze od stavu na konci odecte kapital.


if __name__ == "__main__":
    main()
