/**
 * Demonstrate using DataReceiver to read color data from Serial, and using
 * ColorPiper to transfer (pipe) that color data to the LED strip.
 *
 * See the .py file in this directory, which generates and sends colors.
 */


#include <newanddelete.h> // For Arduino before 1.0, new and delete operators.
#include <DataReceiver.h>
#include <ledcontroller.h>

#define PIN_LED_DATA	5	// red wire
#define PIN_LED_CLOCK	4	// green wire
#define PIN_LED1_DATA 7
#define PIN_LED1_CLOCK 6
#define PIN_LED2_DATA	9	// red wire
#define PIN_LED2_CLOCK	8	// green wire
#define PIN_LED3_DATA 11
#define PIN_LED3_CLOCK 10
#define PIN_LED4_DATA 13
#define PIN_LED4_CLOCK 12

DataReceiver<5> dataReceiver;
LedController::LedPiper ledPiper(PIN_LED_DATA, PIN_LED_CLOCK);
LedController::LedPiper ledPiper1(PIN_LED1_DATA, PIN_LED1_CLOCK);
LedController::LedPiper ledPiper2(PIN_LED2_DATA, PIN_LED2_CLOCK);
LedController::LedPiper ledPiper3(PIN_LED3_DATA, PIN_LED3_CLOCK);
LedController::LedPiper ledPiper4(PIN_LED4_DATA, PIN_LED4_CLOCK);

void setColorsAndSend(size_t size, const char* colorBytes) {
	ledPiper.setColorsAndSend(size, colorBytes);
}

void setColorsAndSend1(size_t size, const char* colorBytes) {
	ledPiper1.setColorsAndSend(size, colorBytes);
}

void setColorsAndSend2(size_t size, const char* colorBytes) {
	ledPiper2.setColorsAndSend(size, colorBytes);
}

void setColorsAndSend3(size_t size, const char* colorBytes) {
	ledPiper3.setColorsAndSend(size, colorBytes);
}

void setColorsAndSend4(size_t size, const char* colorBytes) {
	ledPiper4.setColorsAndSend(size, colorBytes);
}

void setup() {
	dataReceiver.setup();
	ledPiper.setup();
        ledPiper1.setup();
        ledPiper2.setup();
        ledPiper3.setup();
        ledPiper4.setup();
        
	dataReceiver.addKey(LedController::LedPiper::KEY, &setColorsAndSend);
        dataReceiver.addKey("COLOR1", &setColorsAndSend1);
        dataReceiver.addKey("COLOR2", &setColorsAndSend2);
        dataReceiver.addKey("COLOR3", &setColorsAndSend3);
        dataReceiver.addKey("COLOR4", &setColorsAndSend4);
        
	dataReceiver.sendReady();
}

void loop() {
	dataReceiver.readAndUpdate();
}
