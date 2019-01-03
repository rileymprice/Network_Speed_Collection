import speedtest
from datetime import datetime as dt
from path import Path
from os import path


def test_speed():
    '''Input: N/A
    Output: Results dictionary
    '''
    test = speedtest.Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    return test.results.dict()


def write_to_file(file_name, given_string):
    '''Input: file to write, string to write to file
    Output: Depending if file exists, this is create file and write string to file, otherwise will append string to file
    '''
    print('Printing to file')
    if path.exists(Path(f'./{file_name}')):
        print('Appending to file')
        with open(Path(f'./{file_name}'), 'a') as appendable_file:
            appendable_file.write(given_string+'\n')
    else:
        print('Creating File')
        with open(Path(f'./{file_name}'), 'w') as writable_file:
            writable_file.write(
                'DATE,TIME,DOWNLOAD,UPLOAD,PING/LATENCY,IP,BYTES_SENT,BYTES_RECEIVED,ISP,SERVER_LAT,SERVER_LON,ISP_LAT,ISP_LON,PROCESS_TIME\n')
            writable_file.write(given_string+'\n')
    print('Wrote to file')


def speed_to_string(internet_test, time_called):
    print('Printing to String')
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

    return result


def main():
    time_called = dt.now()
    print('Starting test')
    start_time = dt.now()
    internet_test = test_speed()
    end_time = dt.now()
    process_time = end_time - start_time
    print('Test complete')
    result_string = speed_to_string(internet_test, time_called)
    result_string += str(process_time)
    write_to_file('internet_speed.csv', result_string)


if __name__ == "__main__":
    main()
