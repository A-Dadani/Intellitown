#include "SignalHead.h"
#include <Arduino.h>

SignalHead::SignalHead(uint8_t redPin, uint8_t orangePin, uint8_t greenPin)
	:
	redPin(redPin),
	orangePin(orangePin),
	greenPin(greenPin)
{
	pinMode(redPin, OUTPUT);
	pinMode(orangePin, OUTPUT);
	pinMode(greenPin, OUTPUT);
	digitalWrite(redPin, LOW);
	digitalWrite(orangePin, LOW);
	digitalWrite(greenPin, LOW);
}

void SignalHead::TurnRed() const
{
	digitalWrite(redPin, HIGH);
	digitalWrite(orangePin, LOW);
	digitalWrite(greenPin, LOW);
}

void SignalHead::TurnOrange() const
{
	digitalWrite(redPin, LOW);
	digitalWrite(orangePin, HIGH);
	digitalWrite(greenPin, LOW);
}

void SignalHead::TurnGreen() const
{
	digitalWrite(redPin, LOW);
	digitalWrite(orangePin, LOW);
	digitalWrite(greenPin, HIGH);
}

