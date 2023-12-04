#include <Wire.h>
#include <stdint.h>
#include "RGLed.h"
#include "SignalHead.h"

#define SEND_BUFFER_SIZE 3
#define RECEIVE_BUFFER_LIMIT 4
#define SELF_ID 's'

uint8_t selfI2CAddr = 0x8;
unsigned long currRotationStartTime = 0ul;
RGLed NSRGLED(22, 2);
RGLed EWRGLED(23, 3);
RGLed WERGLED(24, 4);
RGLed XXRGLED(25, 5);
SignalHead NSSignal('n', 50, 49, 48);
SignalHead EWSignal('e', 53, 52, 51);

void OnReceive(int);

void OnRequest();

void setup()
{
	Wire.begin(selfI2CAddr);
	Wire.onReceive(OnReceive);
	Wire.onRequest(OnRequest);
}

void loop()
{
#pragma region Traditional Traffic Lights
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
#pragma endregion 


}

void OnRequest()
{
	byte report[SEND_BUFFER_SIZE];
	if (SignalHead::GetIDToBeReported() == 0)
	{
		for (int i = 0; i < SEND_BUFFER_SIZE; ++i)
		{
			report[i] = 0;
		}
		Wire.write(report, SEND_BUFFER_SIZE);
	}
	else
	{
		report[0] = 1;
		report[1] = SELF_ID;
		report[2] = SignalHead::GetIDToBeReported();
		SignalHead::MarkAsReported();
		Wire.write(report, SEND_BUFFER_SIZE);
	}
}

void OnReceive(int)
{
	byte receivedData[RECEIVE_BUFFER_LIMIT];
	Wire.read();
	for (int i = 0; i < RECEIVE_BUFFER_LIMIT && Wire.available(); ++i)
	{
		receivedData[i] = Wire.read();
	}
	if (receivedData[0] == 1)
	{
		if (receivedData[1] == 'n')
		{
			if (receivedData[2] == 's')
			{
				switch (receivedData[3])
				{
				case 0:
					NSRGLED.TurnGreen();
					break;
				case 1:
					NSRGLED.TurnOrange();
					break;
				case 2:
					NSRGLED.TurnRed();
					break;
				default:
					return;
				}
			}
		}
		else if (receivedData[1] == 'e')
		{
			if (receivedData[2] == 'w')
			{
				switch (receivedData[3])
				{
				case 0:
					EWRGLED.TurnGreen();
					break;
				case 1:
					EWRGLED.TurnOrange();
					break;
				case 2:
					EWRGLED.TurnRed();
					break;
				default:
					return;
				}
			}
		}
		else if (receivedData[1] == 's')
		{
			if (receivedData[2] == 'n')
			{
				switch (receivedData[3])
				{
				case 0:
					XXRGLED.TurnGreen();
					break;
				case 1:
					XXRGLED.TurnOrange();
					break;
				case 2:
					XXRGLED.TurnRed();
					break;
				default:
					return;
				}
			}
		}
		else if (receivedData[1] == 'w')
		{
			if (receivedData[2] == 'e')
			{
				switch (receivedData[3])
				{
				case 0:
					WERGLED.TurnGreen();
					break;
				case 1:
					WERGLED.TurnOrange();
					break;
				case 2:
					WERGLED.TurnRed();
					break;
				default:
					return;
				}
			}
		}
	}
}