void setup()
{
  Serial.begin(9600);
  pinMode(2,INPUT);
  pinMode(4,INPUT);
  pinMode(7,INPUT);
  pinMode(8,INPUT);
}

void loop(){
  Serial.print(analogRead(A0));
  Serial.print(",");
  Serial.print(analogRead(A1));
  Serial.print(",");
  Serial.print(digitalRead(2));
  Serial.print(",");
  Serial.print(digitalRead(4));
  Serial.print(",");
  Serial.print(digitalRead(7));
  Serial.print(",");
  Serial.print(digitalRead(8));
delay(10);
}