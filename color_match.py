#!/usr/local/bin/python3
import pandas as pd
import random
import pygame,sys
import pygame.freetype
import time

# Set up pygame
pygame.init()
clock = pygame.time.Clock()

# Initialize display
screen_w=640
screen_h=240
screen = pygame.display.set_mode((screen_w, screen_h),pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.ASYNCBLIT)
pygame.display.set_caption('Color Matcher')

# Colors
BLACK = pygame.Color(0, 0, 0)
YELLOW=pygame.Color(255, 153, 0)
WHITE=pygame.Color(255,255,255)
RED=pygame.Color(255,0,0)

# Load fonts
HELVETICA=pygame.freetype.Font('HelveticaNeue.ttc')
FONT_DIN=pygame.freetype.Font('din-1451-fette-breitschrift-1936.ttf')


# ==========================================================================
def random_colors(num_colors):
	''' Returns a list of random colors of size num_colors'''
	rand_colors=[]
	for i in range(num_colors):
		new=(random.randrange(0, 255+1),random.randrange(0, 255+1),random.randrange(0, 255+1))
		# print (f"new:{new}")
		rand_colors.append(new)
	return rand_colors

# ==========================================================================
def rgb_to_int(in_color):
	''' Converts RGB -> hex -> integer.'''
	return (int('%02x%02x%02x' % in_color,16))

def hex_to_rgb(raw):
	''' Convert hex code to RGB values for 8-bit color'''
	print (f"raw:{raw}")

	# If R=0
	if l==4:
		raw="00"+raw
	# If R=0 & G=0
	elif l==2:
		raw="0000"+raw
	# If (R,G,B)=(0,0,0)
	elif l==0:
		raw="000000"

	R=int(raw[0:2],16)
	G=int(raw[2:4],16)
	B=int(raw[4:6],16)

	return (R,G,B)

def hex_to_int(raw):
	''' Converts hexadecimal number to integer'''
	return rgb_to_int(hex_to_rgb(raw))

# ==========================================================================
def color_match_by_hex(input_color,df):
	''' Finds the closest color by comparing absolute hex values.'''
	rows=df.shape[0]
	min_diff=100000000
	min_name=""
	min_code=0

	# end=10
	end=rows
	for index in range(0,end):
		raw=int(str(df["Hex"][index]).lstrip("#"),16)
		name=df["Name"][index]
		diff=abs(input_color-raw)

		# names.append(name)
		# diffs.append()
		if diff<=min_diff:
			min_diff=diff
			min_code=raw
			min_name=name

			# print ("index,name,raw,diff:",index,name,hex(raw),diff)

	print ()
	print (f"input:[{hex(input_color)}], {input_color} ")
	print ("Closest match:")

	print (f"hex(min_code):{hex(min_code)}")
	rgb=hex_to_rgb(str(hex(min_code)).lstrip("0x"))

	print (f"               {min_name}:[{hex(min_code)}], {rgb} ")
	print (f"               diff: {min_diff}")

# ==========================================================================

def color_match_by_rgb(input_color,df):
	''' Finds the closest color by comparing avg of RGB difference.'''
	rows=df.shape[0]
	min_diff=100000000
	min_diff_rgb=None
	min_name=""
	min_code=0

	end=rows
	for index in range(0,end):
		# Raw vals
		R=df["R"][index]
		G=df["G"][index]
		B=df["B"][index]
		name=df["Name"][index]

		# Calculate
		diff_R=abs(R-input_color[0])
		diff_G=abs(G-input_color[1])
		diff_B=abs(B-input_color[2])

		diff_avg=round((diff_R+diff_B+diff_G)/3,2)

		# Compare
		if diff_avg<=min_diff:
			min_diff=diff_avg
			closest_match=(R,G,B)
			min_diff_rgb=(diff_R,diff_G,diff_B)
			min_name=name

			# print (name,diff_avg)
			# print (f"{index}: {name} {min_code} {min_diff}\n[{min_diff_rgb}]\n")

	# # print ()
	# # print (f"input: {input_color} ")
	# print ("Closest match:")
	# print (f"               {min_name}: {min_code} ")
	# print (f"               diff: {min_diff} [{min_diff_rgb}]")

	return closest_match, min_diff_rgb, min_diff, min_name

# ==========================================================================

ROW=screen_h//4
COL=screen_w//2
def blit_current_color(in_color):
	''' Blits rectangle with input color'''
	pygame.draw.rect(screen, in_color, (280,30, 140, 40))

def blit_closest_color(in_color):
	''' Blits rectangle with closest match color'''
	pygame.draw.rect(screen, in_color, (280,110, 140, 40))

def event_handler(color_num,in_color_code,df):
	''' For handling quit, key_left, key_right.'''
	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key==113)):
			pygame.quit()
			sys.exit()
		elif (event.type == pygame.KEYDOWN and (event.key == pygame.K_RIGHT)):
			if color_num==len(in_color_list)-1:
				color_num=0
			else:
				color_num+=1
		elif (event.type == pygame.KEYDOWN and (event.key == pygame.K_LEFT)):
			if color_num==0:
				color_num=len(in_color_list)-1
			else:
				color_num-=1
	return color_num


if __name__ == "__main__":

	# Load database of colors
	df=pd.read_excel("Colors_RGB_list.xlsx",sheet_name="All",header=0,verbose=False)

	# List of 300 random colors
	num_colors=300
	in_color_list=random_colors(num_colors)

	# Start with the first entry
	color_num=0

	FPS=0.5

	col=50



	while True:

		if color_num==1:
			time.sleep(10)
		color_num+=1

		in_color_code=in_color_list[color_num]

		clock.tick(FPS)
		color_num=event_handler(color_num,in_color_code,df)
		screen.fill(BLACK)

		# Blit input color
		FONT_DIN.render_to(screen, (col,30), f"INPUT #{color_num+1}/{num_colors}", YELLOW,style=0,size=20)
		HELVETICA.render_to(screen, (col,55), f"{in_color_code}", WHITE,style=0,size=22)
		blit_current_color(in_color_code)

		# Find closest match to input color
		closest_match,min_diff_rgb,min_diff,min_name=color_match_by_rgb(in_color_code,df)
		blit_closest_color(closest_match)

		row=120
		FONT_DIN.render_to (screen, (col,row), f"CLOSEST MATCH", YELLOW,style=0,size=18)
		HELVETICA.render_to(screen, (col,row+20), f"{min_name}", WHITE,style=0,size=26)
		HELVETICA.render_to(screen, (col,row+50), f"{closest_match}", WHITE,style=0,size=22)

		# ----------------------------------------------
		FONT_DIN.render_to (screen, (COL+150,30), f"DIFF", YELLOW,style=0,size=20)
		HELVETICA.render_to(screen, (COL+150,55), f"{min_diff_rgb}", WHITE,style=0,size=24)

		FONT_DIN.render_to (screen, (COL+150,110), f"DIFF AVG", YELLOW,style=0,size=20)
		HELVETICA.render_to(screen, (COL+150,135), f"{min_diff}", WHITE,style=0,size=34)




		pygame.display.update()
