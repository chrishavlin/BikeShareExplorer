"""
src/data.py

class for data manipulation
"""
import urllib,os,requests,datetime
import pandas as pd
from dateutil.relativedelta import relativedelta

class data(object):
    def __init__(self,attdict=None):
        if attdict is not None:
            for key in attdict.keys():
                setattr(self,key,attdict[key])

        if hasattr(self, 'dataDir') is False:
            print("WARNING: data.data() class must be initialized with dataDir attribute:")
            print("  data.data({'dataDir':'path/to/dataDir'})")


    def urlexists(self,urlstr):
        try:
            check=requests.head(urlstr)
            if check.status_code<400:
                return True
            else:
                return False
        except Exception:
            return False

    def portlandFetchSingleFile(self,year,month,overwrite=False):
        """ downloads a single portland file """
        urlbase='https://s3.amazonaws.com/biketown-tripdata-public/'

        # build file and url strings
        mo=str(month)
        if month<10:
            mo='0'+mo

        thefile=str(year)+'_'+mo+'.csv'
        urlstr=urlbase+thefile

        # check the portland data directory
        saveDir=self.dataDir+'/portland_files'
        if os.path.isdir(saveDir) is False:
            os.mkdir(saveDir)

        # download file if it does not exist (or if overwriting)
        if os.path.isfile(saveDir+'/'+thefile) is False or overwrite:
            if self.urlexists(urlstr):
                print(" downloading "+urlstr+" to "+saveDir)
                opener = urllib.URLopener()
                opener.retrieve(urlstr, saveDir+'/'+thefile)
            else:
                print(" "+urlstr+" does not exist")
        else:
            print(" "+urlstr+" already downloaded")

        return

    def portlandFetch(self):
        """ fetches latest data for portland bikeshare (biketown) """
        fetchdate=datetime.date(2016,7,1)
        today=datetime.date.today()
        finaldate=datetime.date(today.year,today.month-1,1)
        while fetchdate <= finaldate:
            self.portlandFetchSingleFile(fetchdate.year,fetchdate.month)
            fetchdate=fetchdate+relativedelta(months=1)

        return

    def portlandProc(self):
        """ processes the downloaded portland files """
        print("Processing portland files")
        dir=self.dataDir+'/portland_files/'
        df=None
        for fi in os.listdir(dir):
            print dir+fi
            if os.path.isfile(dir+fi):
                print("loading "+fi)
                dfi=pd.read_csv(dir+fi,low_memory=False)
                if df is None:
                    df=dfi.copy(deep=True)
                else:
                    df=pd.concat([df,dfi])
        df.sort_values(by=['StartDate','StartTime'],inplace=True)
        df.to_csv(self.dataDir+'/PortlandBulk.csv',index=False)

        return
