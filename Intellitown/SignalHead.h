#pragma once
#include <stdint.h>

class SignalHead
{
public:
	SignalHead(uint8_t redPin, uint8_t orangePin, uint8_t greenPin);
	void TurnRed() const;
	void TurnOrange() const;
	void TurnGreen() const;
private:
	uint8_t redPin;
	uint8_t orangePin;
	uint8_t greenPin;
};