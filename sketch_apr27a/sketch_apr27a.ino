float value = 10;

void setup()
{
  pinMode(3, OUTPUT);
  Serial.begin(9600);
}

void loop(){
  float napetie1, napetie2;
  
  napetie1=analogRead(A0);
  napetie2=analogRead(A1);
  
  delay(100);

  analogWrite(3, value);
  delay(100);
  
  Serial.println(float(napetie1-napetie2));

  if(Serial.read() != -1){
    value = Serial.read();
  }  
}
