import pygame, math
import numpy as np
import Arm_IK

from vrep import *
import time
import sys
import psutil



from math import cos, sin, radians, atan2, degrees

 # Variables definition
width = 500
height = 500
basePoint = np.array([int(width/2), int(height/2)])

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

#Robot Definition
# Num_linksArray = 3
# length_Link = [80, 60, 50]

# Display Mechansim
pygame.display.init()
pygame.display.set_caption("Robot Arm Controller")
screen = pygame.display.set_mode([width, height])

class Scaled_Arm_IK():
	def __init__(self, x_, y_):
		self.x = x_ # baseX of arm
		self.y = y_ # baseY of arm
		self.linksArray = [] # Array/List to hold all the linksArray
		self.prevLink = None # Last Arm

	def addLink(self, length_):
		link = Arm_IK.armLink(0, 0, length_, 0)
		if self.prevLink:
			link.x = self.prevLink.getEndX()
			link.y = self.prevLink.getEndY()
			link.parent = self.prevLink
		else:
			link.x = self.x
			link.y = self.y
		self.linksArray.append(link)
		self.prevLink = link

	def show(self):
		for i in range(len(self.linksArray)):
			pygame.draw.line(screen, WHITE, (self.linksArray[i].x, self.linksArray[i].y), (self.linksArray[i].getEndX(), self.linksArray[i].getEndY()), 4)

	def drag(self, x_, y_):
		self.prevLink.drag(x_, y_) # Calls drag method from the Arm_IK
		# Keeps calling parents until parent does not exist. First link

	def reach(self, x_, y_):
		self.drag(x_, y_)
		self.update()

	def update(self): # Readjusts all the previous links until the first one
		for tempLink in self.linksArray:
			if tempLink.parent is not None:
				tempLink.x = tempLink.parent.getEndX()
				tempLink.y = tempLink.parent.getEndY()
			else: # If I am the first link, then the Passed base Point is my Base point.
				tempLink.x = self.x
				tempLink.y = self.y

def wait(duration=5, str_=''):
	print(str_, end="")
	for _ in range(duration):
		print(".", end="", flush=True)
		time.sleep(1)
	print()

if not 'vrep' in [p.name() for p in psutil.process_iter()]:
	try:
		vrep_dir = "/home/ubuntu/Downloads/V-REP_PRO_EDU_V3_6_1_Ubuntu18_04/"
		scene_file = os.path.join(sys.path[0], 'IK_Test_7DOF.ttt')
		command_to_execute = "gnome-terminal -x " + vrep_dir + "vrep.sh " + scene_file
		print(f"Executing: {command_to_execute}")
		os.system(command_to_execute)
		wait(6, 'Launching V-REP.')
		print('Loading Scene File')
	except:
		print("VREP Scene file not found at /Scenes/7dof_arm_sim.ttt")
		sys.exit(0)
else:
	print("V-REP instance detected.")

def main():
	


	simxFinish(-1) # just in case, close all opened connections
	clientID=simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to V-REP

	if clientID!=-1:

		myArm = Scaled_Arm_IK(basePoint[0], basePoint[1])
		myArm.addLink(70)
		myArm.addLink(70)

		print ('Connected to remote API server')
	    # enable the synchronous mode on the client:
		simxSynchronous(clientID,True)

	    # start the simulation:
		simxStartSimulation(clientID,simx_opmode_blocking)

		returnCode, targetHandle = simxGetObjectHandle(clientID, "redundantRobot_target", simx_opmode_blocking)
		if returnCode == simx_return_ok:
			while True:
				screen.fill(BLACK)
				pygame.draw.circle(screen, RED, basePoint, 15)

				Target = np.array(pygame.mouse.get_pos())
				targetX, targetY = Target[0] - 250, Target[1] - 250
				myArm.reach(Target[0], Target[1])
				print(targetX, targetY)

				returnCode = simxSetObjectPosition(clientID, targetHandle,-1, [targetX/200, targetY/200, 0.5],simx_opmode_oneshot)
				time.sleep(0.1)

				myArm.show()
				pygame.draw.circle(screen, BLUE, Target, 15)
				pygame.display.flip()
			        

				#pygame.draw.circle(screen, RED, (int(Link3.getEndX()), int(Link3.getEndY())), 10)	

				for event in pygame.event.get():
				    if event.type == pygame.QUIT:
				        return

			simxSynchronousTrigger(clientID);

			# stop the simulation:
			simxStopSimulation(clientID,simx_opmode_blocking)

			# Now close the connection to V-REP:
			simxFinish(clientID)
	else:
	    print ('Failed connecting to remote API server')

	# Update / Loop


if __name__ == '__main__':
	main()
