import numpy as np
import pandas as pd
import uproot

def get_nonzero(arr):
    return arr[np.nonzero(arr)]

def hist_to_df(histo):
    
    '''
    This code takes in a histogram stored in a ROOT file and returns a DataFrame containing
      1. The center of each bin stored as the "times"
      2. The ADC/energy = signal in each bin
      3. The standard deviation at each time point
      4. The standard deviation of the mean estimator at each time point.
      
    See _____ document for how these quantities are computed (and why they are the same as the way
    ROOT computes these quantities). The source code of TProfile had to be examined. For now see
    Logbook July 18 2019.
    
    '''
    
    histo_df = histo.pandas()
      
    fBinEntries = get_nonzero(np.array(histo._fBinEntries)[1:-1])
    fBinSumw2 = get_nonzero(np.array(histo._fBinSumw2)[1:-1])
    fSumw2 = get_nonzero(np.array(histo._fSumw2)[1:-1])
    fBin = get_nonzero(np.array(histo_df['count']))
    
    # Get Times
    times = np.array(histo_df.index.mid)
    
    # Get Signal
    signal = fBin/fBinEntries
    
    # Get Standard deviation and Standard Deviation of Mean Estimator
    N_eff = fBinEntries**2 / fBinSumw2
    eprim2 = np.abs((fSumw2/fBinEntries)-(fBin/fBinEntries)**2)
    bin_std_mean = np.sqrt(eprim2/N_eff)
    bin_std = np.sqrt(eprim2)
    
    # Construct DataFrame and Return
    plotting_df = pd.DataFrame()
    plotting_df['t'] = times
    plotting_df['s'] = signal
    plotting_df['std'] = bin_std
    plotting_df['std_mean'] = bin_std_mean
    
    return plotting_df

def hist_to_df_uw(histo):
    
    '''
    This code takes in a histogram stored in a ROOT file and returns a DataFrame containing
      1. The center of each bin stored as the "times"
      2. The ADC/energy = signal in each bin
      3. The standard deviation at each time point
      4. The standard deviation of the mean estimator at each time point.
      
    See _____ document for how these quantities are computed (and why they are the same as the way
    ROOT computes these quantities). The source code of TProfile had to be examined. For now see
    Logbook July 18 2019.
    
    '''
    
    histo_df = histo.pandas()
      
    fBinEntries = get_nonzero(np.array(histo._fBinEntries)[1:-1])
    fSumw2 = get_nonzero(np.array(histo._fSumw2)[1:-1])
    fBin = get_nonzero(np.array(histo_df['count']))
    
    # Get Times
    times = np.array(histo_df.index.mid)
    
    # Get Signal
    signal = fBin/fBinEntries
    
    # Get Standard deviation and Standard Deviation of Mean Estimator
    N_eff = fBinEntries
    eprim2 = np.abs((fSumw2/fBinEntries)-(fBin/fBinEntries)**2)
    bin_std_mean = np.sqrt(eprim2/N_eff)
    bin_std = np.sqrt(eprim2)
    
    # Construct DataFrame and Return
    plotting_df = pd.DataFrame()
    plotting_df['t'] = times
    plotting_df['s'] = signal
    plotting_df['std'] = bin_std
    plotting_df['std_mean'] = bin_std_mean
    
    return plotting_df




    
    