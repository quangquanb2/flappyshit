# Import 
import pygame
import sys
import random
import numpy as np
from pygame.locals import *

pygame.init()

# Colours
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
GREEN = (  0, 128,   0)

# Basic setup
FPS = 120
WIDTH, HEIGHT = 1200, 750

# Encountered
def encountered(ObjX, ObjY, bulletX, bulletY):
	if(bulletX in range(ObjX, ObjX + 125)) and (bulletY in range(ObjY, ObjY + 79)):
		return 1
	if(bulletX + 32 in range(ObjX, ObjX + 125)) and (bulletY + 32 in range(ObjY, ObjY + 79)):
		return 1
	return 0

# Bullet movement
def bulletMovement(bulletInf, speed, scores, rate, tmpW, tmpH):
	if bulletInf[2] == tmpW - 10:
		bulletInf[0] -= (speed + scores // rate)
	elif bulletInf[2] == 10:
		bulletInf[0] += (speed + scores // rate)
	
	if bulletInf[3] < tmpH // 4:
		bulletInf[1] += (speed + scores // rate)
	elif bulletInf[3] > int(tmpH * .75):
		bulletInf[1] -= (speed + scores // rate)

def main(MAX_):

	# Create Object
	ObjX, ObjY = 10, 10
	ObjW, ObjH = 125, 79
	Obj = pygame.image.load('cat.png')
	Obj = pygame.transform.flip(Obj,1,0)
	orObj = Obj

	# Create Bullet (shit)
	# General 
	bulletW, bulletH = 32, 32
	bullet = pygame.image.load('shit.png')
	bullet = pygame.transform.scale(bullet, (bulletW,bulletH))
	
	# Bullet 1
	listBulletX = [10, WIDTH - 10]
	bulletX = random.choice(listBulletX)
	orgBulletX = bulletX
	bulletY = random.randint(10,HEIGHT - 10)
	orgBulletY = bulletY
	flag = 0
	bulletInf = [bulletX, bulletY, orgBulletX, orgBulletY]
	
	# Bullet 2
	bullet2 = bullet
	bulletX2 = random.randint(0,WIDTH - 10)
	orgBulletX2 = bulletX2
	listBulletY2 = [10, HEIGHT - 10]
	bulletY2 = random.choice(listBulletY2)
	orgBulletY2 = bulletY2
	flag2 = 0
	bulletInf2 = [bulletY2, bulletX2, orgBulletY2, orgBulletX2]
	
	# Others
	moving = 1
	time = 0
	scores = 0
	direction = 'right'
	
	# Warning
	text = pygame.font.Font('freesansbold.ttf', 32)
	warning = text.render("WARNING", True, WHITE, GREEN)
	warningPos = warning.get_rect()
	warningPos.center = (WIDTH // 2, HEIGHT // 2)
	
	# Window Display and Background
	SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
	BGROUND = pygame.image.load('background.png')
	
	while True:

		# SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
		pygame.display.set_caption('Flappy Cat')

		# Background
		SCREEN.blit(BGROUND, (0, 0))
		
		# Basic
		speed = 15
		rate = 25
		Won = 0
		
		if moving:
		
			# Obj movement
			time += 1
			
			if direction == 'up':
				ObjY -= (time + 1)
				Obj = pygame.transform.rotate(orObj,15)
				if ObjY <=10:
					time = 0
					direction = 'down'
			elif direction == 'down':
				ObjY += time * 2 + 1
				Obj = pygame.transform.rotate(orObj,-15)
				if ObjY >=HEIGHT - ObjW:
					time = 0
					direction = 'up'
			elif direction == 'right':
				ObjX += 2
				Obj = orObj
				if ObjX >=WIDTH - ObjW:
					Obj = pygame.transform.flip(Obj,0,1)
					direction = 'left'	
			elif direction == 'left':
				ObjX -= 1
				Obj = pygame.transform.flip(orObj,1,0)
				if ObjX <=10:
					Obj = pygame.transform.flip(Obj,1,0)
					direction = 'right'
			
			# Create new bullet 
			if flag:
				bulletInf[1] = random.randint(1,HEIGHT - 10)
				bulletInf[3] = bulletInf[1]
				bulletInf[0] = random.choice(listBulletX)
				bulletInf[2] = bulletInf[0]
				flag = 0
			if flag2:
				bulletInf2[1] = random.randint(1,WIDTH - 10)
				bulletInf2[3] = bulletInf2[1]
				bulletInf2[0] = random.choice(listBulletY2)
				bulletInf2[2] = bulletInf2[0]
				flag2 = 0
			if (bulletInf[0] < 0 or bulletInf[0] > WIDTH) or (bulletInf[1] >= HEIGHT or bulletInf[1] <= 0):
				flag = 1
			if (bulletInf2[1] < 0 or bulletInf2[1] > WIDTH) or (bulletInf2[0] >= HEIGHT or bulletInf2[0] <= 0):
				flag2 = 1
				
			scores = int((1339 - np.sqrt((WIDTH - 40 - ObjX)**2 + (HEIGHT - 162//2 - ObjY)**2))//60)
			
			# Bullet movement
			tmpW, tmpH = WIDTH, HEIGHT
			
			bulletMovement(bulletInf, speed, scores, rate, tmpW, tmpH)	# Bullet 1 movement
			bulletMovement(bulletInf2, speed, scores, rate, tmpH, tmpW) # Bullet 2 movement
			
			# Score displaying and calculating
			if scores // 2 >= MAX_: MAX_ = scores // 2
			HighScoresDisplay = text.render("BEST: " + str(MAX_), True, WHITE)
			scoresDisplay = text.render("SCORE: " + str(scores//2), True, WHITE)
			
			# Drawing out the screen 
			SCREEN.blit(Obj, (ObjX, ObjY))
			SCREEN.blit(bullet, (bulletInf[0], bulletInf[1]))
			SCREEN.blit(bullet2, (bulletInf2[1], bulletInf2[0]))
			SCREEN.blit(scoresDisplay, (WIDTH - 250, 30))
			SCREEN.blit(HighScoresDisplay, (WIDTH - 450, 30))
		
		for event in pygame.event.get():
			
			# Exit
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		
			keyEvent = pygame.key.get_pressed()
			# if not moving and (keyEvent[pygame.K_UP] or keyEvent[pygame.K_DOWN] or keyEvent[pygame.K_LEFT] or keyEvent[pygame.K_RIGHT]):
			if not moving and (keyEvent[pygame.K_SPACE]):
				main(MAX_)
				
			# Key event detection
			if keyEvent: time = 0
			if keyEvent[pygame.K_UP] or keyEvent[pygame.K_w]:
				direction = 'up'
			if keyEvent[pygame.K_DOWN] or keyEvent[pygame.K_s]:
				direction = 'down'
			if keyEvent[pygame.K_LEFT] or keyEvent[pygame.K_a]:
				direction = 'left'
			if keyEvent[pygame.K_RIGHT] or keyEvent[pygame.K_d]:
				direction = 'right'
				
		# Encountered check
		if encountered(ObjX, ObjY, bulletInf[0], bulletInf[1]) or encountered(ObjX, ObjY, bulletInf2[1], bulletInf2[0]):
			moving = 0
			
		# Winning check
		if (ObjX + ObjW >= WIDTH - 40) and (ObjY + ObjH >= 585) and not Won:
			moving, Won = 0, 1
		
		# Losing animation 
		if not moving and ObjY < HEIGHT and not Won:
			Obj = pygame.transform.rotate(orObj, -ObjY//10)
			SCREEN.blit(Obj, (ObjX, ObjY))
			ObjY += 8
			
		# Winning, Losing anouncement
		if Won:
			warning = text.render("YOU WON", True, WHITE, GREEN)
			SCREEN.blit(warning, warningPos)
		elif ObjY > HEIGHT:
			warning = text.render("YOUR SCORE: " + str(scores//2), True, WHITE, GREEN)
			SCREEN.blit(warning, warningPos)
		
		pygame.display.update()
		pygame.time.Clock().tick(FPS)

if __name__ == '__main__':
	MAX_ = 0
	main(MAX_)