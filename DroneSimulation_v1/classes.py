import math
import random
#import matplotlib

#from Visualization import *
#import pylab

#import drone_awe

#m = drone_awe.model({})

#m = drone_awe.model({},plot=True)
#m.simulate()


class WSN(): ##ComplexNetwork, Environment w/ obstacles?
    def __init__(self, width, length, radius, nodes):
        """
        :param width: Int for x axis bound
        :param length: Int for y axis bound
        :param radius: Int/Float for cell radius in km
        :param Nodes: List of network nodes, first value is Base Station loc. and rest are ClusterHeads
        """
        self.width = width
        self.length = length
        self.radius = radius
        self.BS = nodes[0]
        self.C = nodes[1]
        self.nodes = nodes[1:] # {cell: 0 for cell in boundary unless cell is X distance from a cluster head}

        #self.emergency = [] ##Routes which can not be taken during specific emergencies


    def show_info(self): 
        print(self.width, 'x', self.length) 
        print('Cell Radius ', self.radius )
        print('Base Station', self.BS,  '// Nodes ', self.nodes)
        print('---------------------------')
        
        pass


    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        x = random.uniform(0, self.width)  # random float value
        y = random.uniform(0, self.length)  # random float value

        return Position(x, y)





    def is_pos_in_boundary(self, pos):
        """

        """

        xpos = pos.get_x()
        ypos = pos.get_y()

        y = self.length
        x = self.width
        r = self.radius
        center = self.C  # self.network.nodes[1]

        print(xpos, ypos, center)

        if xpos + 50 > x or xpos - 50 < 0:
            return False

        if ypos + 50 > y or ypos - 50 < 0:
            return False

        # if int(xpos) > center[0] + r*100: ###Map Coordinate
        # print("Edge of wsn")
        # return True




    def is_pos_in_cell(self, pos):
        """
        Determines if pos is inside the network.

        pos: a Position object.
        Returns: True if pos is in the network, False otherwise.
        """


        xpos = pos.get_x()
        ypos = pos.get_y()

        x = self.C[0]
        y = self.C[1]


        r = self.radius

        x3 = x - r
        y3 = y + r
        x4 = x + r
        y4 = y - r

        if xpos + 50 > x4 or xpos - 50 < x3:
            return False

        if ypos + 50 > y3 or ypos - 50 < y4:
            return False






class Drone():

    def __init__(self, name, network, battery, speed, weight, L_D, c, A ):
        """


        ######:param BS: Tuple (x,y) of the location of the drone's Base Station (starting position)  ???

        :param network:
        :param battery: int, battery capacity in mAh
        :param speed: int, avg. speed in m/s
        :param weight: float, payload weight in grams
        :param L_D: float,  Lift/Drag ratio (unitless)
        """

        ##Not initialized yet
        self.position = Position(network.BS[0], network.BS[1]) #network.get_random_position()
        self.direction = 0 #Facing North, (degrees measured CW)

        self.name = name
        self.network = network
        self.battery = battery ### Option for 2s, 3s, etc.
        self.speed = speed
        self.weight = weight #kg
        self.L_D = L_D #For fixed wing values are inbetween .10 - .30
        self.c = c #Drag coefficient of Drone
        self.A = A #Surface Area


    def show_info(self): 
        print(self.name) 
        print('battery ' , self.battery) 
        print('weight ', self.weight) 
        print('L/D ', self.L_D) 
        print('Drag Coeff ', self.c)


        print('---------------------------')        
        pass  


    #Energy consumption at each stage
    def get_drone_name(self):
        """

        """
        return self.name
    def get_drone_position(self):
        """
        Returns: a Position object giving the drone's position in the room.
        """
        return self.position

    def get_drone_direction(self):
        """
        Returns: a float d giving the direction of the drone as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.direction

    def set_rand_direction(self):

        rand = random.uniform(0,360)
        print("New Direction: ", str(rand))
        self.direction = rand

    def get_drone_speed(self):
        """

        """
        return self.speed
    def set_drone_position(self, position):
        """
        Set the position of the drone to position.

        position: a Position object.
        """
        self.position = position


    def set_drone_speed(self, speed):
        """

        """
        self.speed = speed

    def set_drone_direction(self, direction):
        """
        Set the direction of the drone to direction.

        direction: float representing an angle in degrees
        """
        self.direction = direction








    def update_position(self):
        """
        Simulates the passage of a single time-step.

        Moves drone to new position and cleans tile according to drone movement
        rules.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError

    def travel_to_location(self, loc1, loc2):
        """
        loc1: Tuple (x1,y1)
        loc2: Tuple (x2,y2)

        returns: True/False
        """

        #Find angle to travel,

        dy = int(loc2[1] - loc1[1])
        dx = int(loc2[0] - loc1[0])

        theta_rads = math.atan2(dy,dx)
        self.direction = 90 - math.degrees(theta_rads) ###Reference angle check ...

        #print(self.position, self.direction, self.speed)

        newPosition = self.get_drone_position().get_new_position(self.get_drone_direction(), self.speed)
        self.set_drone_position(newPosition)  # updating position



        #print("Arrived.")

    def hover_at_location(self, loc):
        """
        pass
        """


        for i in range(5):
            print("hovering", i)

        return True



class Weather():

    def __init__(self, T, p, w, rain, gusts = False):

        self.temp = T  ##Avg. temp. in C, 64 F  Or specify weather ... Integrate w/ Accuweather daily forecast
        self.p= p  # range of 99-102 kPa, 11.1 PSI or 25.6 kg/m^3
        self.wind_s = w[0]  # Initialy no windspeed, (Specify direction, seperaate weather class)
        self.wind_d = w[1]
        self.rain = rain #Rain %, assuming x area is covered for x duration ????

        ###Random GUSTS of winds that impact travel speed of drone... but not drag induced ??


    def show_info(self): 
        print('Temp ', self.temp) 
        print('Pressure ', self.p) 
        print('Wind: ', self.wind_s, ' ', self.wind_d) 
        print('Rain ', self.rain)
 
        print('---------------------------')        
        pass  




    def set_weather(self, T_new, p_new, w_new):
        self.temp = T_new
        self.p = p_new
        self.wind_s = w_new[0]
        self.wind_d = w_new[1]


    def set_wind(self, wind_s, wind_d):
        self.wind_s = wind_s
        self.wind_d = wind_d



    def random_wind(self):

        self.wind_s = random.uniform(1,15)
        self.wind_d = random.uniform(0,360)




class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()

        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))

        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y

        return Position(new_x, new_y)

    def __str__(self):
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))




