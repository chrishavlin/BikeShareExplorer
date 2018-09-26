import matplotlib.pyplot as plt
import pandas as pd

def portlandRides(dataDir,minDate='2011-01-01',maxDate='2050-01-01'):
    # read in portland bulk file
    df=pd.read_csv(dataDir+'/PortlandBulk.csv',low_memory=False)

    # group and sort it
    dfg=df.groupby(['StartDate'])['Distance_Miles'].agg(['sum','count','median','mean'])
    dfg.reset_index(inplace=True)
    dfg['dt']=pd.to_datetime(dfg.StartDate)
    dfg.sort_values(by='dt',inplace=True)

    dfg=dfg[dfg.dt>=pd.to_datetime(minDate)]
    dfg=dfg[dfg.dt<=pd.to_datetime(maxDate)]

    # make a plot thing
    plt.subplot(2,1,1)
    plt.plot(dfg.dt,dfg['count'],'.k')
    plt.plot(dfg.dt,dfg['count'],'k')
    plt.ylabel('Number of Rides')
    plt.subplot(2,1,2)
    plt.plot(dfg.dt,dfg['median'],'.k')
    plt.plot(dfg.dt,dfg['median'],'k')
    plt.xlabel('date')
    plt.ylabel('Median Ride Distance [mi]')
    plt.show()
