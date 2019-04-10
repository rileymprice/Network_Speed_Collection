import speedtest
from datetime import datetime as dt
import time
from path import Path
from os import path, chdir
from sys import platform
import logging

WINDOWS_LOGGER = 'E:\\Documents\\speedtest_files\\logs\\speedtest.log'
WINDOWS_FILE = 'E:\\Documents\\speedtest_files\\internet_speed.csv'
PI_LOGGER = '/home/pi/Documents/speedtest_files/logs/speedtest.log'
PI_FILE = '/home/pi/Documents/speedtest_files/internet_speed.csv'

platform_os = 'win' if str(platform) == 'win32' else 'pi'
LOG_FILE = WINDOWS_LOGGER if platform_os == 'win' else PI_LOGGER
FILE_NAME = WINDOWS_FILE if platform_os == 'win' else PI_FILE

logger = logging.getLogger('Speedtest')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def test_speed():
    '''Goal: Call speedtest and return the results dictionary
    Input: N/A
    Output: Results dictionary
    '''
    logger.info('Calling Speedtest')
    try:
        test = speedtest.Speedtest()
    except Exception as e:
        logger.critical('Error with Speedtest: %s', e)
        return None
    else:
        logger.info('Speedtest Successful')
        test.get_best_server()
        test.download()
        test.upload()
        logger.debug('Returning from test_speed %s', test.results)
        return test.results.dict()


def write_to_file(path_name, given_string):
    '''Goal: Given a file name and string, creates a file with the string or appends the string to the file
    Input: file to write, string to write to file
    Output: Depending if file exists, this is create file and write string to file, otherwise will append string to file
    '''
    logger.info('Writing to file')
    if platform_os == 'win':
        print(path_name)
        folder_path, file_name = path_name.rsplit('\\', 1)
    else:
        folder_path, file_name = path_name.rsplit('/', 1)
    chdir(folder_path)
    if path.exists(file_name):
        logger.debug('File already exists in write_to_file: %s', file_name)
        with open(file_name, 'a') as appendable_file:
            appendable_file.write(given_string+'\n')
    else:
        logger.debug('File does not exist in write_to_file: %s', file_name)
        with open(file_name, 'w') as writable_file:
            # Headers are:
            # DATE
            # TIME
            # DOWNLOAD
            # UPLOAD
            # PING / LATENCY
            # IP
            # BYTES SENT
            # BYTES RECEIVED
            # ISP
            # SERVER LATITUDE
            # SERVER LONGITUDE
            # ISP LATITUDE
            # ISP LONGITUDE
            # PROCESS TIME (time to call speedtest)
            writable_file.write(
                'DATE,TIME,DOWNLOAD,UPLOAD,PING/LATENCY,IP,BYTES_SENT,BYTES_RECEIVED,ISP,SERVER_LAT,SERVER_LON,ISP_LAT,ISP_LON,PROCESS_TIME\n')
            writable_file.write(given_string+'\n')
    logger.info('Wrote to file')


def speed_to_string(internet_test, time_called):
    logger.info('Printing to string speed_to_string')
    result = ''
    result += time_called.strftime('%m-%d-%y')+','  # date
    result += time_called.strftime('%H:%M')+','  # time
    # converted from bits to mb | download speed
    result += str(internet_test['download'] / 1000000)+','
    # converted from bits to mb | upload speed
    result += str(internet_test['upload']/1000000)+','
    result += str(internet_test['ping'])+','  # ping
    result += str(internet_test['client']['ip'])+','  # ip
    result += str(internet_test['bytes_sent'])+','  # bytes sent
    result += str(internet_test['bytes_received'])+','  # bytes received
    result += internet_test['client']['isp']+','  # isp
    result += str(internet_test['server']['lat'])+','  # server lat
    result += str(internet_test['server']['lon'])+','  # server lon
    result += str(internet_test['client']['lat'])+','  # isp lat
    result += str(internet_test['client']['lon'])+','  # isp lon
    logger.debug('Returning from speed_to_string %s', result)
    return result


def main():
    logger.info('Started Script')
    time_called = dt.now()
    start_time = time.perf_counter()
    internet_test = test_speed()
    end_time = time.perf_counter()
    process_time = end_time - start_time
    if internet_test == None:
        logger.debug('Speedtest failed, canceling rest of script')
    else:
        logger.info('Test Complete')
        result_string = speed_to_string(internet_test, time_called)
        result_string += str(process_time)
        write_to_file(FILE_NAME, result_string)
        logger.info('Script Complete')
        logger.info('-'*50)


if __name__ == "__main__":
    main()
