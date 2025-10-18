// библиотека для работы с датчиками серии DHT
#include <TroykaDHT.h>

// создаём объект класса DHT
// передаём номер пина к которому подключён датчик и тип датчика
// типы сенсоров: DHT11, DHT21, DHT22
DHT dht(4, DHT11);
bool firstRead = true; // Флаг для пропуска первого чтения

float sensorData[2]; // Массив для двух float значенийrf
 
void setup()
{
  // открываем последовательный порт для мониторинга действий в программе
  Serial.begin(9600);
  dht.begin();
}
 
void loop()
{
  // считывание данных с датчика
  dht.read();
  // проверяем состояние данных

  
  switch(dht.getState()) {
    // всё OK
    case DHT_OK:
      // выводим показания влажности и температуры

      // Пропускаем первое чтение
  if (firstRead) {
    firstRead = false;
    delay(2000); // Ждем следующего цикла
    return;
  }
  
      float humidity = dht.getHumidity();
  float temperature = dht.getTemperatureC();
  
  // Сохраняем в массив
  sensorData[0] = temperature;
  sensorData[1] = humidity;
  
  // Проверяем корректность
  if (!isnan(sensorData[0]) && !isnan(sensorData[1])) {
    Serial.print(sensorData[0]);
    Serial.print(",");
    Serial.println(sensorData[1]);
  }     
     
     //float temperature = dht.getTemperatureC();
     
      //Serial.print(temperature);
      //Serial.print(dht.getTemperatureC());
      //Serial.print(",");
      //float humidity = dht.getHumidity();
      //Serial.println(humidity);

      
      //Serial.print("Temperature = ");
      //Serial.print(dht.getTemperatureC());
      //Serial.println(" C \t");
      //Serial.print("Temperature = ");
      //Serial.print(dht.getTemperatureK());
      //Serial.println(" K \t");
      //Serial.print("Temperature = ");
      //Serial.print(dht.getTemperatureF());
      //Serial.println(" F \t");
      //Serial.print("Humidity = ");
      //Serial.print(dht.getHumidity());
      //Serial.println(" %");
      break;
    // ошибка контрольной суммы
    case DHT_ERROR_CHECKSUM:
      Serial.println("Checksum error");
      break;
    // превышение времени ожидания
    case DHT_ERROR_TIMEOUT:
      Serial.println("Time out error");
      break;
    // данных нет, датчик не реагирует или отсутствует
    case DHT_ERROR_NO_REPLY:
      Serial.println("Sensor not connected");
      break;
  }
 
  // ждём две секунды
  delay(3000);
}
