#include "SignalHead.h"
#include <Arduino.h>

char SignalHead::IDToBeReported = 0;

SignalHead::SignalHead(char ID, uint8_t redPin, uint8_t orangePin, uint8_t greenPin)
	:
	ID(ID),
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

void SignalHead::TurnRed()
{
	if (currentColor == Colors::red) return;
	digitalWrite(redPin, HIGH);
	digitalWrite(orangePin, LOW);
	digitalWrite(greenPin, LOW);
	currentColor = Colors::red;
	IDToBeReported = ID;
}

void SignalHead::TurnOrange()
{
	if (currentColor == Colors::orange) return;
	digitalWrite(redPin, LOW);
	digitalWrite(orangePin, HIGH);
	digitalWrite(greenPin, LOW);
	currentColor = Colors::orange;
}

void SignalHead::TurnGreen()
{
	if (currentColor == Colors::green) return;
	digitalWrite(redPin, LOW);
	digitalWrite(orangePin, LOW);
	digitalWrite(greenPin, HIGH);
	currentColor = Colors::green;
}

SignalHead::Colors SignalHead::GetColor() const
{
	return currentColor;
}

void SignalHead::MarkAsReported()
{
	IDToBeReported = 0;
}

char SignalHead::GetIDToBeReported()
{
	return IDToBeReported;
}