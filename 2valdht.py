import serial
import time
import datetime
import sqlite3
#import keyboard

# Настройка последовательного порта
SERIAL_PORT = '/dev/ttyACM0'  # Проверьте правильный порт через dmesg или ls /dev/tty*
BAUD_RATE = 9600
DB_NAME = 'sensor_data.db'

def setup_database():
    try:
        # Создаем подключение к базе данных
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Создаем таблицу, если она не существует
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                temperature REAL,
                humidity REAL
            )
        ''')
        conn.commit()
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Ошибка при создании базы данных: {e}")
        return None, None

def setup_serial():
    try:
        # Открываем последовательный порт
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Время на инициализацию
        return ser
    except serial.SerialException as e:
        print(f"Ошибка при открытии порта: {e}")
        return None

def read_sensor_data(ser):
    try:
        # Читаем данные с Arduino
        line = ser.readline().decode('utf-8').strip()
        # Парсим данные
        if line:
            try:
                temperature, humidity = map(float, line.split(','))
                return temperature, humidity
            except ValueError:
                print("Ошибка при парсинге данных")
                return None, None
    except Exception as e:
        print(f"Ошибка при чтении данных: {e}")
        return None, None
    
def save_to_db(conn, cursor, temperature, humidity):
    try:
        cursor.execute('''
            INSERT INTO sensor_data (timestamp, temperature, humidity)
            VALUES (CURRENT_TIMESTAMP, ?, ?)
        ''', (temperature, humidity))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при записи в базу данных: {e}")


def main():
    ser = setup_serial()
    if not ser:
        return
    
    conn, cursor = setup_database()
    if not conn or not cursor:
        return
    
    try:
        while True:
            temp, hum = read_sensor_data(ser)
            if temp is not None and hum is not None:
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{current_time}] Температура: {temp:.2f}°C, Влажность: {hum:.2f}%")
                save_to_db(conn, cursor, temp, hum)

            time.sleep(3)  # Интервал опроса датчика
            
            #if keyboard.is_pressed('q'):  # Остановка по нажатию 'q'
            #    break
            
    except KeyboardInterrupt:
        print("Работа завершена пользователем")
    finally:
        ser.close()
        print("Последовательный порт закрыт")
        if conn:
            conn.close()
            print("База данных закрыта")

if __name__ == "__main__":
    main()
