#Leonardo Bispo All rights reserved https://github.com/ldab
'''
Open Zip file, plot the graph and save it as a pdf.
'''

from datetime import datetime, date, time
import statistics                     #calculate median
import zipfile												#to manipulate zip
import shutil, os											#to delete folder
import csv														#read .csv file
import numpy as np
import random
import string

# Matplotlib in a web application server: do this before importing pylab or pyplot
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter, LinearLocator, AutoLocator

tempFolder = ''
zip_File = ''

def open_zip(file_path, upload_folder):
  '''
  Open zip file and extract to /new folder
  '''
  global zip_File
  global tempFolder
  
  #generate random number/name for new folder
  tempFolder = 'temp' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
  tempFolder = upload_folder + '/' + tempFolder
  
  # This scans the directory in order to find zip files
  #for x in os.listdir(file_path):       #TODO REPLACE WITH A LAMBDA FUNCTION
  #  if x.endswith('.zip'):
  #    zip_File = x                      #Change this if want to process multiple zip files
  
  #zip_path = file_path + zip_File

  # But we will parse the zip that has already been uploaded
  zip_path = file_path
  
  fantasy_zip = zipfile.ZipFile(zip_path)
  fantasy_zip.extractall(tempFolder)
  fantasy_zip.close()
  #now delete zip file
  os.unlink(zip_path)
    
def read_csv():
  '''
  read extracted .csv file and create X and Y lists
  '''
  global tempFolder
  csv_files = []
  
  #find .csv files in the temp folder
  for f in os.listdir(tempFolder):    #TODO REPLACE WITH A LAMBDA FUNCTION
    if f.endswith('.csv'):
      csv_files.append(f)
  
  #for every file, open, print PDF and save a list with X and Y...
  for _csv in csv_files:
    X, Y, table_row = [], [], []
    csv_filepath = ''
    csv_filepath = tempFolder + '/' + _csv
    with open(csv_filepath, newline='', encoding='utf-16') as f:
      reader = csv.reader(f)
      for row in reader:
        table_row.append(row)
        dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        X.append(dt)
        r_float = round(float(row[1]),1)
        Y.append(r_float)
        #print(row)
    print_save(_csv, X, Y)

def round_me(n, dec=1):
  '''
  round the number to x decimal places
  '''
  n = round(float(n), dec)
  return n

def y_label(csv_path):
  '''
  Return Y label based on the file name eg. xxx_xxx_xxx_YLABEL.csv
  '''
  ylabel = csv_path.split('_')
  ylabel = ylabel[-1].split('.')
  return ylabel[0]

def x_label(csv_path):
  '''
  Return X label based on the file name eg. XLABEL_xxx_xxx_XXXX.csv
  '''
  xlabel = csv_path.split('_')
  return xlabel[0]

def print_save(csv_doc, X, Y):
  #Graph
  gridsize = (3, 1)                               #3 rows and 1 column
  fig = plt.figure(figsize=(11.69,8.27))          #A4 size
  ax = plt.subplot2grid(gridsize, (0, 0), rowspan=2)
  tx= plt.subplot2grid((3,6), (2, 1), colspan=4)
  
  #TODO tide it up, define minor and major
  dateFmt = mdates.DateFormatter('%d-%m-%Y')
  hourFmt = mdates.DateFormatter('%H:%M')
  dayFmt = mdates.DateFormatter('%d-%m')

  ax.xaxis.set_major_locator(LinearLocator(7))
  ax.xaxis.set_minor_locator(AutoMinorLocator())
  #ax.xaxis.set_minor_locator(LinearLocator(31))

  # Else if longer than a daily, Major = Days, Minor = Hours
  if len(X) <= (60*24*7):
    ax.xaxis.set_major_formatter(dateFmt)
    ax.xaxis.set_minor_formatter(hourFmt)

  # Else if longer than weekly, Major = Full date, Minor = day
  else:
    ax.xaxis.set_major_formatter(dateFmt)
    ax.xaxis.set_minor_formatter(dayFmt)

  ax.yaxis.set_major_locator(LinearLocator(10))
  #ax.yaxis.set_major_locator(AutoLocator())
  ax.yaxis.set_minor_locator(AutoMinorLocator(4))
  ##########################################################

  ylabel = y_label(csv_doc)
  title = x_label(csv_doc)
  ax.set_ylabel(ylabel)
  ax.set_title(title, fontsize=38)

  #calculate stuff to put in the table
  yMedian = round_me(statistics.median(Y))
  yAverage = round_me(statistics.mean(Y))
  yMax = round_me(max(Y))
  yMin = round_me(min(Y))
  MaxIndex = Y.index(max(Y))
  MinIndex = Y.index(min(Y))
  MaxTime = X[MaxIndex]
  MinTime = X[MinIndex]
 
  #create table
  tableCont = [['Maximum', yMax, MaxTime], ['Minimum', yMin, MinTime], ['Average', yAverage, ''], ['Median', yMedian, '']]
  columns = ('', ylabel, 'Date')

  #Add table at the bottom of the page
  tx.axis('tight')
  tx.axis('off')
  the_table  = tx.table(cellText=tableCont, colLabels=columns, loc='lower center')
  the_table.set_fontsize(36)
  the_table.scale(1, 1.3)

  # Rotate axis 45degress
  plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
  plt.setp(ax.xaxis.get_minorticklabels(), rotation=45)

  ax.grid(color='k', linestyle='-', linewidth=0.5)
  ax.plot(X, Y)

  #do not need it if now displaying image
  #plt.show()

  #save file to .zip file path + file name + .pdf
  fig.savefig(tempFolder + '/' + csv_doc.split('.')[0] + '.pdf')

def compress_it(zip_name):
  '''
  Compress .pdf files saved on the temp folder
  '''
  fantasy_zip = zipfile.ZipFile(tempFolder + '/' + zip_name, 'w')
    
  for folder, subfolders, files in os.walk(tempFolder):
  
      for file in files:
          if file.endswith('.pdf'):
              fantasy_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), tempFolder), compress_type = zipfile.ZIP_DEFLATED)

  print('compressing as')
  print(tempFolder + '/' + zip_name)
  fantasy_zip.close()
  return tempFolder + '/'

#open_zip(csv_path)
#read_csv()
#compress_it()

def delete_folder():
  print('Removing temporary folder......')
  shutil.rmtree(tempFolder)

#TODO Create a date list in order to compare data and avoid plotting when no data is available
