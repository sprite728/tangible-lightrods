//
//  PatternChangingColorColumn.h
//  
//
//  Created by mac on 6/21/12.
//  Author: Chuan-Che Huang. chuanche@umich.edu
//

#include "PatternChangingColorColumn.h"
#include "Config.h"

#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

#define DEFAULT_COLOR 0x808080	// Middle Brightness White: r=g=b=128

// For sinosoidal texture
#define DEFAULT_SINE_WAVE_FRAMES MAX_SINE_WAVE_FRAME
#define DEFAULT_SINE_WAVE_ORIGIN 0.45	//min: 0.0 , max: 1.0
#define DEFAULT_SINE_WAVE_AMPLITUDE 0.4	// origin + aplitude can not go over 1.0
#define MAX_SINE_WAVE_FRAME 80
#define MIN_SINE_WAVE_FRAME 40

LED_CONTROLLER_NAMESPACE_USING
PatternChangingColorColumn::PatternChangingColorColumn() :
	amplitude(DEFAULT_SINE_WAVE_AMPLITUDE),
	origin(DEFAULT_SINE_WAVE_ORIGIN),
	numOfFrames(DEFAULT_SINE_WAVE_FRAMES)
{
	Color defaultColor = Color(DEFAULT_COLOR);
	addColor(defaultColor);
}

PatternChangingColorColumn::PatternChangingColorColumn(const Color& color) :
	amplitude(DEFAULT_SINE_WAVE_AMPLITUDE),
	origin(DEFAULT_SINE_WAVE_ORIGIN),
	numOfFrames(DEFAULT_SINE_WAVE_FRAMES)
{
	addColor(color);
}

void PatternChangingColorColumn::advance()
{
	currentDisplayedColorIndex++;
	if(currentDisplayedColorIndex >= colorArrayTop)
		currentDisplayedColorIndex = 0;
}


bool PatternChangingColorColumn::update()
{
	if(isEmpty()){
		return false;
	} else {
		advance();
		return true;
	}
}


bool PatternChangingColorColumn::updateSine()
{
	sineWaveFrameCounter++;
	if(sineWaveFrameCounter >= numOfFrames){
		sineWaveFrameCounter = 0;
	}
}

void PatternChangingColorColumn::apply(Color* stripColors)
{
	if(!isEmpty()){
		for(int i = 0; i < STRIP_LENGTH; i++){
			float scale = calculateScale(i);
        	stripColors[i].add(colorArray[currentDisplayedColorIndex].scaled(scale));
    	}
	}
	else {
		// No Color exists in the color array
		Color defaultColor = Color(DEFAULT_COLOR);
		for(int i = 0; i < STRIP_LENGTH; i++){
			float scale = calculateScale(i);
        	stripColors[i].add(defaultColor.scaled(scale));
    	}
	}
}

void PatternChangingColorColumn::restart()
{
	currentDisplayedColorIndex = 0;
}


float PatternChangingColorColumn::calculateScale(byte aLedIndex)
{
	float phaseShift = float(aLedIndex)/STRIP_LENGTH;
	float scale = origin + 
		amplitude*sin((float(sineWaveFrameCounter)/numOfFrames + phaseShift)*2*PI);
	return scale;
}

bool PatternChangingColorColumn::addColor(const Color& color)
{
	if(isFull())	//Color array is full now
		return false;
	else {
		colorArray[colorArrayTop] = color;
		colorArrayTop++;
		return true;
	}
}

bool PatternChangingColorColumn::deleteColor(const Color& color)
{
	if(isEmpty())
		return false;
	else {
		colorArrayTop--;
		return true;
	}	
}

bool PatternChangingColorColumn::deleteAll()
{
	if(isEmpty()){
		return false;
	} else {
		colorArrayTop = 0;
		return true;
	}
	
}

bool PatternChangingColorColumn::isFull()
{
	if(colorArrayTop == DEFAULT_MAX_COLORS)
		return true;
	else 
		return false;
}

bool PatternChangingColorColumn::isEmpty()
{
	if(colorArrayTop == 0)
		return true;
	else 
		return false;
}

void PatternChangingColorColumn::setNumOfFrames(byte frame)
{
	if(frame > MAX_SINE_WAVE_FRAME)
		this->numOfFrames = MAX_SINE_WAVE_FRAME;
	else if (frame < MIN_SINE_WAVE_FRAME)
		this->numOfFrames = MIN_SINE_WAVE_FRAME;
	else 
		this->numOfFrames = frame; 
}
