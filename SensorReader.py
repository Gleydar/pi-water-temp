import json
import os
import glob
import time


class SensorReader:
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    sensor_config = None
    sensor_data = {'sensors': []}

    def read_temps_raw(self):
        list = []
        i = 0
        while i < len(self.sensor_config['sensors']):
            list.append(self.read_single_temp_raw(i))
        return list

    def read_single_temp_raw(self, i: int):
        sensor = self.sensor_config['sensors'][i]
        folder = glob.glob(self.sensor_config['base_dir'] + sensor['address_glob'])[0]
        f = open(folder + self.sensor_config['device_file'], 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        data = self.read_temps_raw()
        i: int = 0
        for lines in data:
            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = self.read_single_temp_raw(i)
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos + 2:]
                temp_c = float(temp_string) / 1000.0
                temp_c = round(temp_c, ndigits=2)
                self.sensor_data['sensors'].append(
                    {'name': self.sensor_config['sensors'][i]['name'], 'temperature': temp_c})
            i = i + 1

    def loop(self):
        self.read_temp()
        time.sleep(60)

    def __init__(self):
        with open('static/sensorConfig.conf.json') as f:
            self.sensor_config = json.load(f)
