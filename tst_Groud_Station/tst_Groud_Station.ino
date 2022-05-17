int cont=0, triguer;

void setup() {
  Serial.begin(9600);
}

void loop() {
  cont++;
  int randNumber1 = random(300);
  int randNumber2= random(300);
  int randNumber3= random(300);
  int randNumber5= random(300);
  int randNumber6= random(300);
  int randNumber7= random(300);
  int randNumber8= random(300);
  int randNumber9= random(300);
  int randNumber10= random(300);
  int randNumber11= random(300);
  int randNumber12= random(300);
  int randNumber13= random(300);
  int randNumber14= random(300);
  int randNumber15= random(300);
  int randNumber16= random(300);
  int randNumber17=random(300);
  int randNumber18= random(300);
  int randNumber19= random(300);
  
  triguer= 0;
  Serial.print(randNumber1);
  Serial.print(',');
  Serial.print(randNumber2);
  Serial.print(',');
  Serial.print(randNumber3);
  Serial.print(',');
  if ((cont % 4) == 0){
    Serial.print('t');
    triguer= 1;
  }
  else {
    Serial.print('c');
  }
  Serial.print(',');
  Serial.print(randNumber5);
  Serial.print(',');
  Serial.print(randNumber6);
  Serial.print(',');
  Serial.print(randNumber7);
  Serial.print(',');
  if (triguer != 0){
    Serial.print(randNumber8);
    Serial.print(',');
    Serial.print(randNumber9);
    Serial.print(',');
    Serial.print(randNumber10);
    Serial.print(',');
    Serial.print(randNumber11);
    Serial.print(',');
    Serial.print(randNumber12);
    Serial.print(',');
    Serial.print(randNumber13);
    Serial.print(',');
    Serial.print(randNumber14);
    Serial.print(',');
    Serial.print(randNumber15);
    Serial.print(',');
    Serial.print(randNumber16);
    Serial.print(',');
    Serial.print(randNumber17);
    Serial.print(',');
    Serial.print(randNumber18);
    Serial.print(',');
    Serial.print(randNumber19);
  }
    Serial.println();
  delay(250);

}
