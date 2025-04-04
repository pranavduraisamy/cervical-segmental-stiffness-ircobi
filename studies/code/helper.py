import os
from pathlib import Path
import pandas as pd
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import arviz as az
_p=Path(os.getcwd())
p=_p.parent
p_data2=p.parent/'data/Nightingale2002'
p_data7=p.parent/'data/Nightingale2007'

def extract_lower_cervical():
    df2=pd.read_csv(p_data2/'clean-data/master.csv')
    df2=df2[(df2['level']!='C0C3')&(df2['level']!='C0C2')&(df2['level']!='C7T1')].copy().reset_index(drop=True)
    df7=pd.read_csv(p_data7/'clean-data/master.csv')
    df7=df7[(df7['level']!='C0C3')&(df7['level']!='C0C2')&(df7['level']!='C7T1')].copy().reset_index(drop=True)
    df=pd.concat([df2,df7],ignore_index=True)
    df['sex'] = df['sex'].map({'m':'Male','f':'Female'})
    df['loading'] = df['loading'].map({'extension':'Extension','flexion':'Flexion'})
    df['r3']=df['3.0']
    df=df.loc[:,['new_id','test_id','ref_id','sample_id','sex','age','level','loading','test','ascii_id','date','cod','r3']].copy()
    ds=xr.Dataset(
        {
            "r3": (["test_id"],df['r3']),
            "ref_id": (["test_id"],df['ref_id']),
            "sample_id": (["test_id"],df['sample_id']),
            "sex": (["test_id"],df['sex']),
            "age": (["test_id"],df['age']),
            "level": (["test_id"],df['level']),
            "loading": (["test_id"],df['loading']),
            "cod": (["test_id"],df['cod'])
        },
        coords={
            "test_id":df['new_id']
        }
    )
    ds.to_netcdf(p/'processed-data/master.nc')
    df.to_csv(p/'processed-data/master.csv',index=None)
    print('saved: master.csv')
    print('saved: master.nc')

def plot_contrast(inf,cc,xdist):
    if xdist=='Prior':
        idata=inf.prior
        nsample=500
        mns=2
    elif xdist=='Posterior':
        idata=inf.posterior
        nsample=6000
        mns=0.85

    if cc=='sex differences':
        col=['#E44E58','#17BEBB']
        lab=['Female','Male']
        A=['Extension', 'Female','Flexion', 'Female']
        B=['Extension', 'Male','Flexion', 'Male']
        subtt=['Extension','Flexion']
        cntr=' [Female-Male]'
        suptt='Comparison of Female and Male'

    elif cc=='loading differences':
        col=['#40798C','#F48366']
        lab=['Flexion','Extension']
        A=['Flexion', 'Male','Flexion', 'Female']
        B=['Extension', 'Male','Extension', 'Female']
        subtt=['Male','Female']
        cntr=' [Flexion-Extension]'
        suptt='Comparison of Flexion and Extension'

    a=idata.loading.sel({'loading_dim':A[0]})+idata['loading|sex'].sel({'sex__factor_dim':A[1],'loading__expr_dim':A[0]})
    b=idata.loading.sel({'loading_dim':B[0]})+idata['loading|sex'].sel({'sex__factor_dim':B[1],'loading__expr_dim':B[0]})
    d=a-b  
    fig,ax=plt.subplots(2,2,figsize=(8,6),sharex=True)
    fig.tight_layout(pad=2.4)
    fig.suptitle(suptt,fontsize=18,y=1.02)

    plt.sca(ax[0][0])
    al,ah=az.hdi(a,hdi_prob=0.95).x.values
    bl,bh=az.hdi(b,hdi_prob=0.95).x.values
    az.plot_dist(a,ax=ax[0][0],color=col[0],label=lab[0])
    az.plot_dist(b,ax=ax[0][0],color=col[1],label=lab[1])
    a_x,a_y= ax[0][0].lines[0].get_data()
    b_x,b_y= ax[0][0].lines[1].get_data()
    plt.fill_between(a_x,a_y, where=(al<a_x)&(a_x<ah), color=col[0], alpha= 0.4,interpolate=True)
    plt.fill_between(b_x,b_y, where=(bl<b_x)&(b_x<bh), color=col[1], alpha= 0.4,interpolate=True)
    plt.ylabel('Density',fontsize=12)
    plt.xticks(fontsize=11)
    plt.legend(fontsize=11)
    plt.title(subtt[0],fontsize=14)

    plt.sca(ax[0][1])
    kax=az.plot_dist(d,color='k',ax=ax[0][1]);
    dl,dh=az.hdi(d,hdi_prob=0.95).x.values
    x,y=kax.get_lines()[0].get_data()
    nid=(x<0)
    pid=(x>=0)
    nprb=100*np.sum(d<0)/nsample
    pprb=100*np.sum(d>=0)/nsample
    plt.axvline(x=np.mean(d), linestyle="dashed", color="black", label= "Diff Mean")
    plt.fill_between(x=x[pid], y1=np.zeros(sum(pid)), y2=y[pid],color=col[0], label=f"{pprb:1.0f}%"+lab[0])
    plt.fill_between(x=x[nid], y1=np.zeros(sum(nid)), y2=y[nid],color=col[1], label=f"{nprb:1.0f}%"+lab[1])
    plt.hlines(0.01,dl,dh,color='k',linewidth=2)
    plt.text(np.mean(d)-mns,0.05, 'mean ='+str(np.round(np.mean(d).values,2)), fontsize=11, color='k', rotation=90)
    plt.title('Contrast'+cntr+' for '+subtt[0],fontsize=14)
    plt.xticks(fontsize=11)
    plt.legend(fontsize=11)

    a=idata.loading.sel({'loading_dim':A[2]})+idata['loading|sex'].sel({'sex__factor_dim':A[3],'loading__expr_dim':A[2]})
    b=idata.loading.sel({'loading_dim':B[2]})+idata['loading|sex'].sel({'sex__factor_dim':B[3],'loading__expr_dim':B[2]})
    d=a-b
    plt.sca(ax[1][0])
    al,ah=az.hdi(a,hdi_prob=0.95).x.values
    bl,bh=az.hdi(b,hdi_prob=0.95).x.values
    az.plot_dist(a,ax=ax[1][0],color=col[0],label=lab[0])
    az.plot_dist(b,ax=ax[1][0],color=col[1],label=lab[1])
    a_x,a_y= ax[1][0].lines[0].get_data()
    b_x,b_y= ax[1][0].lines[1].get_data()
    plt.fill_between(a_x,a_y, where=(al<a_x)&(a_x<ah), color=col[0], alpha= 0.4,interpolate=True)
    plt.fill_between(b_x,b_y, where=(bl<b_x)&(b_x<bh), color=col[1], alpha= 0.4,interpolate=True)
    plt.xlabel('Rotation at 3 Nm',fontsize=12)
    plt.ylabel('Density',fontsize=12)
    plt.xticks(fontsize=11)
    plt.legend(fontsize=11)
    plt.title(subtt[1],fontsize=14)

    plt.sca(ax[1][1])
    kax=az.plot_dist(d,color='k',ax=ax[1][1]);
    dl,dh=az.hdi(d,hdi_prob=0.95).x.values
    x,y=kax.get_lines()[0].get_data()
    nid=(x<0)
    pid=(x>=0)
    nprb=100*np.sum(d<0)/nsample
    pprb=100*np.sum(d>=0)/nsample
    plt.axvline(x=np.mean(d), linestyle="dashed", color="black", label= "Diff Mean")
    plt.fill_between(x=x[pid], y1=np.zeros(sum(pid)), y2=y[pid],color=col[0], label=f"{pprb:1.0f}%"+lab[0])
    plt.fill_between(x=x[nid], y1=np.zeros(sum(nid)), y2=y[nid],color=col[1], label=f"{nprb:1.0f}%"+lab[1])
    plt.hlines(0.01,dl,dh,color='k',linewidth=2)
    plt.text(np.mean(d)-mns,0.05, 'mean ='+str(np.round(np.mean(d).values,2)), fontsize=11, color='k', rotation=90)
    plt.title('Contrast'+cntr+' for '+subtt[1],fontsize=14)
    plt.xlabel('Rotation Contrast',fontsize=12)
    plt.xticks(fontsize=11)
    plt.legend(fontsize=11)