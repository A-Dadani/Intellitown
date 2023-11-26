#include <Wire.h>
#include <stdint.h>
#include "RGLed.h"
#include "SignalHead.h"

uint8_t selfI2CAddr = 0x8;
unsigned long currRotationStartTime = 0ul;

RGLed northRGLED(22, 2);
RGLed eastRGLED(23, 3);
RGLed westRGLED(24, 4);
RGLed southRGLED(25, 5);
SignalHead NSSignal(50, 49, 48);
SignalHead EWSignal(53, 52, 51);

void OnRequest();

void setup()
{
	Wire.begin(selfI2CAddr);
	Wire.onRequest(OnRequest);
}

void loop()
{
	if (millis() - currRotationStartTime > 14000) currRotationStartTime = millis();
	
	if (millis() - currRotationStartTime < 5000)
	{
		NSSignal.TurnGreen();
		EWSignal.TurnRed();
	}
	else if (millis() - currRotationStartTime < 6000)
	{
		NSSignal.TurnOrange();
		EWSignal.TurnRed();
	}
	else if (millis() - currRotationStartTime < 7000)
	{
		NSSignal.TurnRed();
		EWSignal.TurnRed();
	}
	else if (millis() - currRotationStartTime < 12000)
	{
		NSSignal.TurnRed();
		EWSignal.TurnGreen();
	}
	else if (millis() - currRotationStartTime < 13000)
	{
		NSSignal.TurnRed();
		EWSignal.TurnOrange();
	}
	else if (millis() - currRotationStartTime <= 14000)
	{
		NSSignal.TurnRed();
		EWSignal.TurnRed();
	}
}

void OnRequest()
{
	Wire.write("hello world");
}