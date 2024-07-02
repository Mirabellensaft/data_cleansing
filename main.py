import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import datetime as dt


# helper functions
def replace_midnight(line):
    
    # print(line.time())
        if line.time() == dt.datetime.min.time():
            # print(line.time())
            # print("time change")
            time_change = dt.timedelta(hours=24) 
            line = line + time_change 
            # print(line)
            return line
        else:
            # print(line)
            return line
        

def test_continuity(dates, previous):
    for line in dates:

        if line.time() == dt.datetime.min.time():
            time_change = dt.timedelta(hours=24) 
            line = line + time_change 
            # print("line change")
                # print(line)


        time_change = dt.timedelta(minutes=15) 
        new_time = previous + time_change 

        if line != new_time:
            print("Error")
            print(previous, line)     
    
        previous = line
        

def test_weekdays(dictionary):
    for dictionary in data_dict:
        day = dictionary.get('date')
        date_obj = dt.datetime.strptime(day, "%d/%m/%Y %H:%M")
        weekday = dictionary.get('Day_of_week')
        status = dictionary.get('WeekStatus')

        match date_obj.weekday():
            case 0: 
                if weekday != "Monday":
                    print("Weekday Error")
                if status != "Weekday":
                    print("Weekstatus Error")

            case 1:
                if weekday != "Tuesday":
                    print("Weekday Error")
                if status != "Weekday":
                    print("Weekstatus Error")
            case 2:
                if weekday != "Wednesday":
                    print("Weekday Error")
                if status != "Weekday":
                    print("Weekstatus Error")
            case 3: 
                if weekday != "Thursday":
                    print("Weekday Error")
                if status != "Weekday":
                    print("Weekstatus Error")
            case 4:
                if weekday != "Friday":
                    print("Weekday Error")
                if status != "Weekday":
                    print("Weekstatus Error")
            case 5:
                if weekday != "Saturday":
                    print("Weekday Error")
                if status != "Weekend":
                    print("Weekstatus Error")
            case 6:
                if weekday != "Sunday":
                    print("Weekday Error")
                if status != "Weekend":
                    print("Weekstatus Error")

# ingest csv
steel_industry = pd.read_csv("Steel_industry_data.csv", parse_dates=True)

# print head of table
print(steel_industry.head())

# create a new column, date_parsed, with the parsed dates
steel_industry['date_parsed'] = pd.to_datetime(steel_industry['date'], format="%d/%m/%Y %H:%M")


pd.set_option('display.max_columns', None)
print(steel_industry.describe())

# Create subsets for data during working hours and off-hours
weekdays = steel_industry[steel_industry['WeekStatus'].str.contains('Weekday')]
workinghours = weekdays.query('NSM < 79200 and NSM > 28800')
non_workinghours = weekdays.query('NSM < 28800 or NSM > 79200')


print("weekdays working hours")
print(workinghours.describe())
print(non_workinghours.describe())

# test continuity of dates

# sets a fictional timestamp 15 min before the first 
previous = dt.datetime(2018, 1, 1, 0, 0, 0) 
dates = steel_industry["date_parsed"]
test_continuity(dates, previous)

# fix order of timestamps 
steel_industry['fixed_dates'] = steel_industry["date_parsed"].apply(replace_midnight)


df = steel_industry.set_index('fixed_dates')

data_dict = steel_industry.to_dict(orient='records')
test_weekdays(data_dict)

#Check for duplicate and null(missing) values
print(steel_industry.loc[(steel_industry['Lagging_Current_Reactive_Power_kVarh']== 0) & (steel_industry['Leading_Current_Reactive_Power_kVarh']== 0)])
print(steel_industry['Day_of_week'].unique())
print(steel_industry['WeekStatus'].unique())
print(steel_industry['Usage_kWh'].isnull())
print(steel_industry.isna())




print(steel_industry.loc[(steel_industry['Load_Type']== 'Light_Load') & (steel_industry['Usage_kWh'] > 130)])

# outlier detection
print(steel_industry.loc[(steel_industry['Usage_kWh'] > 133)])
# steel_industry.loc[(steel_industry['Usage_kWh'] < 1.5)] = steel_industry.quantile(.25)
print(steel_industry.loc[(steel_industry['CO2(tCO2)'] > 1)])
# calculate IQR for column Height
# Q1 = df['Height'].quantile(0.25)
# Q3 = df['Height'].quantile(0.75)
# IQR = Q3 - Q1

# # identify outliers
# threshold = 1.5
# outliers = df[(df['Height'] < Q1 - threshold * IQR) | (df['Height'] > Q3 + threshold * IQR)


# correlation
print("Correlation")
print(steel_industry["Usage_kWh"].corr(steel_industry['CO2(tCO2)']))
print(steel_industry['Leading_Current_Reactive_Power_kVarh'].corr(steel_industry['Lagging_Current_Reactive_Power_kVarh']))
print(steel_industry["Usage_kWh"].corr(steel_industry['Lagging_Current_Reactive_Power_kVarh']))
print(steel_industry["Usage_kWh"].corr(steel_industry['Leading_Current_Reactive_Power_kVarh']))
print(steel_industry["Usage_kWh"].corr(steel_industry['Lagging_Current_Power_Factor']))
print(steel_industry["Usage_kWh"].corr(steel_industry['Leading_Current_Power_Factor']))
print(steel_industry['Lagging_Current_Power_Factor'].corr(steel_industry['Leading_Current_Power_Factor']))

# plots

# df = steel_industry.set_index('date_parsed')
# plt.xlabel('Month')
# plt.ylabel('Energy Usage [kWh]')
# plt.title("Distribution of Energy Usage Peaks")
# plt.plot(df.index, steel_industry['Usage_kWh'])
# plt.axhline(y = 133, color = 'r', linestyle = '-') 
# plt.plot(df.index, steel_industry['Lagging_Current_Reactive_Power_kVarh'])
# plt.plot(df.index, steel_industry['Leading_Current_Reactive_Power_kVarh'])
plt.show()

# plotting current and kWh
fig, ax1 = plt.subplots()
plt.plot(df.index, steel_industry['Usage_kWh'], color='tab:blue', label='Energy Usage')  # Plot some data on the axes.
ax2 = ax1.twinx()
ax2.plot(df.index, steel_industry['CO2(tCO2)'], color='tab:red', label='CO2') 
# ax2.plot(df.index, steel_industry['Lagging_Current_Reactive_Power_kVarh'], color='tab:green',label='Lagging_Current_Reactive_Power')  # Plot more data on the axes...
# ax2.plot(df.index, steel_industry['Leading_Current_Reactive_Power_kVarh'], color='tab:orange',label='Leading_Current_Reactive_Power')  # ... and some more.
# ax2.plot(df.index, steel_industry['Lagging_Current_Power_Factor'], color='tab:red', label='Lagging_Current_Power_Factor')  # Plot more data on the axes...
# ax2.plot(df.index, steel_industry['Leading_Current_Power_Factor'], color='tab:green', label='Leading_Current_Power_Factor')  # ... and some more.
ax1.set_xlabel('Day')  # Add an x-label to the axes.
ax1.set_ylabel('Energy Usage [kWh]')  # Add an x-label to the axes.
ax2.set_ylabel("CO2 [ppm]")  # Add a y-label to the axes.
ax1.set_title('CO2 Emission in relation to Energy Usage')  # Add a title to the axes.

# labels = ['Leading_Current_Reactive_Power', 'Lagging_Current_Reactive_Power', 'Energy Usage']

# plt.legend()
fig.legend() 
plt.show()


# Assuming you have a DataFrame named 'data' with columns 'timestamp', 'energy1', 'energy2', 'energy3'
# Convert the 'timestamp' column to datetime format and set it as the index of the DataFrame
steel_industry['timestamps'] = pd.to_datetime(steel_industry['fixed_dates'])
steel_industry.set_index('timestamps', inplace=True)

# Resample the DataFrame to ensure it is evenly spaced at 15-minute intervals
data_resampled = steel_industry.resample('24h')  # Change '15T' to match your desired frequency

print("Load")
low_load = data_resampled[data_resampled['Load_Type'].str.contains('Maximum_Load')]

print(low_load.describe())
# Calculate autocorrelation for each energy consumption value
# autocorrelation_energy1 = data_resampled['Usage_kWh'].autocorr()
# autocorrelation_energy2 = data_resampled['Lagging_Current_Reactive_Power_kVarh'].autocorr()
# autocorrelation_energy3 = data_resampled['Leading_Current_Reactive_Power_kVarh'].autocorr()

# print("Autocorrelation for Usage_kWh:", autocorrelation_energy1)
# print("Autocorrelation for Lagging_Current_Reactive_Power_kVarh:", autocorrelation_energy2)
# print("Autocorrelation for Leading_Current_Reactive_Power_kVarh:", autocorrelation_energy3)


    

# # print(rows, entries)