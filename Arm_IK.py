import pygame, math
import numpy as np

from math import cos, sin, radians, atan2, degrees

 # Variables definition
width = 500
height = 500
basePoint = np.array([int(width/4), int(height/2)])

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

#Robot Definition
# Num_Links = 3
# length_Link = [80, 60, 50]



# Display Mechansim
pygame.display.init()
pygame.display.set_caption("PCCA Arm IK")
screen = pygame.display.set_mode([width, height])


class armLink():
	def __init__(self, x_, y_, length_, angle_):
		self.x = x_
		self.y = y_
		self.length = length_
		self.angle = angle_
		self.parent = None

	# Polar to Cartesian Transformation
	def getEndX(self):
		EndX = self.x + cos(self.angle) * self.length
		return EndX

	def getEndY(self):
		EndY = self.y + sin(self.angle) * self.length
		return EndY

	# Updates angle of the segment based on a Target
	def pointAt(self, targetX_, targetY_):
		dx = targetX_ - self.x
		dy = targetY_ - self.y
		self.angle = atan2(dy, dx)

	# Drag points a link towards the target and then drags it to that point.
	def drag(self, targetX_, targetY_):
		self.pointAt(targetX_, targetY_)

		# Using Trignometry to find the new point where base of link needs to be, using current angle and link length
		self.x = targetX_ - cos(self.angle) * self.length
		self.y = targetY_ - sin(self.angle) * self.length

		#If I have a prent, drag it to my base.
		if (self.parent):
			self.parent.drag(self.x, self.y)
   	
   	# Function to draw Segments of Arm
	def show(self):
		pygame.draw.line(screen, WHITE, (self.x, self.y), (self.getEndX(), self.getEndY()), 4)

def main():
	Link1 = armLink(basePoint[0], basePoint[1], 80, 0) 
	Link2 = armLink(Link1.getEndX(), Link1.getEndY(), 50, 0)
	Link3 = armLink(Link2.getEndX(), Link2.getEndY(), 100, 0)

	Link2.parent = Link1
	Link3.parent = Link2

	# Update / Loop
	while True:
		screen.fill(BLACK)
		pygame.draw.circle(screen, RED, basePoint, 15)

		Target = np.array(pygame.mouse.get_pos())
		Link3.drag(Target[0], Target[1])

		Link1.show()
		Link2.show()
		Link3.show()

		#pygame.draw.circle(screen, RED, (int(Link3.getEndX()), int(Link3.getEndY())), 10)	
		pygame.draw.circle(screen, BLUE, Target, 15)
		pygame.display.flip()
		for event in pygame.event.get():
		    if event.type == pygame.QUIT:
		        return

if __name__ == '__main__':
	main()