int sensorPin = 0; //analog pin 0 感測器外側訊號腳接Arduino 類比腳位 ANALOG IN #0

void setup()
{
Serial.begin(9600);
}

void loop()
{
int val = analogRead(sensorPin);
Serial.println(val);

delay(100);

}
