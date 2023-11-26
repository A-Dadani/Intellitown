#pragma once
#include <stdint.h>

class SignalHead
{
public:
	enum class Colors
	{
		none,
		red,
		orange,
		green
	};
public:
	SignalHead(uint8_t redPin, uint8_t orangePin, uint8_t greenPin);
	void TurnRed();
	void TurnOrange();
	void TurnGreen();
	Colors GetColor() const;
private:
	uint8_t redPin;
	uint8_t orangePin;
	uint8_t greenPin;
	Colors currentColor = Colors::none;
};