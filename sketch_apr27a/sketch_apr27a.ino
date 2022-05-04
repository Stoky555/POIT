float value = 10;

void setup()
{
  pinMode(3, OUTPUT);
  Serial.begin(9600);
}

void loop(){
  float napetie1, napetie2;
  
  napetie1=(float)analogRead(A0)*5/1023;
  napetie2=(float)analogRead(A1)*5/1023;
  
  delay(100);

  analogWrite(3, value);
  delay(100);
  
  Serial.println(float(napetie1-napetie2));

  if(Serial.read() != -1){
    value = Serial.read();
  }  
}
