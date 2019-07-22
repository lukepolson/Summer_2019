# used with a standard figure
def plotter_macro(ax, plotting_dfs, hwid):
    plotting_df = plotting_dfs[hwid]
    
    times = plotting_df['t']
    signal = plotting_df['s']
    signal_err = plotting_df['std']
    
    ax.scatter(times, signal, color='r', s=5, label='Energy Weighted Signal Mean', zorder=2)       
    ax.errorbar(times, signal, yerr=signal_err, ls='',
             ecolor='k', capthick=1, markersize=1, zorder=1, label='Standard Deviation')

    ax.set_xlabel('Time (ns)')
    ax.set_ylabel('ADC/Energy [arb]')
    ax.grid(which='both')
    ax.legend(fontsize=12)
    ax.set_title('Hwid = {}'.format(hwid), fontsize=16)

# should be used with a figure defined as follows:
# fig, ax = plt.subplots(nrows=2, gridspec_kw={'height_ratios': [3, 1]}, sharex=True, figsize=(10,5))
def plotter_macro_comp(ax, plotting_dfs, plotting_dfs_uw, hwid):
    plotting_df = plotting_dfs[hwid]
    plotting_df_uw = plotting_dfs_uw[hwid]
    
    tt = plotting_df['t']
    ss = plotting_df['s']
    tt_uw = plotting_df_uw['t']
    ss_uw = plotting_df_uw['s']
    ss_var = plotting_df['std_mean']
    
    ax[0].scatter(tt, ss, color='r', s=2, label=r'Energy Weighted ($\bar{S}$)')
    ax[0].scatter(tt_uw, ss_uw, color='b', s=2, label=r'Normal Weighted ($\bar{S}_{UW}$)')
    ax[0].grid()
    leg1 = ax[0].legend()

    ax[1].plot(tt, ss-ss_uw, color='k', label=r'$\bar{S}-\bar{S}_{UW}$')
    ax[1].fill_between(tt, -ss_var, ss_var, color='r', alpha=0.5, label=r'$\pm \sigma_{\bar{S}}$')

    # Trick to add legend to first axis
    handles, labels = ax[1].get_legend_handles_labels()
    leg2 = ax[0].legend(handles, labels, loc='center right')
    ax[0].add_artist(leg1)

    ax[0].set_ylabel('ADC/Energy [arb]')
    ax[1].set_xlabel('Time (ns)')

    ax[0].set_title('Hwid = {}'.format(hwid), fontsize=16)