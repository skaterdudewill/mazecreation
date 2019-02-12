'''
MAZE MAKING
https://www.jamisbuck.org/mazes/
http://www.astrolog.org/labyrnth/algrithm.htm
MAZE SOLVING

--VIDEO
-SHOW THE CREATION
-COLOR CODE TO MAKE CLEARER
-SEE IT SOLVE THE ONE YOU MADE

--GAME
-GIVE A WEBSITE THAT WILL LET YOU DOWNLOAD AN IMAGE
-SOLVE THAT MAZE
-WEB API TO UPLOAD SOLUTION [(0,0),(1,0),(1,1),....]
'''

import cv2
import numpy as np #matrix/array manipulation
import random
from PIL import Image
width = 20
height = 20


def rbtGeneration():
	print('Creating Maze')
	img = np.zeros((height * 2 + 1, width * 2 + 1), dtype=np.uint8)
	img[1::2, 1::2] = 1
	stack = [(1, 1)]
	count = 0
	prevLocations = []
	prevLocations.append((1, 1))
	while stack:
		i = random.randrange(len(stack))
		i = -1
		x, y = stack[i]
		img[y, x] = 255
		colorImg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
		# colorImg[y,x]=(255,0,0)
		counter = 0
		for jy, jx in prevLocations[len(prevLocations)::-1]:
			colorImg[y, x] = (255, 255, 0)
			colorImg[jy, jx] = (counter, counter, 255)
			counter += 1

		possibleNeighbors = []
		for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
			wallx = x + dx
			wally = y + dy
			if np.all(img[wally, wallx] != 0) or np.all(wallx == 0) or np.all(wally == 0) or np.all(
					wallx == width * 2) or np.all(wally == height * 2):
				continue
			nextNodex = x + 2 * dx
			nextNodey = y + 2 * dy
			if np.all(img[nextNodey, nextNodex] == 1):
				possibleNeighbors.append((nextNodex, nextNodey))
		if possibleNeighbors:
			x2, y2 = random.choice(possibleNeighbors)
			img[y2, x2] = 255  # 255
			img[(y + y2) // 2, (x + x2) // 2] = 255  # knock wall
			stack.append((x2, y2))
			location = (y2, x2)
			wall = (y + y2) // 2, (x + x2) // 2

			prevLocations.append(location)
			prevLocations.append(wall)
			while len(prevLocations) > 255:
				prevLocations.pop(0)

		else:
			stack.pop(i)
		cv2.imwrite("rbtMaze%03d.png" % count, colorImg)
		count += 1
	cv2.imwrite("rbtMaze.png", img)
	return img
	print('Finished!')
def binaryGeneration():
	print("Creating Binary Maze")
	img = np.zeros((height*2+1,width*2+1),dtype=np.uint8)
	img[1::2,1::2] = 1
	stack = [(1,1)]
	prevLocations=[]
	count = 0
	x = width * 2 - 1
	y = height * 2 - 1
	prevLocations.append((y,x))
	colorImg=cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
	first=False
	while y > 0:
		x=width*2 - 1
		location=(y,x)
		prevLocations.append(location)
		while len(prevLocations)>255:
			prevLocations.pop(0)
		if (first):
			location=(y-2,x)
			prevLocations.append(location)
			while len(prevLocations)>255:
				prevLocations.pop(0)
			y -= 2
		if (y <1):
				print("Stopping")
				y-=1000
		while x > 0:
			counter=0
			for jy,jx in prevLocations[len(prevLocations)::-1]:
				colorImg[y,x]=(255,255,0)
				colorImg[jy,jx]=(counter,counter,255)
				counter+=1
			img[y,x]=255
			rand = random.randint(0,1)
			if (x == 1):
				if (y == 1):
					location=(y,x)
					prevLocations.append(location)
					while len(prevLocations)>255:
						prevLocations.pop(0)
					cv2.imwrite("maze%03d.png" % count, colorImg)
					x-=1000
					y-=1000
				else:
					location = (y - 1, x)
					prevLocations.append(location)
					while len(prevLocations) > 255:
						prevLocations.pop(0)
					img[y-1,x]=255
					print("Up")
					x-=2
			elif (y == 1):
				location = (y, x)
				prevLocations.append(location)
				prevLocations.append((y, x - 1))
				while len(prevLocations) > 255:
					prevLocations.pop(0)
				img[y,x]=255
				x-=1
			elif(rand == 0):
				location = (y, x - 1)
				prevLocations.append(location)
				prevLocations.append((y, x - 2))
				while len(prevLocations) > 255:
					prevLocations.pop(0)
				print("left")
				img[y,x-1]=255
				x -= 2
			elif(rand == 1):
				location = (y - 1, x)
				prevLocations.append(location)
				prevLocations.append((y, x - 2))
				while len(prevLocations) > 255:
					prevLocations.pop(0)
				print("up")
				img[y-1,x]=255
				x -= 2
			else:
				print("What???")
			cv2.imwrite("maze%03d.png" % count, colorImg)
			count+=1
		first=True
	cv2.imwrite("binaryMaze.png",img)
	return img

x=1
y=1
image = cv2.imread("binaryMaze.png")
correctPath = image
followImg = image
wasHere= np.zeros((height*2+1,width*2+1))
counting=0


def mazeSolver(x,y):
	global counting
	newwidth,newheight,z=followImg.shape
	if x==39 and y==39:
		return True
	if np.all(followImg[y,x] == 0):
		return False
	if wasHere[y,x]:
		correctPath[y,x]=(0,255,255)
		cv2.imwrite("binarysolve%03d.png" % counting, correctPath)
		counting+=1
		return False
	wasHere[y,x] = True
	correctPath[y,x]=(255,0,0)
	cv2.imwrite("binarysolve%03d.png" % counting, correctPath)
	counting+=1
	if x != 0 and mazeSolver(x-1,y):
		correctPath[y,x] = (0,0,255)
		cv2.imwrite("binarysolve%03d.png" % counting, correctPath)
		counting+=1
		return True
	if x != newwidth and mazeSolver(x+1,y):
		correctPath[y,x] = (0,0,255)
		cv2.imwrite("binarysolve%03d.png" % counting, correctPath)
		counting+=1
		return True
	if y != 0 and mazeSolver(x, y-1):
		correctPath[y,x] = (0,0,255)
		cv2.imwrite("binarysolve%03d.png" % counting, correctPath)
		counting+=1
		return True
	if y != newheight and mazeSolver(x,y+1):
		correctPath[y,x] = (0,0,255)
		print("Found")
		cv2.imwrite("binarysolve%03d.png" % counting, correctPath)
		counting+=1
		return True
	return False

correctPath[height*2-1,width*2-1] = (0, 0, 255)
cv2.imwrite("binarysolve%03d.png" % counting, correctPath)
mazeSolver(1,1)
#cv2.imwrite("maze.png",img)