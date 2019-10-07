int sensorPin = 0; //analog pin 0 感測器外側訊號腳接Arduino 類比腳位 ANALOG IN #0
unsigned int   sum;
unsigned int   averge;
int readserial;
bool boolen = false;
void setup()
{
Serial.begin(9600);
}

void loop()
{ 
  sum = 0;
  if(Serial.available()>0)
  {
  boolen = true;
  readserial = Serial.read();
  if (boolen == true)
  { 
    boolen = false;
      for (int i =0 ; i<100 ; i++)
      { 
      int val = analogRead(sensorPin);
      Serial.println(val);
      sum += val ;
      delay(100);
      }
    averge = sum/100 ;
    Serial.println("averge");
    Serial.println(averge);  
    }
  } 
}
