void setup()
{
  pinMode(3, OUTPUT);
  Serial.begin(9600);
}

void loop(){
  float napetie1, napetie2;
  
  napetie1=analogRead(AO);
  napetie2=analogRead(A1);
  
  delay(10);

  analogWrite(3, 10);
  delay(10);

  Serial.println(napetie1-napetie2);  
}
