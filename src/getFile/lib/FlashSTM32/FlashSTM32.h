#include <HardwareSerial.h>
#include "SPIFFS.h"
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#define DATA_BUFFER 256

#define ACK_MESSAGE 0x79
#define NAK_MESSAGE 0x1F

#define EraseCMD 0x43
#define Erase_extend_CMD 0xFF
#define ReadCMD 0x11
#define WriteCMD 0x31

#define NormalRecord 0x00
#define EndRecord 0x01
#define BaseAddress 0x08000000

#define downloadPath "download/"
#define setNullPath "set-data/"
#define getDataPath "get-data/"


struct IntelHexFile
{
    uint8_t byteCount;
    uint16_t address;
    uint8_t recordType;
    uint8_t data[16];
    uint8_t checksum;
};

struct URL{
    String url = "http://192.168.137.1:8000/";
    String fileID; 
    String fileName;  
}; 

class FlashSTM32
{
private:
    uint8_t port;
    int NRST_PIN;
    int BOOT0_PIN;
public:
    FlashSTM32(int rst_pin, int boot0_pin);
    void setup();
    void sendCMD(uint8_t cmd, HardwareSerial &flashPort);
    bool DownloadFirmware(URL &url);
    bool enterBootMode(HardwareSerial &flashPort);
    void exitBootMode();
    void Flash(File &firmwareFile, HardwareSerial &flashPort);
    void Erase(HardwareSerial &flashPort);
    ~FlashSTM32();
private:
    void parseHexFile(File &firmwareFile, HardwareSerial &flashPort);
    void parseHexLine(String line, IntelHexFile &intelHex);
    void sendAddress(uint16_t address, HardwareSerial &flashPort);
    void sendData(IntelHexFile &intelHex, HardwareSerial &flashPort);
    void generateFileName(URL url); 
};

void updateValueToNull(URL url); 
// void fetchJSON(URL url); 
