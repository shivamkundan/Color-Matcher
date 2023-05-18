#!/usr/local/bin/python3

import pandas as pd
import random
import pygame,sys
import pygame.freetype

pygame.init()

screen_w=440
screen_h=200
screen = pygame.display.set_mode((screen_w, screen_h),pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.ASYNCBLIT)
pygame.display.set_caption('Color Matcher')
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
red = pygame.Color(255,0,0)

HELVETICA=pygame.freetype.Font('HelveticaNeue.ttc')

clock = pygame.time.Clock()
# ==========================================================================
rand_colors=[]

for i in range(300):
	new=(random.randrange(0, 255+1),random.randrange(0, 255+1),random.randrange(0, 255+1))
	# print (f"new:{new}")
	rand_colors.append(new)

in_color_list=[(0,72,186),(0,0,0),(132,17,12),(213,203,77),\
				(128,0,0),(64,0,0),(173,234,234),(0,120,0),(100,255,255),\
				(70,130,109),(0,0,64),(255,128,0),\
				(100,90,100),(122,37,29),(122,0,29),(240,230,140)]

in_color_list=rand_colors+in_color_list
FPS=5

# ==========================================================================
def rgb_to_int(in_color):
	return (int('%02x%02x%02x' % in_color,16))

def hex_to_rgb(raw):
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
	return rgb_to_int(hex_to_rgb(raw))

# ==========================================================================
def color_match_by_hex(input_color,df):
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
	pygame.draw.rect(screen, in_color, (COL,ROW, 100, 30))

def blit_closest_color(in_color):
	pygame.draw.rect(screen, in_color, (COL,ROW+50, 100, 30))

def event_handler(color_num):
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

	df=pd.read_excel("Colors_RGB_list.xlsx",sheet_name="All",header=0,verbose=False)

	color_num=0

	while True:

		in_color_code=in_color_list[color_num]

		clock.tick(FPS)


		color_num=event_handler(color_num)


		screen.fill(black)

		HELVETICA.render_to(screen, (30,50), f"[{color_num}] {in_color_code}", white,style=0,size=18)
		blit_current_color(in_color_code)

		# Find closest match
		closest_match,min_diff_rgb,min_diff,min_name=color_match_by_rgb(in_color_code,df)

		HELVETICA.render_to(screen, (30,100), f"{min_name}", white,style=0,size=18)
		HELVETICA.render_to(screen, (30,120), f"{closest_match}", white,style=0,size=18)
		HELVETICA.render_to(screen, (30,140), f"diff: {min_diff_rgb}", white,style=0,size=16)
		HELVETICA.render_to(screen, (30,160), f"diff avg: {min_diff}", white,style=0,size=16)

		blit_closest_color(closest_match)


		pygame.display.update()
