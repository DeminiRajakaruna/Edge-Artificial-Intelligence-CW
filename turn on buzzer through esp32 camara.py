
#define BUZZER_PIN 12  // Connect buzzer to GPIO 12

void setup() {
  Serial.begin(115200);
  
  // Set buzzer pin as output
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  // Turn on buzzer
  digitalWrite(BUZZER_PIN, HIGH);
  Serial.println("🔊 Buzzer ON");
  delay(2000); // Buzzer on for 2 seconds

  // Turn off buzzer
  digitalWrite(BUZZER_PIN, LOW);
  Serial.println("🔕 Buzzer OFF");
  delay(5000); // Wait 5 seconds before repeating
}
