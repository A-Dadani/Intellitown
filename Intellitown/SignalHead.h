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
	SignalHead(char selfID, uint8_t redPin, uint8_t orangePin, uint8_t greenPin);
	void TurnRed();
	void TurnOrange();
	void TurnGreen();
	Colors GetColor() const;
	static void MarkAsReported();
	static char GetIDToBeReported();
private:
	char ID;
	static char IDToBeReported;
	uint8_t redPin;
	uint8_t orangePin;
	uint8_t greenPin;
	Colors currentColor = Colors::none;
};