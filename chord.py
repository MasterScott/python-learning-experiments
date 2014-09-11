#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Quick code to demonstrate combining multiple pitches together
# into a chord.

import pygame
from pygame import mixer
from pygame.mixer import Sound
from array import array
from time import sleep

# Frequencies in Hz, play_time in full seconds
# For chords, you can't just loop an individual wave cycle
# because each pitch has a different cycle length.
# Therefore, the total play time must be specified at creation.

def build_chord(frequency_list=[], play_time=1):
	# import ipdb; ipdb.set_trace()
	'''Return a sample array of multiple frequencies playing at the same time'''
	fl = len(frequency_list)
	if fl:
		# Create a sample for each frequency separately, then put them
		# into a list.
		sample_list = [0] * fl
		rate = mixer.get_init()[0]
		for i in range(fl):
			period = int(round(rate / frequency_list[i]))
			sample_list[i] = array("h", [0] * period)
			# Divide by fl to prevent final amplitude from going over the max
			amplitude = 2 ** (abs(mixer.get_init()[1]) - 1) / fl - 1
			for t in xrange(period):
				if t < period / 2:
					sample_list[i][t] = amplitude
				else:
					sample_list[i][t] = -amplitude
		# Mix the sample arrays together into one.
		# Since each cycle is a different length,
		# use mod to loop back through the cycle instead of overflowing.
		# Make an empty sound of length play_time in seconds...
		final_sample = array("h", [0] * play_time * rate)
		# ...and sum the samples in samples_list into it.
		for i in range(fl):
			for s in xrange(play_time * rate):
				final_sample[s] += sample_list[i][s % (len(sample_list[i]) - 1)]
		return final_sample
	else:
		print "Warning: No frequencies specified. Returning 0."
		return 0
		
# Crude quick test
if __name__ == '__main__':
	mixer.pre_init(44100, -16, 1, 1024)
	pygame.init()
	# Make a chord of these frequencies at 2 seconds long
	time = 2
	mychord = Sound(build_chord([220, 275, 331], time))
	mychord.play()
	sleep(time)
	pygame.quit()
	