#include "FlashSTM32.h"

const char *ssid = "Nhennn";
const char *pass = "trungnhan0203";

HardwareSerial FlashPort(2);
FlashSTM32 devKit(5, 18);
unsigned long previousTime = 0;
URL url;

void fetchJSON(URL url)
{
    HTTPClient http;
    http.begin(url.url + String(getDataPath));
    int httpCode = http.GET();
    if (httpCode > 0)
    {
        Serial.printf("HTTP GET code: %d\n", httpCode);

        if (httpCode == HTTP_CODE_OK)
        {
            String payload = http.getString();
            StaticJsonDocument<50> doc;
            DeserializationError err = deserializeJson(doc, payload);

            if (!err)
            {
                String value = doc["value"];
                url.fileID = value;
                Serial.println(value);
            }
            else
            {
                Serial.println("Error to parsing json.");
            }

            if (url.fileID != String("null"))
            {
                unsigned long startMillis = millis();
                updateValueToNull(url);
                Serial.println("update Null Done");
                if (devKit.DownloadFirmware(url))
                {
                    Serial.println("Download hex file successfully!!!");
                    File firmwareFile = SPIFFS.open(("/" + url.fileName).c_str(), "r");
                    if (!firmwareFile)
                    {
                        Serial.println("Failed to open firmware file");
                        return;
                    }

                    size_t fileSize = firmwareFile.size();
                    Serial.print("Firmware file size: ");
                    Serial.println(fileSize);

                    if (!devKit.enterBootMode(FlashPort))
                    {
                        Serial.println("Failed to enter bootloader mode.");
                        return;
                    }

                    devKit.Flash(firmwareFile, FlashPort);
                    delay(5);
                    devKit.exitBootMode();
                    unsigned long endMillis = millis();
                    Serial.println("Firmware upload complete");
                    Serial.print("Finish at: ");
                    Serial.println(endMillis - startMillis);
                }
            }
        }
    }
    else
    {
        Serial.printf("HTTP GET failed, error: %s\n", http.errorToString(httpCode).c_str());
    }
    http.end();
}

void setup()
{
    Serial.begin(115200);
    FlashPort.begin(115200, SERIAL_8E1, 16, 17);
    delay(500);

    devKit.setup();
    WiFi.begin(ssid, pass);
    Serial.write("Connecting to wifi ");
    Serial.write(ssid);
    Serial.write(":");
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.write(".");
        delay(100);
    }
    Serial.println();
    Serial.print("Connected to wifi ");
    Serial.write(ssid);
    Serial.println();

    if (!SPIFFS.begin(true))
    {
        Serial.println("Failed to mount file system");
        return;
    }
    else
    {
        Serial.println("Successful to mount file system");
    }
}
void loop()
{
    if (WiFi.status() == WL_CONNECTED)
    {
        unsigned long currentTime = millis();

        if (currentTime - previousTime >= 500)
        {
            previousTime = currentTime;
            fetchJSON(url);
        }
    }
}