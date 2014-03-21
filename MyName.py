#! /usr/bin/env python

import pygame

name = raw_input("Hello. What is your name?  " )
favorite_color = raw_input("What is your favorite color?  " )

##### Setup Pygame ####################################
pygame.init()
clock = pygame.time.Clock()
running = True

# Setup the Screen
screen = pygame.display.set_mode((640,400))
pygame.display.set_caption("Hello, " + name)
game_board = screen.get_rect()

#### Game Pieces ######################################

font = pygame.font.Font(None, 300)
text = font.render(name, 1, pygame.Color(favorite_color))
text_position = text.get_rect()
text_position.midleft = game_board.midright

##### Game Play Loop ##################################

while running:

	# Run 60 frames per second
	clock.tick(60)

	##### User Input ###################################

	event = pygame.event.poll()
	if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
		running = False

	##### Game Rules ###################################

	# Move the text
	text_position.centerx = text_position.centerx - 3
	if text_position.right < game_board.left:
		text_position.left = game_board.right

	##### Draw the Screen ##############################

	# Always start with a blank screen
	screen.fill((0,0,0))

	# Draw the text
	screen.blit(text, text_position)

	# Show the frame
	pygame.display.flip()

