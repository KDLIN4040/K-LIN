#include <NewPing.h>
 
#define TRIGGER_PIN  12
#define ECHO_PIN     11
#define MAX_DISTANCE 200
double distance;
double count;
double   sum;
double   averge;
int readserial;
bool boolen = false;
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);
 
void setup() {
  Serial.begin(9600);
}
 
void loop()
{ 
  count = 0;
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
          if (distance > 0)
          {
          count += 1;
          sum += distance ;
          delay(25);
          }
        }
    averge = sum/count ;
    Serial.println("count");
    Serial.println(count);
    Serial.println("averge");
    Serial.println(averge);  
    }
  } 
}
