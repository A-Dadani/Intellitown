#pragma once
#include <stdint.h>

class RGLed
{
public:
	RGLed(uint8_t redPin, uint8_t greenPin);

	void TurnRed() const;
	void TurnOrange() const;
	void TurnGreen() const;
	void TurnOff() const;
private:
	uint8_t redPin;
	uint8_t greenPin;
	static constexpr uint8_t greenAmountinOrange = 9;
	static constexpr uint8_t greenBrightness = 70;
};