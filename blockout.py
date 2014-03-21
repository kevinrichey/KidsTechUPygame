 ! /usr/bin/env python

import pygame

# Setup the game state
pygame.init()
clock = pygame.time.Clock()
running = True
game_on = True

# Setup the game board
screen = pygame.display.set_mode((640,400))
game_board = screen.get_rect()

# Start the ball off-center, moving at an angle
ball = pygame.Rect(0,0, 20,20)
ball.center = game_board.center
ball.centerx -= 100
ball_dx = 1
ball_dy = 1

# Put a rectangular paddle near the bottom
paddle = pygame.Rect(0, game_board.bottom-50, 60,10)
paddle.centerx = game_board.centerx
paddle_dx = 0
paddle_speed = 3

# Pile o' Bricks
bricks = [ 
	pygame.Rect((row*64)+2, (column*25)+40, 60,20) 
	for row in range(10) 
	for column in range(5) ]

### The Main Loop

while running:
	clock.tick(100)

	# Get user input
	event = pygame.event.poll()
	if event.type == pygame.QUIT:
		running = False

	elif event.type == pygame.KEYDOWN:
		if event.key == pygame.K_LEFT:
			paddle_dx = -paddle_speed
		elif event.key == pygame.K_RIGHT:
			paddle_dx = paddle_speed

	elif event.type == pygame.KEYUP:
		if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
			paddle_dx = 0

	# Bounce ball off the paddle.
	# Change angle by where the ball hits the paddle.
	if paddle.colliderect(ball):
		ball_dy = -ball_dy
		ball_dx = (ball.centerx - paddle.centerx) / 15

	## Bounce ball off the edges

	# Bounce off the right edge
	if ball_dx > 0 and ball.right > game_board.right:
		ball_dx = -ball_dx

	# Bounce off the left edge
	elif ball_dx < 0 and ball.left < game_board.left:
		ball_dx = -ball_dx

	# Bounce off the top edge
	if ball_dy < 0 and ball.top < game_board.top:
		ball_dy = 1

	# Game Over when ball hits the bottom
	elif ball_dy > 0 and ball.bottom > game_board.bottom:
		game_on = False
		end_message = "Game Over"

	# Ball hits a brick
	hit = ball.collidelist(bricks)
	if hit > -1:
		# Erase the brick
		brick = bricks.pop(hit)
		# Bounce off the left edge
		if ball_dx > 0 and brick.collidepoint(ball.midright):
			ball_dx = -ball_dx
		# Bounce off the right edge
		elif ball_dx < 0 and brick.collidepoint(ball.midleft):
			ball_dx = -ball_dx
		# Bounce off the top or bottom edges
		else:
			ball_dy = -ball_dy
		# If that was the last brick, you win!
		if not bricks:
			game_on = False
			end_message = "You Win!"
	
	### Draw game on the screen

	# Start with a blank screen, erase everything
	screen.fill((0,0,0))

	# Draw bricks, blue with white border
	for brick in bricks:
		pygame.draw.rect(screen, (0,64,255), brick)
		pygame.draw.rect(screen, (200,200,255), brick, 2)

	if game_on:
		# Move and draw the paddle
		paddle.left += paddle_dx
		pygame.draw.rect(screen, (255, 255, 255), paddle)

		# Move and draw the ball
		ball.centerx += ball_dx
		ball.centery += ball_dy
		pygame.draw.circle(screen, (255,64,0), ball.center, ball.width/2)

	# Show "Game Over" in the center if the player lost.
	else:
		font = pygame.font.Font(None, 36)
		text = font.render(end_message, 1, (255,255,255))
		textpos = text.get_rect()
		textpos.center = game_board.center
		screen.blit(text, textpos)

	# Show the frame
	pygame.display.flip()

