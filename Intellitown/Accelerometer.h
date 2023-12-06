#pragma once
#include <stdint.h>

#define	RAWMIN 0
#define RAWMAX 1023
#define SAMPLE_SIZE 10

class Accelerometer
{
public:
	Accelerometer(uint8_t xAxisPin, uint8_t yAxisPin, uint8_t zAxisPin);
	short int GetXAcceleration() const;
	short int GetYAcceleration() const;
	short int GetZAcceleration() const;
private:
	uint8_t xAxisPin;
	uint8_t yAxisPin;
	uint8_t zAxisPin;
};