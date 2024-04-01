const int microphonePin = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int mn = 1024;
  int mx = 0;

  for (int i = 0; i < 1000; ++i) {

    int val = analogRead(microphonePin);
    
    mn = min(mn, val);
    mx = max(mx, val);
  }

  int delta = mx - mn;

  //Serial.print("Min=");
  //Serial.print(mn);
  //Serial.print(" Max=");
  //Serial.print(mx);
  //Serial.print(" Delta=");
  Serial.println(delta);
}