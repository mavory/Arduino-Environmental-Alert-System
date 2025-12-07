#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <ThreeWire.h>
#include <RtcDS1302.h>
#include <DHT.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

ThreeWire myWire(3, 4, 2); // dat, clk, rst!!!!!!!!!
RtcDS1302<ThreeWire> rtc(myWire);

#define DHTPIN 5
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

#define greenLed 8
#define redLed 9
#define buzzer 6

unsigned long lastBeepTime = 0;
bool beepState = false;
float lastHum = -1;
float lastTemp = -1;
bool sensorError = false;
unsigned long lastBlink = 0;
bool blinkState = false;

void fadeInDisplay(const char* l1, const char* l2) {
  lcd.clear();
  for (int i = 0; i <= 16; i++) {
    lcd.setCursor(0, 0);
    lcd.print(String(l1).substring(0, i));
    lcd.setCursor(0, 1);
    lcd.print(String(l2).substring(0, i));
    delay(40);
  }
}

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.backlight();

  pinMode(greenLed, OUTPUT);
  pinMode(redLed, OUTPUT);
  pinMode(buzzer, OUTPUT);
  digitalWrite(buzzer, LOW);

  rtc.Begin();
  dht.begin();

  if (!rtc.GetIsRunning()) {
    rtc.SetDateTime(RtcDateTime(__DATE__, __TIME__));
  }

  fadeInDisplay("  System Start  ", "   Initializing ");
  delay(500);
  lcd.clear();
}

void loop() {
  float hum = dht.readHumidity();
  float temp = dht.readTemperature();
  RtcDateTime now = rtc.GetDateTime();

  char dateBuffer[17];
  snprintf(dateBuffer, sizeof(dateBuffer), "   %02u/%02u/%04u   ",
           now.Day(), now.Month(), now.Year());

  if (!isnan(hum) && !isnan(temp)) {
    if (sensorError) {
      lcd.clear();
      sensorError = false;
    }

    bool outOfRange = (hum < 30.0 || hum > 70.0);
    digitalWrite(greenLed, outOfRange ? LOW : HIGH);
    digitalWrite(redLed,   outOfRange ? HIGH : LOW);

    if (outOfRange) {
      if (millis() - lastBeepTime > 1000) {
        beepState = !beepState;
        digitalWrite(buzzer, beepState);
        lastBeepTime = millis();
      }
    } else {
      digitalWrite(buzzer, LOW);
    }

    if (abs(hum - lastHum) >= 0.1 || abs(temp - lastTemp) >= 0.1 || lastHum < 0) {
      char humBuf[6], tempBuf[6];
      dtostrf(hum, 4, 1, humBuf);
      dtostrf(temp, 4, 1, tempBuf);

      lcd.setCursor(0, 0);
      lcd.print(dateBuffer);

      lcd.setCursor(0, 1);
      lcd.print(" ");
      lcd.print(humBuf);
      lcd.print("% | ");
      lcd.print(tempBuf);
      lcd.print((char)223);
      lcd.print("C ");

      Serial.print("H:");
      Serial.print(humBuf);
      Serial.print(",T:");
      Serial.println(tempBuf);

      lastHum = hum;
      lastTemp = temp;
    }

  } 

  else {
    if (!sensorError) {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(" NO SENSOR DATA ");
      Serial.println("ERROR:SENSOR");
      sensorError = true;
    }

    if (millis() - lastBlink > 500) {
      blinkState = !blinkState;
      digitalWrite(greenLed, blinkState);
      digitalWrite(redLed, !blinkState);
      lastBlink = millis();
    }

    digitalWrite(buzzer, LOW);
  }

  delay(250);
}
