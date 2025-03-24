         /////////////////////////////////////////////  
        // Stardew Valley Villager Recognition and //
       //      Gift Preferences Bot w/ OpenCV     //
      //             ---------------             //
     //         (LattePanda Alpha 864s)         //           
    //             by Kutluhan Aktar           // 
   //                                         //
  /////////////////////////////////////////////

//
// Via OpenCV, recognize villagers to display their birthdays, loves, likes, and hates while playing Stardew Valley on LattePanda Alpha.
//
// For more information:
// https://www.theamplituhedron.com/projects/Stardew_Valley_Villager_Recognition_and_Gift_Preferences_Bot_w_OpenCV
//
//
// Connections
// LattePanda Alpha 864s (Arduino Leonardo) :  
//                                3.5'' 320x480 TFT LCD Touch Screen (ILI9488)
// D10 --------------------------- CS 
// D8  --------------------------- RESET 
// D9  --------------------------- D/C
// MOSI -------------------------- SDI 
// SCK --------------------------- SCK 
// MISO -------------------------- SDO(MISO) 
//                                Buzzer
// D11 --------------------------- S     
//                                5mm Green LED
// D12 --------------------------- S


// Include the required libraries:
#include "SPI.h"
#include <Adafruit_GFX.h>
#include <ILI9488.h>

// Define the required pins for the 320x480 TFT LCD Touch Screen (ILI9488)
#define TFT_DC 9
#define TFT_CS 10
#define TFT_RST 8

// Use hardware SPI (on Leonardo, SCK, MISO, MOSI) and the above for DC/CS/RST
ILI9488 tft = ILI9488(TFT_CS, TFT_DC, TFT_RST);

// Define the buzzer pin:
#define buzzer 11
// Define the green LED pin:
#define green_LED 12

// Define the data holders:
String gameData = "";

void setup() {
  pinMode(green_LED, OUTPUT);
  // Initialize the serial communication:
  Serial.begin(9600);
  // Initialize the TFT LCD Touch Screen (ILI9488):
  tft.begin();
  tft.setRotation(1);
  tft.fillScreen(ILI9488_RED);
  tft.setCursor(0, 0);
  tft.setTextColor(ILI9488_BLACK); tft.setTextSize(4);
  tft.println("\nStardew Valley\n");
  tft.println("Villager Recognition\n");
  tft.println("and Gift Preferences\n");
  tft.println("Bot w/ OpenCV\n");

}

void loop() {
  // Via the serial communication, elicit the detected character's information:
  while (Serial.available()) {
    char c = (char)Serial.read();
    gameData += c;
  }
  // Display the transferred character information:
  if(gameData != ""){
    // Notify the user:
    tft.fillScreen(ILI9488_BLACK);
    tft.setCursor(10, 5);
    tft.setTextColor(ILI9488_RED); tft.setTextSize(4);
    tft.println("Stardew Valley\n");
    tft.setTextColor(ILI9488_GREEN); tft.setTextSize(2);
    tft.println(gameData);
    tone(buzzer, 500);
    digitalWrite(green_LED, HIGH);
    delay(500);
    noTone(buzzer);
    digitalWrite(green_LED, LOW);
  }
  // Clear:
  delay(250);
  gameData = "";
}
