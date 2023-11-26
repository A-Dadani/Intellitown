#include <Wire.h>
#include <stdint.h>
#include "RGLed.h"
#include "SignalHead.h"

uint8_t selfI2CAddr = 0x8;

RGLed northLED(22, 2);
RGLed eastLED(23, 3);
RGLed westLED(24, 4);
RGLed southLED(25, 5);
SignalHead EWSignal(53, 52, 51);
SignalHead NSSignal(50, 49, 48);

void OnRequest();

void setup()
{
	Wire.begin(selfI2CAddr);
	Wire.onRequest(OnRequest);
}

void loop()
{

}

void OnRequest()
{
	Wire.write("hello world");
}