from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
from domain.parking import Parking


class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename
        self.accelerometer_file = None
        self.gps_file = None
        self.parking_file = None
        self.accelerometer_reader = None
        self.gps_reader = None
        self.parking_reader = None

    def read(self) -> AggregatedData:
        if not self.accelerometer_file or not self.gps_file:
            raise ValueError("Files not open. Call startReading() first.")

        accelerometer_row = next(self.accelerometer_reader, None)
        gps_row = next(self.gps_reader, None)
        parking_row = next(self.parking_reader, None)

        # Перевіряємо, чи опрацьовано всі дані
        if accelerometer_row is None or gps_row is None or parking_row is None:
            raise ValueError("All data has been processed")

        # Пропускаємо рядок, що є заголовком
        while accelerometer_row[0][0].isalpha():
            accelerometer_row = next(self.accelerometer_reader, None)

        # Перевіряємо, якщо більше нема даних окрім заголовку
        if accelerometer_row is None:
            raise ValueError("Accelerometer data has been processed")

        # Пропускаємо рядок, що є заголовком
        if gps_row[0][0].isalpha():
            gps_row = next(self.gps_reader, None)

        # Перевіряємо, якщо більше нема даних окрім заголовку
        if gps_row is None:
            raise ValueError("GPS data has been processed")

        # Пропускаємо рядок, що є заголовком
        if parking_row[0][0].isalpha():
            parking_row = next(self.parking_reader, None)

        # Перевіряємо, якщо більше нема даних окрім заголовку
        if parking_row is None:
            raise ValueError("Parking data has been processed")

        #accelerometer_data = []
        ## Skip the header row
        #self.accelerometer_file.seek(0)
        #next(self.accelerometer_file)
        #for row in self.accelerometer_reader:
        #    if row:
        #        values = row[0].split(',')
        #        if len(values) >= 3:
        #            x, y, z = map(int, values[:3])
        #            accelerometer_data.append(Accelerometer(x, y, z))
#
        #gps_data = []
        #self.gps_file.seek(0)
        #next(self.gps_file)
        #for row in self.gps_reader:
        #    if row:
        #        values = row[0].split(',')
        #        if len(values) >= 2:
        #            # Assuming the GPS data is formatted as "longitude,latitude"
        #            longitude, latitude = map(float, values[:2])
        #            gps_data.append(Gps(longitude, latitude))
#
        #parking_data = []
        #self.parking_file.seek(0)
        #next(self.parking_file)
        #for row in self.parking_reader:
        #    if row:
        #        values = row[0].split(',')
        #        if len(values) >= 3:
        #            # Assuming the GPS data is formatted as "longitude,latitude"
        #            empty_count = int(values[0])
        #            longitude, latitude = map(float, values[1:3])
        #            gps = Gps(longitude, latitude)
        #            parking_data.append(Parking(empty_count, gps))
#
        time_data = datetime.now()

        accelerometer_data = Accelerometer(x=int(accelerometer_row[0]), y=int(accelerometer_row[1]), z=int(accelerometer_row[2]))
        gps_data = Gps(longitude=float(gps_row[0]), latitude=float(gps_row[1]))
        parking_data = Parking(empty_count=int(parking_row[0]), gps=Gps(float(parking_row[1]), float(parking_row[2])))

        return AggregatedData(accelerometer=accelerometer_data, gps=gps_data, parking=parking_data, time=time_data)

    def startReading(self):
        """Відкриття файлів для читання"""
        self.accelerometer_file = open(self.accelerometer_filename, 'r')
        self.gps_file = open(self.gps_filename, 'r')
        self.parking_file = open(self.parking_filename, 'r')

        self.accelerometer_reader = reader(self.accelerometer_file)
        self.gps_reader = reader(self.gps_file)
        self.parking_reader = reader(self.parking_file)

        # Перемістити курсор файлу на початок
        self.accelerometer_file.seek(0)
        self.gps_file.seek(0)
        self.parking_file.seek(0)

    def stopReading(self):
        """Закриття файлів"""
        if self.accelerometer_file:
            self.accelerometer_file.close()
        if self.gps_file:
            self.gps_file.close()
        if self.parking_file:
            self.parking_file.close()
