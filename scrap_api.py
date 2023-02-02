import pandas as pd
from pybliometrics.scopus import AbstractRetrieval
from tqdm import tqdm
import time
import warnings
from make_conf import rework_config
import os

def change_config(i):
    with open(r'.\api_keys.txt', 'r') as f:
        res = f.readlines()
    rework_config(res[i])
    return True

def do_something(a):
    a = a[a['date']>='2021-01-01']
    return a

def main():
    os.mkdir(r'.\inter_bases')
    warnings.filterwarnings("ignore")
    new = do_something(pd.read_excel(r'.\total_result.xlsx'))
    number_of_except=0
    df_total = pd.DataFrame()
    df_med = pd.DataFrame()
    i=0
    n=0
    configs = 0
    change_config(0)
    start = time.time()
    for eid in tqdm(new['eid']):
        while True:
            try:
                time.sleep(1)
                ab = AbstractRetrieval(eid, view='FULL')
                break
            except Exception as e:
                print(e)
                i+=1
                change_config(i)
                continue
        try:
            rrr = ab.__dict__
            r1 = {}
            for key in rrr:
                r1[key] = [rrr[key]]
            df_inter = pd.DataFrame.from_dict(r1)
        except:
            print(ab)
            number_of_except += 1
            continue
        df_total = pd.concat([df_total, df_inter])
        df_med = pd.concat([df_med, df_inter])
        if i % 100 == 0 or i == new.shape[0] - 1:
            sta_1 = time.time() - start
            print('Общее время обработки, секунд: ', sta_1)
            df_med.to_excel('.\inter_bases\med_base_' + str(n) + '.xlsx')
            n += 1
            df_med = pd.DataFrame()
        i+=1
        df_total.to_excel('base.xlsx')
    print('Общее время обработки результатов, секунд: ', time.time()-start)
    print('Общее кол-во ошибок:', number_of_except)

main()