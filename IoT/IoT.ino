#include <ESP8266WiFi.h>
#include <ESPAsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <RTClib.h>
#include <DNSServer.h>
#include <ESP8266mDNS.h>
#include <ArduinoJson.h>

RTC_Millis RTC;

String ssid     = "Proiect";
String password = "testing1";
const char* p_pcHostname = "proiect";

AsyncWebServer server(80);

// Captive Portal for DHCP
const byte DNS_PORT = 53;
DNSServer dnsServer;

const int maxValues = 10;
String times[maxValues];
float temperatures[maxValues];
float humidities[maxValues];
int currentIndex = 0;

// Loop delay for WebClient and DNS Update
const long interval = 5000;  

float speed;
float temperature;
float vibration;
float noise;
float load;
bool defect;

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
  WiFi.mode(WIFI_AP);
  WiFi.softAPConfig(IPAddress(127, 0, 0, 1), IPAddress(127, 0, 0, 1), IPAddress(255, 255, 255, 0));

  // 4th param is to hide AP
  if(WiFi.softAP(ssid, password, 1, 0) == true)
  {
    Serial.print("Access Point is Created with SSID: ");
    Serial.println(ssid);
    Serial.print("Access Point IP: ");
    Serial.println(WiFi.softAPIP().toString());
  }
  else
    Serial.println("Unable to Create Access Point");

  if (!MDNS.begin(p_pcHostname)) 
    Serial.println("Error setting up MDNS responder!");

  dnsServer.start(DNS_PORT, "*", WiFi.softAPIP());

  server.on("/data", HTTP_GET, [](AsyncWebServerRequest *request)
  {
    String rows = "sensor_data : {";
    for (int i = 0; i < maxValues; i++) 
    {
      if (temperatures[i] != 0.0 || humidities[i] != 0.0) 
      {
        rows += String("<br>&nbsp;&nbsp;\"sensor_1\": {<br>&nbsp;&nbsp;&nbsp;&nbsp;\"temperature\": " + String(temperatures[i]) + 
          ",<br>&nbsp;&nbsp;&nbsp;&nbsp;\"humidity\": " + String(humidities[i]) + ",<br>&nbsp;&nbsp;&nbsp;&nbsp;\"timestamp\": \"" + 
          times[i] + "\"<br>&nbsp;&nbsp;}");
      }
    }

    rows += "<br>}";
    request->send_P(200, "text/html", rows.c_str());
  });

  server.begin();

  MDNS.addService("http", "tcp", 80);
}

void loop()
{  
  MDNS.update();

  dnsServer.processNextRequest();
  delay(interval);

  generateData();
  String jsonData = createJSON();

  // Trimitere JSON prin Serial
  Serial.println(jsonData);
}

String getTime() 
{
  DateTime now = RTC.now();

  String timeString = String(now.day()) + "/" + String(now.month()) + "/" + String(now.year()) + " " + 
    String(now.hour()) + ":" + String(now.minute()) + ":" + String(now.second());

  return timeString;
}
