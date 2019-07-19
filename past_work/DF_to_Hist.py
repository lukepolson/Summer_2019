import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
from ast import literal_eval

def get_lag_time_col(row):
    if (row['LBNumber']>=157 and row['LBNumber']<=189):
        return 0
    elif (row['LBNumber']>=190 and row['LBNumber']<=252):
        return 12.5
    elif (row['LBNumber']>=253 and row['LBNumber']<=284):
        return 6.25
    elif (row['LBNumber']>=285 and row['LBNumber']<=313):
        return 18.75
    elif (row['LBNumber']>=315 and row['LBNumber']<=347):
        return 3.125
    elif (row['LBNumber']>=349 and row['LBNumber']<=398):
        return 21.875
    elif (row['LBNumber']>=399 and row['LBNumber']<=420):
        return 12.5
    else:
        return 1000
    
def DF_to_sorted_CSV(READ_PATH):
    # Seperate into sorted CSV files
    BIG_DF = pd.DataFrame(columns=COLUMNS)
    for (i,filename) in enumerate(os.listdir(READ_PATH)):
        if i%20==0:
            BIG_DF['groups']=pd.cut(BIG_DF['HwidCell'],group_intervals)
            grouped = BIG_DF.groupby('groups')
            for name, group in grouped:
                file_loc = READ_PATH+'csvs/cell_'+str(name)+'.csv'
                with open(file_loc, 'a') as f:
                    group.sort_values(by=['HwidCell']).to_csv(f, header=f.tell()==0, sep=';')
            del(BIG_DF)
            BIG_DF = pd.DataFrame(columns=COLUMNS)
            
        if filename.endswith(".pkl"):
            opened_df = pd.read_pickle(READ_PATH+filename)
            BIG_DF = pd.concat([opened_df, BIG_DF])
            del(opened_df)

def sorted_CSV_to_histo(READ_PATH, df_of_histograms):
    for (i,filename) in enumerate(os.listdir(READ_PATH)):
        if filename.endswith(".csv"):
            opened_df = pd.read_csv(READ_PATH+filename, 'sep=;')
            opened_df['ADC'] = opened_df['ADC'].apply(literal_eval)
            opened_df['LagTime'] = opened_df.apply(get_lag_time_col, axis=1)
        
        grouped = opened_df.groupby('HwidCell')
        for cell, df in grouped:
            histo_df = histo_df_skeleton
            for index, row in df.iterrows():
                t = list(times + row['LagTime'])
                new_row = row['ADC']/row['ECell']
                histo_df = histo_df.append(dict(zip(t, new_row)), ignore_index=True)

            weighted = True
            if weighted:
                w_df = histo_df.where(pd.isnull,1).mul(weights, axis='rows')
                w_df = w_df.multiply(1 / w_df.sum(axis=0), axis=1)
                std_corr1 = w_df.sum(axis=0)**2; std_corr2 = (w_df**2).sum(axis=0)
                w_df = w_df.mul(w_df.describe().T['count'], axis=1)
        
            histo_df = (histo_df * w_df).describe()
            histo_df = histo_df.append(pd.Series(std_corr1/std_corr2, name='mean_std_corr'))
        
            means = histo_df.T['mean'].values
            errs = (histo_df.T['std']/np.sqrt(histo_df.T['mean_std_corr'])).values
            df_of_histograms.append(dict(zip(df_of_hists_cols, [HwidCell, means, errs])))
    
    return df_of_histograms
        

            
sr = 25
times = np.arange(0,32,1, dtype=float)*sr
group_intervals = np.arange(0, 248000, 1000)

tt_bins = np.arange(0, 32+7, 1)*sr
histo_df_skeleton = pd.DataFrame(columns=list(tt_bins))
df_of_hists_cols = ['HwidCell', 'Means', 'Errors']
df_of_hists = pd.DataFrame(columns=df_of_hists_cols)

READ_PATH_DF = '/Users/lukepolson/Documents/test_data/pulse_347848/'
READ_PATH_CSV = '/Users/lukepolson/Documents/test_data/pulse_347848/csvs/'

COLUMNS = ['RunNumber','LBNumber',  'EventNumber','BCID','LArError','ncells', 'ECell',
            'TCell', 'EtaCell', 'PhiCell', 'LayerCell','ProvCell', 'QuaCell','GainCell',
            'HwidCell','ADC',]


DF_to_sorted_CSV(READ_PATH_DF)
sorted_CSV_to_histo(READ_PATH_CSV, df_of_hists).to_csv(READ_PATH_DF+'big_csv.csv')