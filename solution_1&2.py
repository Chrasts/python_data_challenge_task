import pandas as pd
from pathlib import Path

    # 1) funkce pro oznaceni prviho dne mesice - z libivolneho dne nejakeho mesice udela prvni den mesice
def first_day_of_month(d) -> pd.Timestamp:
    t = pd.Timestamp(d)          
    return pd.Timestamp(t.year, t.month, 1)

    # 2) funkce pro oznaceni prviho dne dawiho mesice - pro libovolny den udela prvni den nasaledujiciho mesice
def first_day_of_next_month(d) -> pd.Timestamp:
    t = pd.Timestamp(d)
    if t.month == 12:
        return pd.Timestamp(t.year + 1, 1, 1) # "if" rewici prechod mezi roky
    return pd.Timestamp(t.year, t.month + 1, 1)

    # 3) nacteni inputu
def main():
    data = Path(__file__).with_name("ChallengeTask_data.xlsx") #nacteni souboru
    sp = pd.read_excel(data, sheet_name="SHARE_PRICE") # nacteni listu share_price
    sph = pd.read_excel(data, sheet_name="SHARE_PRICE_HIST") # nacteni listu share_price_hist


    #  4) sjednotim den, mesic a rok s_from do jednho parametru s_from
    sp["S_FROM"]  = pd.to_datetime(dict(year=sp["S_FROM_YR"],  month=sp["S_FROM_MT"],  day=sp["S_FROM_DAY"]))
    sph["S_FROM"] = pd.to_datetime(dict(year=sph["S_FROM_YR"], month=sph["S_FROM_MT"], day=sph["S_FROM_DAY"]))

    # 5) upravim ts_from na format zahrnujici az sekundy pro posouzeni, jaky zaznam je aktualni (nejnovejwi oprava)
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

    # 8) zbaveni se duplikatu - pro rows se stenymi dvojicemi (S_FROM, COMPANY) se necha to s nejnovejsim ts_from
    df = df.sort_values(["COMPANY", "CURRENCY", "S_FROM", "TS_FROM"])
    df = df.drop_duplicates(subset=["COMPANY", "CURRENCY", "S_FROM"], keep="last")


    prices = df.copy() # vysledna tabulka vzikla sjednocenim share_price a share_price_hist, sjednocenim nazvu, zbaveni se duplikatu, etc. viz kroky vyw

    min_s_from = prices["S_FROM"].min()  # ze sloupce s_from tabulky prices ulozim nejmenwi (nejstarwi) datum jako min_s_from, abych vedel, kdy data v inputu zcinaji.

    # 9) funkce pro ziskani radku, u nichz je s_from menwrovno boundary mesice
    def pick_row_at_or_before(df_prices, boundary):    
        cand = df_prices[df_prices["S_FROM"] <= boundary] # mnozina "kandidatu", radku, jejichz s_from je menwi 1. den priwtiho mesice (boundary). 
        return cand.sort_values("S_FROM").iloc[-1] # seradim prvky mnoziny cand a vezme psoledni (tedy nejnovejwi, nejbliz k boundary).

    # 10) nastaveni boundary mesice a promennych pro while loop
    T0 = first_day_of_month(min_s_from) # T0 je prvni den mesice nejstarwiho data v input data
    if min_s_from == T0:              
        T = T0   # kdyz je prvni cena akcii datovana k prvnimu dni mesice, zacnu od nej (protoze zmeny pocitame vzdy od prvniho dne mesice, a chceme tedy prvni mesic zahrnout)
    else: T = first_day_of_next_month(T0) #jinak zacnu az dalwim mesicem, protoze prvni mesic je "neúplny" a nemuzu tak urcit rozdil cen akcii od prvniho dne mesice do prvniho dne dalwiho mesice.

    s2 = None # pripravim si promennou
    output_rows = [] # sem budu ukladat vysledne radky pro OUTPUT

    last_s_from = prices["S_FROM"].max() # promenna urcujici posledni zmenu ceny akcii podle s_from
    last_boundary = first_day_of_next_month(first_day_of_month(last_s_from)) #prvni den mesice M, kde mesic M je pvni mesic nsaledujici po posledni zmene akcii last_s_from (prvni mesic, co uz neni v input datch). Bude nam slouzit k zastaveni while loopu.

    # 11) while loop prochizejici jednotlive mesice a pocitajici rozdily cen akcii.
    while True:    # while loop bezici, dokud ho nezastavi break
        T_next = first_day_of_next_month(T) 

        if T_next > last_boundary: 
            break   # pokud je prvni den priwtiho mesice last boudnary, prowli jsme vwechna input data serazena podle dat, a while loop se ukonci


        if s2 is None:
            s1 = pick_row_at_or_before(prices, T)   # pokud s1 nema hodnotu (prvni iterace while loopu), vezmeme row s s_from menwirovno T (zacatek mesice)
        else: s1 = s2 #pokud s1 uz ma hodnotu, da se s1 hodnota S2 (posuneme se o mesic)

        s2 = pick_row_at_or_before(prices, T_next) # za s2 dosadim row s s_from menwirovno T_next (zacatek dalwiho mesice)D

        d1 = float(s1["PRICE"])
        d2 = float(s2["PRICE"]) # hodnoty akcii radku s1 a s2
        d = d2 - d1 # jejich rozdil


        currency = str(s1["CURRENCY"]) # currency radku pojemnuju proste currency
        company  = str(s1["COMPANY"]) # stejne pro company
        if d != 0:
            output_rows.append((d, currency, company, T.month, T.year)) # pokud je rozdil cen akcii na zcatku mesice a na zacatku priwtiho mesice nenulovy, vypiwu ten rozdil spolu s menou, spolecnosti, a mesicem a rokem.
        else:   
            pass # pokud je rozdil nulovy (behem mesice nedowlo ke zmenam nebo se zmeny behem mesice anulovaly), nevypiwu nic.
       
        T = T_next # na konci loopu posunu T na dalwi mesic, aby dalwi iterace while loopu pracovala s dalwim mesicem.


    print(len(output_rows)) # vypiwu pocet ziskanych radku  voutput souboru
    output = pd.DataFrame(output_rows, columns=["DELTA_AMOUNT","CURRENCY","COMPANY","CHANGE_MT","CHANGE_YR"]) # udela dataframe ze ziskanych output radku while loopu
    output.to_excel("OUTPUT.xlsx") # vytvori xlsx soubor pro tento dataframe



if __name__ == "__main__": # brani tomu, aby se main spouwtelo pri importu (napad AI)
    main()

