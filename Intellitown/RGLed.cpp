#include "RGLed.h"
#include <stdint.h>
#include <Arduino.h>

RGLed::RGLed(uint8_t redPin, uint8_t greenPin)
	:
	redPin(redPin),
	greenPin(greenPin)
{
	pinMode(redPin, OUTPUT);
	pinMode(greenPin, OUTPUT);
	TurnOff();
}

void RGLed::TurnRed() const
{
	analogWrite(greenPin, 0);
	digitalWrite(redPin, HIGH);
}

void RGLed::TurnOrange() const
{
	digitalWrite(redPin, HIGH);
	analogWrite(greenPin, greenAmountinOrange);
}

void RGLed::TurnGreen() const
{
	digitalWrite(redPin, LOW);
	analogWrite(greenPin, greenBrightness);
}

void RGLed::TurnOff() const
{
	digitalWrite(redPin, LOW);
	digitalWrite(greenPin, LOW);
}
