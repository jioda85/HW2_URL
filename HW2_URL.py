# ==============================================================================     
#  HW2: Class to read data from URL, process the data same as HW1, and 
#       calculate the annual mean & the standard deviation of the discharge
# ==============================================================================     
#  by InOk Jun
#  OCNG 658, Fall 2013
# ==============================================================================    

# import statement
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
import urllib


class read_data():
    '''
	This class is designed to 
	1) get the data from the USGS waterdata website using a urllib,
	2) return dates, flowrate by processing the data same as HW 1, and
	3) calculate the annual mean & the standard deviation of the discharge.
	
	Input : start_date = date of start
	        end_date   = date of end
		site_no    = number of site
        return: self.dates = dates in [date(yr, mon, day)]
	        self.flow  = discharge in [cms]
		self.mean  = mean 
		self.stdev = stdev
    '''

    def __init__(self, start_date, end_date, site_no):
        
        self.start = start_date
        self.end   = end_date
        self.site  = site_no
        
        # open URL to get the data from the USGS website
        URL = urllib.urlopen\
        ('http://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb'+\
        '&begin_date='+self.start+'&end_date='+self.end+'&site_no='+self.site)
        
        # make an empty list
        dates = []
        flow  = []
        mean  = []
        stdev = []

        # read the data using for-loop except the headerline
        for line in URL.readlines()[28:]:
            data  = line.split()
            year  = int(data[2].split('-')[0])
            month = int(data[2].split('-')[1])
            day   = int(data[2].split('-')[2])
            dates.append(date(year, month, day))
            flow.append(int(data[3]))

        # close URL for memory
        URL.close()
		
	# convert lists to arrays
        dates = np.array(dates)
        flow  = np.array(flow)
		
        # change the flowrate unit from [cfs] to [cms]
        flow = flow / 35.315 
        
        # calculate the annual mean and std. dev. of flowrate for each day
        months = np.array([d.month for d in dates])
        days   = np.array([d.day for d in dates])
        
        for idx in dates:
            cal_flow = flow[(months==idx.month) & (days==idx.day)]
            mean.append(np.mean(cal_flow))
            stdev.append(np.std(cal_flow))

	# convert lists to arrays
        mean  = np.array(mean) 
        stdev = np.array(stdev)                    
        
	# return the result
        self.dates = dates
        self.flow  = flow
        self.mean  = mean
        self.stdev = stdev

    
    
if __name__ == "__main__":

    # setup the data selection 
    start = str(date(1900,1,1))
    end   = str(date.today())
    site  = '01100000'
    
    # run the model and rearrange the result 
    foo   = read_data(start, end, site)
    dates = foo.dates
    flow  = foo.flow
    mean  = foo.mean
    stdev = foo.stdev
    
    # select the time span for plotting
    plt_year  = np.array([d.year for d in dates])
    idx = np.where(plt_year >= 2010)
    plt_dates = dates[idx]
    plt_flow  = flow[idx]
    plt_mean  = mean[idx]
    plt_upstd = mean[idx] + stdev[idx]
    plt_lwstd = mean[idx] - stdev[idx]
	
    # plot the results
    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    ax.plot(plt_dates, plt_flow, 'c', label = "Daily",  lw = 1.7)
    ax.plot(plt_dates, plt_mean, 'k', label = "Annual", lw = 1.5)
    ax.plot(plt_dates, plt_upstd, ':', color = '0.25', label = 'Upper')
    ax.plot(plt_dates, plt_lwstd, ':', color = '0.25', label = 'Lower')
	
    # decorate the plot
    plt.title('Timeseries of Discharge from 2010\n for site no.'+site, size=18)
    plt.xlabel('Dates (mm/yy)', size = 16)
    plt.ylabel('Discharge (m$^{3}$/sec)', size = 16)
    plt.legend(bbox_to_anchor=(1.02, 1), loc = 2, borderaxespad = 0.)
    plt.show()

    # save the figure
    plt.savefig('HW2_by_Jun.pdf')
