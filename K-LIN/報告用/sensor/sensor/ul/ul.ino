#include <NewPing.h>
 
#define TRIGGER_PIN  12
#define ECHO_PIN     11
#define MAX_DISTANCE 200
unsigned int distance;
unsigned int   sum;
unsigned int   averge;
int readserial;
bool boolen = false;
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);
 
void setup() {
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
       for (int i =0 ; i<200 ; i++)
        { 
        int val = sonar.ping();
        distance = val/US_ROUNDTRIP_CM;
        Serial.println(distance);
        sum += distance ;
        delay(100);
        }
    averge = sum/100 ;
    Serial.println("averge");
    Serial.println(averge);  
    }
  } 
}
