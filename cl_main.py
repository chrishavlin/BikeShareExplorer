"""
main for initial command line program
"""
import sys,os
import matplotlib.pyplot as plt
from src import data
from src import cl_plots

def pullData():
    """ pulls the latest data where possible """
    dataDir=os.path.abspath('./data/')
    dt=data.data({'dataDir':dataDir})
    dt.portlandFetch()
    dt.portlandProc()
    return

def initialPlots():
    cl_plots.portlandRides(os.path.abspath('./data/'))
    cl_plots.portlandRides(os.path.abspath('./data/'),'2017-01-01','2018-01-01')
    return

if __name__=='__main__':
    print("welcome to the Bike Share Explorer, command line version")

    methlist='pullData, initialPlots'
    if len(sys.argv) < 2:
        print("\nPlease provide a method argument:")
        print("  python cl_main.py method=pullData")
        print("  where method may be: "+methlist)
    else:
        if sys.argv[1].split('=')[1]=='pullData':
            print("\nAttempting to pull latest data")
            pullData()
        elif sys.argv[1].split('=')[1]=='initialPlots':
            print("\ntrying a plot")
            initialPlots()
