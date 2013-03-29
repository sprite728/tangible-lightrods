//
//  PatternBarPlotToBarPlot.cpp
//  
//
//  Created by mac on 6/21/12.
//  Author: Chuan-Che Huang. chuanche@umich.edu
//

#include "PatternBarPlotToBarPlot.h"
#include "Config.h"

#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

#define DEFAULT_ACTION_INTERVAL 10
#define DEFAULT_COLOR 0x000000

LED_CONTROLLER_NAMESPACE_USING

PatternBarPlotToBarPlot::PatternBarPlotToBarPlot(byte startPosition, byte endPosition, 
	const Color& bgColor, const Color& barColor)
	:PatternSineWave(bgColor), eachActionInterval(DEFAULT_ACTION_INTERVAL)
{
	this->bgColor = bgColor;
	this->barColor = barColor;
	this->startPosition = startPosition;
	this->endPosition = endPosition;
	this->expired = false;
	reverse = false;
	increment = (startPosition > endPosition) ? -1: 1;
	currentPosition = startPosition;
}


void PatternBarPlotToBarPlot::restart()
{
	expired = false;
	currentPosition = startPosition;
	
	eachActionInterval.clearExpired();
}

bool PatternBarPlotToBarPlot::update()
{
	eachActionInterval.update();
	if(eachActionInterval.isExpired()){
		eachActionInterval.clearExpired();
		advance();
		return true;
	} else {
		return false;
	}	
}

void PatternBarPlotToBarPlot::advance()
{
	if(currentPosition != endPosition)
		currentPosition += increment;
	
	// Once the current position reaches the end point
	// set the Led Animation state to 'expired'
	if(currentPosition == endPosition){
		this->expired = true;
	}
	
}

void PatternBarPlotToBarPlot::apply(Color* stripColors)
{
	if(isReverse())
	{
		for(byte i = STRIP_LENGTH-1; i > (STRIP_LENGTH-1)-currentPosition; i--){
			float scale = calculateScale(i);
			stripColors[i].add(barColor.scaled(scale));	
		}
		for(byte i = (STRIP_LENGTH-1) - currentPosition; i >= 0; i--){
			float scale = calculateScale(i);
			stripColors[i].add(bgColor.scaled(scale));
		}
	} else {
		for(byte i = 0; i < currentPosition; i++){
			float scale = calculateScale(i);
			stripColors[i].add(barColor.scaled(scale));
		}
		for(byte i = currentPosition; i < STRIP_LENGTH; i++ ){
			float scale = calculateScale(i);
			stripColors[i].add(bgColor.scaled(scale));
		}
	}
}

void PatternBarPlotToBarPlot::setReverse(bool reverse)
{
	this->reverse = reverse;
}

bool PatternBarPlotToBarPlot::isReverse()
{
	return reverse;
}

bool PatternBarPlotToBarPlot::isExpired()
{
	return expired;
}

void PatternBarPlotToBarPlot::setExpired(bool expired)
{
	this->expired = expired;
}

void PatternBarPlotToBarPlot::setStartPosition(byte position){
	this->startPosition = position;
	increment = (startPosition > endPosition) ? -1: 1;
	currentPosition = startPosition;
}
byte PatternBarPlotToBarPlot::getStartPosition(){
	return startPosition;
}

void PatternBarPlotToBarPlot::setEndPosition(byte position){
	this->endPosition = position;
	increment = (startPosition > endPosition) ? -1: 1;
}
byte PatternBarPlotToBarPlot::getEndPosition(){
	return endPosition;
}

void PatternBarPlotToBarPlot::setBgColor(const Color& bgColor){
	this->bgColor = bgColor;
}
Color PatternBarPlotToBarPlot::getBgColor(){
	return bgColor;
}

void PatternBarPlotToBarPlot::setBarColor(const Color& barColor){
	this->barColor = barColor;
}
Color PatternBarPlotToBarPlot::getBarColor(){
	return barColor;
}


