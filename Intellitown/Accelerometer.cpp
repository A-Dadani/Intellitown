#include "Accelerometer.h"
#include <Arduino.h>

Accelerometer::Accelerometer(uint8_t xAxisPin, uint8_t yAxisPin, uint8_t zAxisPin)
	:
	xAxisPin(xAxisPin),
	yAxisPin(yAxisPin),
	zAxisPin(zAxisPin)
{
	pinMode(xAxisPin, INPUT);
	pinMode(yAxisPin, INPUT);
	pinMode(zAxisPin, INPUT);
}

short int Accelerometer::GetXAcceleration() const
{
	long reading = 0;
	analogRead(xAxisPin);
	delay(1);
	for (int i = 0; i < SAMPLE_SIZE; i++)
	{
		reading += analogRead(xAxisPin);
	}
	return map(reading / SAMPLE_SIZE, RAWMIN, RAWMAX, -3000, 3000);
}

short int Accelerometer::GetYAcceleration() const
{
	long reading = 0;
	analogRead(yAxisPin);
	delay(1);
	for (int i = 0; i < SAMPLE_SIZE; i++)
	{
		reading += analogRead(yAxisPin);
	}
	return map(reading / SAMPLE_SIZE, RAWMIN, RAWMAX, -3000, 3000);
}

short int Accelerometer::GetZAcceleration() const
{
	long reading = 0;
	analogRead(zAxisPin);
	delay(1);
	for (int i = 0; i < SAMPLE_SIZE; i++)
	{
		reading += analogRead(zAxisPin);
	}
	return map(reading / SAMPLE_SIZE, RAWMIN, RAWMAX, -3000, 3000);
}
