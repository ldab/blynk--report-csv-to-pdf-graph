#Leonardo Bispo All rights reserved https://github.com/ldab
'''
Open Zip file, plot the graph and save it as a pdf.
'''

from datetime import datetime, date, time
import statistics                     #calculate median
import zipfile												#to manipulate zip
import shutil													#to delete folder
import csv														#read .csv file
import numpy as np

# Matplotlib in a web application server: do this before importing pylab or pyplot
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter

X, Y = [], []

csv_file = 'htu21d_84938_Humidity.csv'
csv_path = 'C:\\Users\\leonardo\\Downloads\\My Files\\' #ADD site path here
newfolder = 'new folder'
temp_folder = csv_path + newfolder
table_row = []

def open_zip(file_path):
  '''
  Open zip file and extract to \new folder
  '''
  newfolder = 'new folder'
  fantasy_zip = zipfile.ZipFile(file_path + 'l.bispo@live.com_blynkpvukzhpz_39740_2018-09-11.zip')
  fantasy_zip.extractall(file_path + newfolder)
  fantasy_zip.close()
    
def read_csv(csv_filepath):
  '''
  read extracted .csv file and create X and Y lists
  csv_f = "FILE PATH"
  '''
  csv_filepath = csv_path + 'new folder\\' + csv_filepath
  with open(csv_filepath, newline='', encoding='utf-16') as f:
    reader = csv.reader(f)
    for row in reader:
      table_row.append(row)
      dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
      X.append(dt)
      r_float = round(float(row[1]),1)
      Y.append(r_float)
      print(row)

def y_label(csv_path):
  '''
  Return Y label based on the file name eg. xxx_xxx_xxx_YLABEL.csv
  '''
  ylabel = csv_path.split('_')
  ylabel = ylabel[-1].split('.')
  return ylabel[0]

open_zip(csv_path)
read_csv(csv_file)

#Recover the Y lable based on the file name
ylabel = y_label(csv_file)

#Graph
gridsize = (3, 1)                               #3 rows and 1 column
fig = plt.figure(figsize=(11.69,8.27))
ax = plt.subplot2grid(gridsize, (0, 0), rowspan=2)
tx= plt.subplot2grid((3,6), (2, 1), colspan=4)

dateFmt = mdates.DateFormatter('%d-%m-%Y')
minorFmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_locator(MultipleLocator(0.2))
ax.xaxis.set_minor_locator(AutoMinorLocator(5))
ax.yaxis.set_major_locator(MultipleLocator(1.000))
ax.yaxis.set_minor_locator(AutoMinorLocator(4))
ax.xaxis.set_major_formatter(dateFmt)
ax.xaxis.set_minor_formatter(minorFmt)

ax.set_ylabel(ylabel)
ax.set_title('SOME TITLE')

#Roud data to 1 decimal place
def round_me(n, dec=1):
  '''
  round the number to x decimal places
  '''
  n = round(float(n), dec)
  return n

yMedian = round_me(statistics.median(Y))
yAverage = round_me(statistics.mean(Y))
yMax = round_me(max(Y))
yMin = round_me(min(Y))
MaxIndex = Y.index(max(Y))
MinIndex = Y.index(min(Y))
MaxTime = table_row[MaxIndex][0]
MinTime = table_row[MinIndex][0]
print(MaxTime)
print(MinTime)

tableCont = [['Maximum', yMax, MaxTime], ['Minimum', yMin, MinTime], ['Mean', yAverage, ''], ['Average', yMedian, '']]
columns = ('', ylabel, 'Date')

# Add a table at the bottom of the axes
tx.axis('tight')
tx.axis('off')
the_table  = tx.table(cellText=tableCont, colLabels=columns, loc='lower center')
the_table.set_fontsize(36)
the_table.scale(1, 1.3)

# Adjust layout to make room for the table:
#plt.subplots_adjust(left=0.1, bottom=0.3)

plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
plt.setp(ax.xaxis.get_minorticklabels(), rotation=45)

ax.grid(color='k', linestyle='-', linewidth=0.5)
ax.plot(X, Y)

plt.show()

#save file to .zip file path + file name + .pdf
fig.savefig(csv_path + csv_file.split('.')[0] + '.pdf')

DELETE = input('Delete new folder?\n Y or N? ')
if DELETE[0].lower() == 'y':
    print('Removing temporary folder......')
    shutil.rmtree(temp_folder)
else:
    print('Keep Temp folder')

#TODO Create a date list in order to compare data and avoid plotting when no data is available
#MULTIPLE PAGES PDF