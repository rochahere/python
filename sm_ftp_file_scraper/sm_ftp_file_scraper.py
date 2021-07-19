from ftplib import FTP
import os
import shutil
from datetime import date, timedelta
from wells import locations
import glob
from pprint import pprint
import logging

# Logger configurator
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(
  filename = "scrape_hmi.log",
  level = logging.INFO,
  format = LOG_FORMAT
)
logger = logging.getLogger()

wells_missing = []
dates = []

def get_dates(days_back=9):
  for i in range(days_back, 0, -1):
    yesterday = date.today() - timedelta(days=i)
    file_to_look = yesterday.strftime("%y%m%d") + '00.CSV'
    dates.append(file_to_look)
  return dates

def get_missing_files(days_back = 9):
  get_dates(days_back)
  x = 0
  for i in locations:
    files = []
    missing_dates = []
    if locations[i]['odd'] == False:
      os.chdir(locations[i]['directory'])
      for file in glob.glob('*00.CSV'):
        files.append(file)
      # Prints missing files
      for d in dates:
        if d not in files:
          missing_dates.append(d)
      wells_missing.append([i])
      wells_missing[x].append(missing_dates)
      x += 1
  return wells_missing

def relocate_file(file, location):
    shutil.copy2(file, location + file)

def remove_csv_files():
  dir_name = 'R:\Dept\SCADA\Control Room\Code\Scrape HMI'
  test = os.listdir(dir_name)
  for item in test:
    if item.endswith(".CSV"):
        os.remove(os.path.join(dir_name, item))

def run_scrape(number_of_days = 9):
  logger.info('Startig app with number_of_days = %s', number_of_days)
  get_dates(number_of_days)
  logger.info('Checking dates between ' + dates[0][:-6] + "-" + dates[-1][:-6])
  new_locations = {k:v for k, v in locations.items() if v['odd'] == False}
  for well, value in new_locations.items():
    try:
      print('Working on well: ' + well + ' - ' + value['host'])
      logger.info('Working on well: ' + well + ' - ' + value['host'])
      try:
        with FTP(value['host'], value['ftp_user'], value['ftp_pass']) as ftp:
          if ftp.getwelcome() == '220 Hello':
            ftp.cwd('/LOGS/Casing')
            for file in dates:
              try:
                with open(file, 'wb') as fhandle:
                  ftp.retrbinary('RETR ' + file, fhandle.write)
                  print('Saving file: ' + well + ' - ' + file + '...' )
                  logger.info('Successful: ' + well + ' - ' + file)
              except Exception as e:
                print(e)
                print('There was an error with the file name')
                logger.warning(e)
                logger.warning('Error on well %s - %s', well, value['host'])
                continue
              try:
                relocate_file(file, value['directory'])
              except Exception as e:
                print(e)
                print('There was a problem with file relocation')
                logger.warning(e)
                logger.warning('There was a problem with file relocation')
            print('Removing Files from: ' + well)
            remove_csv_files()
          else:
            print('Unable to connect to %s - %s', well, value['host'])
            ftp.quit()
      except Exception as e:
        print(e)
        logger.warning(e)
    except Exception as e:
      print(e)
      print('There was an error with the FTP connection')
      logger.warning('There was an error with the FTP connection')
  for i in get_missing_files(number_of_days):
    logger.warning(i)
  get_missing_files(number_of_days)

def run_scrape_odds():
  logger.info('Startig app (Odds)')
  new_locations = {k:v for k, v in locations.items() if v['odd'] == True}
  for well, value in new_locations.items():
    try:
      print('Working on well: ' + well + ' - ' + value['host'])
      logger.info('Working on well: ' + well + ' - ' + value['host'])
      try:
        with FTP(value['host'], value['ftp_user'], value['ftp_pass']) as ftp:
          if ftp.getwelcome() == '220 Hello':
            ftp.cwd('/LOGS/Casing')
            names = ftp.nlst()
            csv_names = [line for line in names if '.CSV' in line]
            csv_filenames = [
            for i in csv_names:
              csv_filenames.append(int(i[-12:-4]))
            to_pop = max(csv_filenames)
            x = 0
            for p in csv_filenames:
              if p == to_pop:
                csv_filenames.pop(x)
              x += 1
            for file in csv_filenames:
              csv_to_download = str(file) + '.CSV'
              try:
                  with open(csv_to_download, 'wb') as fhandle:
                      ftp.retrbinary('RETR '+ csv_to_download, fhandle.write)
                      logger.info('Successful: ' + well + ' - ' + csv_to_download)
              except Exception as e:
                  print(e)
                  print('There was an error with the file name')
                  logger.warning(e)
                  logger.warning('Error on well %s - %s', well, value['host'])
                  continue
              try:
                relocate_file(csv_to_download, value['directory'])
              except Exception as e:
                print(e)
                print('There was a problem with file relocation')
                logger.warning(e)
                logger.warning('There was a problem with file relocation')
            print('Removing Files from: ' + well)
            remove_csv_files()
            ftp.quit()
          else:
            print('Unable to connect to %s - %s', well, value['host'])
            ftp.quit()
      except Exception as e:
        print(e)
        logger.warning(e)
    except Exception as e:
      print(e)
      print('There was an error with the FTP connection')
      logger.warning('There was an error with the FTP connection')

run_scrape()
run_scrape_odds()

print('CSV files missing: ')
pprint(get_missing_files())




]
