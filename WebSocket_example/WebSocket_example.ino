
int led=13;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(led,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  Serial.println("receiving from arduino");
  delay(200);
  while(Serial.available()>0){
    //digitalWrite(led,HIGH);
    char incoming=Serial.read();
    Serial.println(incoming);
    if(incoming=='1'){
    digitalWrite(led,HIGH);
    }

    if(incoming=='0'){
    digitalWrite(led,LOW);
    }
  }

}
