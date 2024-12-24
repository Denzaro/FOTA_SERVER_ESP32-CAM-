#include "FlashSTM32.h"

void FlashSTM32::generateFileName(URL url){
    url.fileName = "downloaded_file" + url.fileID + ".hex"; 
}

void FlashSTM32::sendAddress(uint16_t address, HardwareSerial &flashPort)
{
    Serial.println("attempting to send address. ");
    uint32_t addr = (uint32_t)(0x08000000) | (uint32_t)address;
    uint8_t add[5];
    add[0] = (uint8_t)((addr >> 24) & 0xff);
    add[1] = (uint8_t)((addr >> 16) & 0xff);
    add[2] = (uint8_t)((addr >> 8) & 0xff);
    add[3] = (uint8_t)(addr & 0xff);
    add[4] = (uint8_t)(add[0] ^ add[1] ^ add[2] ^ add[3]);

    flashPort.write(add[0]);
    flashPort.write(add[1]);
    flashPort.write(add[2]);
    flashPort.write(add[3]);
    flashPort.write(add[4]);
}

void FlashSTM32::sendData(IntelHexFile &intelHex, HardwareSerial &flashPort)
{
    flashPort.write((uint8_t)(intelHex.byteCount - 1));
    delay(5);
    flashPort.write(intelHex.data, 16);
    delay(5);
    uint8_t checksum = (uint8_t)(intelHex.byteCount - 1);
    for (int i = 0; i < 16; i++)
    {
        checksum ^= intelHex.data[i];
    }
    flashPort.write(checksum);
    Serial.print("checksum is: ");
    Serial.println(checksum, HEX);
    uint8_t byte = flashPort.read();
    Serial.print("Received byte: 0x");
    Serial.println(byte, HEX);
    if (byte == ACK_MESSAGE)
    {
        Serial.println("Write data to address successfully.");
    }
}

void FlashSTM32::parseHexLine(String line, IntelHexFile &intelHex)
{
    line.trim();

    if (line.length() < 11 || line[0] != ':')
    {
        Serial.println("Invalid HEX line!");
        return;
    }

    intelHex.byteCount = (uint8_t)strtol(line.substring(1, 3).c_str(), NULL, 16);
    intelHex.address = (uint16_t)strtol(line.substring(3, 7).c_str(), NULL, 16);
    intelHex.recordType = (uint8_t)strtol(line.substring(7, 9).c_str(), NULL, 16);
    for (int i = 9, index = 0; i < 9 + intelHex.byteCount * 2; i += 2, index++)
    {
        intelHex.data[index] = (uint8_t)strtol(line.substring(i, i + 2).c_str(), NULL, 16);
    }
    intelHex.checksum = (uint8_t)strtol(line.substring(9 + intelHex.byteCount * 2, 9 + intelHex.byteCount * 2 + 2).c_str(), NULL, 16);
}

void FlashSTM32::parseHexFile(File &firmwareFile, HardwareSerial &flashPort)
{
    String line = "";
    IntelHexFile intelHex;
    while (firmwareFile.available())
    {
        char c = firmwareFile.read();
        if (c == '\n' || c == '\r')
        {
            if (line.length() > 0)
            {
                this->parseHexLine(line, intelHex);
                this->sendCMD(WriteCMD, flashPort);
                this->sendAddress(intelHex.address, flashPort);
                this->sendData(intelHex, flashPort);
                line = "";
            }
        }
        else
        {
            line += c;
        }
    }
}

void FlashSTM32::sendCMD(uint8_t cmd, HardwareSerial &flashPort)
{
    flashPort.write(cmd);
    flashPort.write(~cmd);
}

FlashSTM32::FlashSTM32(int rst_pin, int boot0_pin)
{
    this->BOOT0_PIN = boot0_pin;
    this->NRST_PIN = rst_pin;
}

void FlashSTM32::setup()
{
    pinMode(BOOT0_PIN, OUTPUT);
    pinMode(NRST_PIN, OUTPUT);
}

bool FlashSTM32::DownloadFirmware(URL &url)
{
    HTTPClient http;Serial.println(url.fileID);

    http.begin(url.url + String(downloadPath) + url.fileID + "/");
    int httpCode = http.GET();
    this->generateFileName(url);
    if (httpCode == HTTP_CODE_OK)
    {
        File file = SPIFFS.open(("/" + url.fileName).c_str(), "w");
        if (!file)
        {
            Serial.println("Failed to open file for writing");
            return false;
        }
        String payload = http.getString();
        file.print(payload);
        file.close();
        Serial.println("Firmware downloaded and saved to SPIFFS");
        return true;
    }
    else
    {
        Serial.printf("Failed to download firmware, error: %d\n", httpCode);
        return false;
    }
}

bool FlashSTM32::enterBootMode(HardwareSerial &flashPort)
{

    digitalWrite(this->BOOT0_PIN, 1);
    delay(50);
    digitalWrite(this->NRST_PIN, 0);
    delay(50);
    digitalWrite(this->NRST_PIN, 1);

    delay(50);

    flashPort.write((uint8_t)0x7F);

    delay(50);
    Serial.println("Attempting to enter bootloader mode...");
    uint8_t byte = flashPort.read();
    Serial.print("Received byte: 0x");
    Serial.println(byte, HEX);
    if (byte == ACK_MESSAGE)
    {
        Serial.println("ACK received, flashPort is in bootloader mode.");
        return true;
    }

    Serial.println("No response from flashPort.");
    return false;
}

void FlashSTM32::exitBootMode()
{
    Serial.println("Exiting bootloader mode...");
    digitalWrite(this->BOOT0_PIN, 0);
    delay(50);
    digitalWrite(this->NRST_PIN, 0);
    delay(50);
    digitalWrite(this->NRST_PIN, 1);
    delay(50);
    Serial.println("Exit bootloader mode done");
}

void FlashSTM32::Erase(HardwareSerial &flashPort)
{
    Serial.println("Attempting to Erase code...");
    this->sendCMD(EraseCMD, flashPort);
    uint8_t byte = flashPort.read();
    Serial.print("Received byte: 0x");
    Serial.println(byte, HEX);
    Serial.println("ACK received, continue to erase code.");
    this->sendCMD(Erase_extend_CMD, flashPort);
    Serial.println("ACK received, Erase command accepted.");
}

void FlashSTM32::Flash(File &firmwareFile, HardwareSerial &flashPort)
{

    this->Erase(flashPort);
    if (!this->enterBootMode(flashPort))
    {
        Serial.println("Failed to entering the bootloader.");
    }
    this->parseHexFile(firmwareFile, flashPort);
}

FlashSTM32::~FlashSTM32()
{
}


void updateValueToNull(URL url) {
    HTTPClient http;

    http.begin(url.url + String(setNullPath));
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<50> doc;
    doc["value"] = nullptr;
    String jsonPayload;
    serializeJson(doc, jsonPayload);

    int httpCode = http.POST(jsonPayload);

    if (httpCode > 0) {
      Serial.printf("HTTP POST code: %d\n", httpCode);

      if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_CREATED) {
        String response = http.getString();
        Serial.println("Response from server:");
        Serial.println(response);
      }
    } else {
      Serial.printf("HTTP POST failed, error: %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
}

