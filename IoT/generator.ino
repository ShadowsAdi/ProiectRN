#include <ArduinoJson.h>
#include <ESP8266WiFi.h>

const char* ssid = "Retea";
const char* password = "1234";

float speed;
float temperature;
float vibration;
float noise;
float load;
bool defect;

AsyncWebServer server(80);

void generateData() {
  speed = random(100, 200) / 100.0;
  temperature = random(600, 700) / 10.0;
  vibration = random(10, 30) / 1000.0;
  noise = random(50, 70);
  load = random(50, 100);
  defect = random(0, 20) == 0;
}

String createJSON() {
  StaticJsonDocument<256> doc;

  doc["Speed (m/s)"] = speed;
  doc["Temperature (°C)"] = temperature;
  doc["Vibration (mm/s)"] = vibration;
  doc["Noise (dB)"] = noise;
  doc["Load (%)"] = load;
  doc["Defect"] = defect;

  String json;
  serializeJson(doc, json);
  return json;
}

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("WiFi connected!");
}

void loop() {
  generateData();
  String jsonData = createJSON();

  Serial.println(jsonData);

  delay(1000);
}
