#! /usr/bin/env python

# Snow drawing test by Chris Muggli-Miller
# Close the window to quit.
# Create 50 snowflakes, make them fall constantly,
# use a sin function to simulate wind blowing them
# right and left. When a snowflake goes below the bottom,
# reset it to a new random point above the top.
#
# This is a result of my reading Chapter 8 in the book
# "Program Arcade Games With Python And Pygame"
# by Paul Vincent Craven

import pygame
import random
import math

# constants
SCREENSIZE = [640, 480]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
PI = math.pi

def main():

	# Initialization
	pygame.init()

	screen = pygame.display.set_mode(SCREENSIZE) # Open a new window
	pygame.display.set_caption("Snow Falling")	# Title the window

	# Used for updating the screen 60 times per second, in the main loop below
	clock = pygame.time.Clock()

	# Create a list of 50 points (the snowflakes)
	snow_list = []
	
	# Arbitrary value. Determines how fast the snow blows horizontally.
	wind_strength = 100
	
	for i in range(50):
		x = random.randrange(-wind_strength, SCREENSIZE[0] + wind_strength)
		y = random.randrange(0, SCREENSIZE[1])
		snow_list.append([x, y])

	#---Main Loop---

	done = False							# when true, exit the loop
	cycle = 0.0								# in radians; controls the sin wave

	while not done:
		for event in pygame.event.get():			# Check what user did
			if event.type == pygame.QUIT:			# User clicked the close box
				done = True							# Loop ends here
	
		# First clear the screen
		screen.fill(BLACK)
	
		# Update the wind direction
		cycle += 0.01
		if cycle > 2 * PI:		# Reset it after one complete revolution (one sin cycle)
			cycle = 0
		
		wind = int(wind_strength * math.sin(cycle))	# wind blows back and forth
	
		# Process each snowflake in the list
		for i in range(len(snow_list)):
		
			# Apply the wind offset to the x value just before drawing,
			# but leave the y value as-is for now
			final_x = snow_list[i][0] + wind
			final_y = snow_list[i][1]
			
			# Draw the snowflake
			pygame.draw.circle(screen, WHITE, [final_x, final_y], 2)
		
			# Now move the flake
			snow_list[i][1] += 2	# move it 2 pixels down
		
			# If the flake is below the bottom of the screen
			if snow_list[i][1] > SCREENSIZE[1]:
				# Randomize a new starting point just above the top
				y = random.randrange(-50, -10)
				x = random.randrange(-wind_strength, SCREENSIZE[0] + wind_strength)
				snow_list[i] = [x, y]
	
		# Flip the screen to display all the new drawing
		pygame.display.flip()
	
		# Limit to 60 frames per second
		clock.tick(60)			# Wait for 1/60 of a second (I think?)
	
	# When you click the close box, close down pygame nicely
	pygame.quit()
	
if __name__ == "__main__":
	main()