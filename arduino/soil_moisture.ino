#include <WiFi.h>
#include <WiFiUdp.h>

#include "arduino_secrets.h"

// Stored in Secrets File
char ssid[] = SSID;
char pass[] = PASSWD;
int udp_port = 13900;
char hostname[] = HOSTNAME;

WiFiUDP udp;
WiFiServer server(13900);

void setup()
{
    // put your setup code here, to run once:
    Serial.begin(9600);
    WiFi.begin(ssid, pass);
    Serial.println("Wifi Connected");

    // Set up Soil Mositure Readings
    pinMode(A0, INPUT);

    // Set up UDP Server
    udp.begin(udp_port);
    Serial.println("UDP initialized");
    server.begin();
    Serial.println("Server started");
}

void loop()
{
    // put your main code here, to run repeatedly:
    Serial.print("Reading from Sensor:");
    int moisture = analogRead(A0);
    Serial.println(moisture);

    // Send UDP Packet
    udp.beginPacket(hostname, udp_port);
    udp.print(moisture);
    udp.endPacket();
    delay(5000);
}