import math
import random
import matplotlib

from Visualization import *
import pylab

import time as t
import base64
from tkinter import *
from tkinter.ttk import Progressbar

from main import*

#import drone_awe

#m = drone_awe.model({})

#m = drone_awe.model({},plot=True)
#m.simulate()




 ################ TXT FILES
 #########





#############
### Position
#############




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

    def get_new_position(self, angle, speed, weather = None):
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



#############
### Weather
#############

class Weather(object):

    def __init__(self, T, p, w, rain, gusts = False):

        self.temp = T  ##Avg. temp. in C, 64 F  Or specify weather ... Integrate w/ Accuweather daily forecast
        self.p= p  # range of 99-102 kPa, 11.1 PSI or 25.6 kg/m^3
        self.wind_s = w[0]  # Initialy no windspeed, (Specify direction, seperaate weather class)
        self.wind_d = w[1]
        self.rain = rain #Rain %, assuming x area is covered for x duration ????

        ###Random GUSTS of winds that impact travel speed of drone... but not drag induced ??

    def set_weather(self, T_new, p_new, w_new):
        self.temp = T_new
        self.p = p_new
        self.wind_s = w_new[0]
        self.wind_d = w_new[1]


    def set_wind(self, wind_s, wind_d):
        self.wind_s = wind_s
        self.wind_d = wind_d



    def random_gust(self):

        self.wind_s = random.uniform(1,15)
        self.wind_d = random.uniform(0,360)






#############
### Network
#############



class Network(): ##ComplexNetwork, Environment w/ obstacles?
    def __init__(self, width, length, radius, nodes):
        """
        :param width: Int for x axis bound
        :param length: Int for y axis bound
        :param radius: Int/Float for cell radius in km
        :param Nodes: List of network nodes, first value is Base Station loc. and rest are ClusterHeads
        """
        #print(type(nodes))

        if type(nodes) != list:

            temp = nodes.split(";")
            self.nodes = []

            for t in temp:  ##Converting from Str to Tuple
                temp2 = t.split(',')
                num1 = int(temp2[0][1:]) #Exclude parantheses
                num2 = int(temp2[1][:len(temp2[1]) -1])
                self.nodes.append((num1, num2))

            self.BS = self.nodes[0]
            self.C = self.nodes[1]

        else:
            self.BS = list(nodes[0])
            self.C = list(nodes[1])
            self.nodes = nodes # {cell: 0 for cell in boundary unless cell is X distance from a cluster head}



        self.width = int(width)
        self.length = int(length)
        self.radius = int(radius)
        #self.BS = list(nodes[0])
        #self.C = list(nodes[1])
        #self.nodes = temp # {cell: 0 for cell in boundary unless cell is X distance from a cluster head}

        self.emergency = [] ##Routes which can not be taken during specific emergencies


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



class SimpleNetwork(Network):

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

#############
### Drone
#############


class Drone():

    def __init__(self, name, network, battery, cells, speed, weight, L_D, c, A ):
        """


        ######:param BS: Tuple (x,y) of the location of the drone's Base Station (starting position)  ???

        :param network:
        :param battery: int, battery capacity in mAh
        :param speed: int, avg. speed in m/s
        :param weight: float, payload weight in grams
        :param L_D: float,  Lift/Drag ratio (unitless)
        """

        ##Not initialized yet

        ###UNCOMMENT POSITION, ADD BATTERY CELL, Convert instantiations into proper types

        self.position = None #Position(network.BS[0], network.BS[1]) #network.get_random_position()
        self.direction = 0 #Facing North, (degrees measured CW)

        self.name = str(name)

        if type(network) == str:
            self.network = int(network)
        else:
            self.network = network


        self.battery = float(battery) ### Option for 2s, 3s, etc.
        self.cells = int(cells)
        self.speed = int(speed)
        self.weight = float(weight) #kg
        self.L_D = float(L_D) #For fixed wing values are inbetween .10 - .30
        self.c = float(c) #Drag coefficient of Drone
        self.A = float(A) #Surface Area


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




class StandardDrone(Drone):

    ###Set channel amount
    ###Set dropped call probability
    ##More?


    def update_position_noWind(self):
        """
        Simulates the passage of a single time-step.

        Calculate the next position for the robot.

        If that position is valid, move the robot to that position. Mark the
        tile it is on as having been cleaned by capacity amount.

        If the new position is invalid, do not move or clean the tile, but
        rotate once to a random new direction.
        """

        #print("in here x2")
        newPosition = self.get_drone_position().get_new_position(self.get_drone_direction(), self.speed)

        #if self.network.is_pos_in_room(newPosition):
            #print("new pos updated", newPosition)

        self.set_drone_position(newPosition)  # updating position

        #else:  # if position isn't valid
            #print("random direction")
            #self.set_drone_direction(random.uniform(0, 360))  # get new random direction

        def update_position_wind(self):
            pass


###########
##Visualization
###############





class DroneVisualization:
    def __init__(self, num_drones, width, height, radius, network, delay = 0.1 ):
        # Number of seconds to pause after each frame
        self.delay = delay
        self.max_dim = max(width, height)

        self.num_drones = num_drones

        self.width = width
        self.height = height
        self.radius = radius
        self.network = network

        self.BS = network.BS
        self.center = network.C

        # Initialize a drawing surface
        self.master = Tk()
        self.w = Canvas(self.master, width=500, height=500) ##Dialog box size
        self.w.pack()
        self.master.update()

        # Draw a backing and lines
        b1, c1 = self._map_coords(0, 0) ##MapCOORDS (READ DOCS), curvature???
        b2, c2 = self._map_coords(width, height)
        self.w.create_rectangle(b1, c1, b2, c2, fill="white")

        print(self.BS, self.center)

        x, y = self._map_coords(int(self.center[0]), int(self.center[1]))
        print("center", x,y)
        r = self._map_coords(self.radius, 0)[0]  #km -> m ### Scaling???? map coord b4 or after I find vertices?
        #print(r)



        #print(v1, v2, v3, v4, v5, v6)

        x3 = x-r
        y3 = y+r
        x4 = x+r
        y4 = y-r

        self.WSN_bounds = [(x3,y3), (x4,y4)]

        #x3, y3 = self._map_coords(x - radius, y+radius )
        #x4, y4 = self._map_coords(x + radius, y-radius )

        self.w.create_rectangle(x3,y3,x4,y4, width = 4)
        #x4, y4 = self._map_coords(int(self.BS[0]), int(self.BS[1]))



        #----------------------------------------------------


        ##Some Text
        self.drones = None
        self.text = self.w.create_text(25, 0, anchor=NW, text=self._status_string(0, 0, 1))
        self.time = 0

        # Bring window to front and focus
        self.master.attributes("-topmost", True)  # Brings simulation window to front upon creation
        self.master.focus_force()  # Makes simulation window active window
        self.master.attributes("-topmost", False)  # Allows you to bring other windows to front

        self.master.update()

    def _status_string(self, time, num_clean_tiles, num_total_tiles):
        "Returns an appropriate status string to print."
        channels_available = 10
        status = "Time: " + str(time) + "s. ; ValidChannel" \
                                        "" \
                                        "" \
                                        "" \
                                        "" \
                                        "" \
                                        "s: " + str(num_clean_tiles) + " with a " + str(num_total_tiles) + "% dropped call probability."

        return status

    def _map_coords(self, x, y):
        "Maps grid positions to window positions (in pixels)."
        return (250 + 450 * ((x - self.width / 2.0) / self.max_dim),
                250 + 450 * ((self.height / 2.0 - y) / self.max_dim))

    def _draw_robot(self, position, direction):
        "Returns a polygon representing a robot with the specified parameters."
        x, y = position.get_x(), position.get_y()
        d1 = direction + 165
        d2 = direction - 165
        x1, y1 = self._map_coords(x, y)
        x2, y2 = self._map_coords(x + 60 * math.sin(math.radians(d1)),
                                  y + 60 * math.cos(math.radians(d1)))
        x3, y3 = self._map_coords(x + 60 * math.sin(math.radians(d2)),
                                  y + 60 * math.cos(math.radians(d2)))

        return self.w.create_polygon([x1, y1, x2, y2, x3, y3], fill="red")

    def update(self, network, drones):

        #self.drones = drones
        # Delete all existing robots.

        if self.drones:
            for drone in self.drones:
                self.w.delete(drone)
                self.master.update_idletasks()



        # Draw new robots
        self.drones = [] ######################
        for drone in drones:
            pos = drone.get_drone_position()
            #print(pos)
            x, y = pos.get_x(), pos.get_y()
            x1, y1 = self._map_coords(x - .08, y - .08)
            x2, y2 = self._map_coords(x + .08, y + .08)
            self.drones.append(self.w.create_oval(x1, y1, x2, y2, fill="black"))
            self.drones.append(self._draw_robot(drone.get_drone_position(), drone.get_drone_direction()))
            #print(self.drones)
        # Update text
        self.w.delete(self.text)
        self.time += 1
        self.text = self.w.create_text(25, 0, anchor=NW, text=self._status_string(self.time, 0, 1))

        self.master.update()
        t.sleep(self.delay)
        #print("end")




    def done(self):
        "Indicate that the animation is done so that we allow the user to close the window."
        mainloop()




class DialogBox:

    def __init__(self):
        self.master1 = Tk()

        ##Init Var types
        self.e1Var = StringVar(self.master1)
        self.e2Var = StringVar(self.master1)
        self.e3Var = StringVar(self.master1)
        self.e4Var = StringVar(self.master1)
        self.e5Var = StringVar(self.master1)
        self.e6Var = StringVar(self.master1)

        self.s1Var = DoubleVar(self.master1)  ###DoubleVar
        self.s2Var = DoubleVar(self.master1)  ###DoubleVar

        self.o0Var = StringVar(self.master1)
        self.o1Var = StringVar(self.master1)  ###DoubleVar
        self.o2Var = StringVar(self.master1)  ###DoubleVar

        #self.bar = Progressbar(self.master1, length=100) ####Move to animation window, or third window with flight stats???
        #self.bar['value'] = 60
        #self.bar.grid(row=0, column=1)
        # self.bar.pack()


        #WSNS Params

        #self.e1 = Entry(self.master1, textvariable=self.e1Var).grid(row = 2, column = 1, pady = 2)
        #self.e2 = Entry(self.master1, textvariable=self.e2Var).grid(row = 4, column = 1, pady = 2)

        self.l0 = Label(self.master1, text="1) WSN Vars", font = ("Ariel",15, 'bold')).grid(row = 0, column = 0)

        self.options0 = [x for x in range(len(NETWORKS))] #["SimpleNetwork", "StandardNetwork", "ComplexNetwork"]
        self.o0 = OptionMenu(self.master1, self.o0Var, *self.options0).grid(row=1, column=1) #
        self.l1 = Label(self.master1, text="Network Type").grid(row = 1, column = 0)

        #self.l2 = Label(self.master1, text="Cell Loc (x,y)").grid(row = 2, column = 0)
        #self.l4 = Label(self.master1, text="B.S Loc (x,y)").grid(row = 4, column = 0)


        #self.l3 = Label(self.master1, text="Cell Radius (km)").grid(row = 3, column = 0)#
        #self.s1 = Scale(self.master1, from_=1, to=5, orient=HORIZONTAL, variable=self.s1Var).grid(row = 3, column = 1)


        ###Drone Parameters


        self.l5 = Label(self.master1, text="Drone Type").grid(row = 1, column = 2)

        self.options1 =  [x for x in range(len(DRONES))] #["CheapDrone", "StandardDrone", "ExpensiveDrone"]
        self.o1 = OptionMenu(self.master1, self.o1Var, *self.options1).grid(row = 1, column = 3)

        self.l6 = Label(self.master1, text="Flight Path").grid(row = 2, column = 2)
        self.options2 = ["1) Travel to waypoints", "2) Random Walk", "3) Hover at Waypoints"]
        self.o2 = OptionMenu(self.master1, self.o2Var, *self.options2).grid(row = 2, column = 3)

        self.l7 = Label(self.master1, text=" # of Drones").grid(row = 3, column = 2)
        self.s2 = Scale(self.master1, from_=1, to=5, orient=HORIZONTAL, variable=self.s2Var).grid(row = 3, column = 3)


        ###Weather Parameters

        #self.l11 = Label(self.master1, text="Air Density ").grid(row = 2, column = 4)
        self.l12 = Label(self.master1, text="Wind Speed, Direction").grid(row=1, column=4)
        #self.l13 = Label(self.master1, text="Temp (C) ").grid(row=3, column=4)
        #self.l14 = Label(self.master1, text="Rainfall % ").grid(row=4, column=4)

        self.e3 = Entry(self.master1, textvariable=self.e3Var).grid(row=1, column=5, pady=2)
        #self.e4 = Entry(self.master1, textvariable=self.e3Var).grid(row=2, column=5, pady=2)
        #self.e5 = Entry(self.master1, textvariable=self.e3Var).grid(row=3, column=5, pady=2)
        #self.e6 = Entry(self.master1, textvariable=self.e3Var).grid(row=4, column=5, pady=2)


        self.l8 = Label(self.master1, text = "2) Drone Vars" , font = ("Ariel",15, 'bold')).grid(row = 0, column = 2)
        self.l9 = Label(self.master1, text="3) Weather Vars" , font = ("Ariel",15, 'bold')).grid(row=0, column=4)

        self.l10 = Label(self.master1, text="4) Start Simulation",  font = ("Ariel",15, 'bold')).grid(row=0, column=6)




        def saveVars():
            """"""
            print("Instantiating inputs")

            #cellLoc = self.e1Var.get()
            #BSLoc = self.e2Var.get()
            r = self.s1Var.get()
            networkT = self.o0Var.get()

            droneT = self.o1Var.get()
            flightP = self.o2Var.get()
            numDrones = self.s2Var.get()


            #temp1 = cellLoc.split(",")
            #temp2 = BSLoc.split(",")

            #center = (int(temp1[0]), int(temp1[1]))
            #BS = (int(temp2[0]), int(temp2[1]))



            #print([, BSLoc], r, droneT, networkT, flightP, numDrones)

            print("New simulation starting ... ")
            network = NETWORKS[int(networkT)]

            print(numDrones)

            drones = [DRONES[int(droneT)] for x in range(int(numDrones))] #####MULTIPLE DRONES FROM .TXT

            tempx = network.BS[0]
            tempy = network.BS[1]

            for drone in drones:
                drone.set_drone_position(Position(tempx, tempy))


            weather = Weather(16,25.6,(0,0),0)

            print(network)
            print(drones)


            if flightP[0] == '1':
                #Travel to waypoint
                pass

            elif flightP[0] == '2':
                test_random_mov(drones, network)
            elif flightP[0] == '3':
                pass


            #print(drone_class)

            #weather = Weather(0,0,(5,270),0) ###get vars
            #flightP = "1"
            #travel(drone, network, weather, flightP)

        self.save = Button(self.master1, text="SAVE", width=25, command=saveVars).grid(row = 0, column = 7)  ###Command = some function

        self.master1.update()

        self.master1.mainloop()



################### Movement


def test_drone_movement(drones, network_type):

    # # room_type(2000, 1000, [(0,250),(1000,250),(1500,1750)] ) #2000, 1000, [(0,250),(1000,250),(1500,1750)]
    network = network_type #[robot_type("DJJ_Mini_2",room_type,2250,15, .250, .30)]

    xBound = network.width
    yBound = network.length
    r = network.radius

    coverage = 0
    time_steps = 0
    min_coverage = 1.0
    anim = DroneVisualization(len(drones), xBound, yBound, r, network)

   #print("in here")
    #print(robots[0].position)
    #print(robots[0].direction)

    while time_steps < 100: #coverage < min_coverage
        time_steps += 1
        for drone in drones:
            drone.set_rand_direction()
            for i in range(10):
                drone.update_position_noWind()
                #print(robot.position)
                anim.update(network, drones)
        t.sleep(5)
        print("Hovering for 5 sec")
                #coverage = float(room.get_num_cleaned_tiles())/room.get_num_tiles()

    anim.done()


def test_model1(drones,network):
    print("testing")
    #print(network.network)

    #drones = [drone]  # room_type(2000, 1000, [(0,250),(1000,250),(1500,1750)] ) #2000, 1000, [(0,250),(1000,250),(1500,1750)]
    #[robot_type("DJJ_Mini_2",room_type,2250,15, .250, .30)]
    xBound = network.width
    yBound = network.length
    r = network.radius

    anim = DroneVisualization(1, xBound, yBound, r, network) ##Make sure mapping is correct

    BS = network.BS
    C = network.C

    for waypoint in network.nodes:
        #for drone in drones:

        #print("WAYpoint", waypoint)
        temp = drones[0].get_drone_position()

        currPos = (temp.get_x(),temp.get_y())

        dist = calculate_distance(currPos, waypoint)
        time = int(dist/drones[0].speed)

        #print("flying to", str(waypoint))

        for i in range(time):
            for drone in drones:
                drone.travel_to_location(currPos, waypoint)
                anim.update(network, drones)

        #print("hovering")
        #t.sleep(5)

    #EC = calculate_EC_steady1_DRAG(drone, network, weather) ###Calculations with multiple drones?
    #print(EC)

    anim.done()



def test_random_mov(drones, network):
    """
    If drone hits edge, rotate b/w x-y degrees
    """


    network = network  # [robot_type("DJJ_Mini_2",room_type,2250,15, .250, .30)]

    #BS = network.BS
    #C = network.C




    xBound = network.width
    yBound = network.length
    r = network.radius

    coverage = 0
    time_steps = 0
    min_coverage = 1.0
    anim = DroneVisualization(len(drones), xBound, yBound, r, network)


    #print("Drone direction", print(drone.direction))


    ##Travel to WSN


    dist = calculate_distance(network.BS, network.C)
    time = int(dist / drones[0].speed)

    # print("flying to", str(waypoint))

    for i in range(time):

        for drone in drones:
            #print(drone)
            drone.travel_to_location(network.BS, network.C)
            anim.update(network, drones)



    ##Fly randomly in WSN


    energy = 0 ##Get curent drone energy
    safety_factor = 0 #distance needed to return to BS ?

    fly = True


    while fly:

        interval = random.randrange(5,15,1)

        for drone in drones:
            drone.set_rand_direction()

        for i in range(interval):

            for drone in drones:


                newPos = drone.position.get_new_position(drone.direction, drone.speed)
                #drone.update_position_noWind()
                WSN_boundary = network.is_pos_in_cell(newPos)
                cell_boundary = network.is_pos_in_boundary(newPos)

                # edge = drone.check_edge()
                #if edge == True:

                    #drone.set_rand_direction()
                    #print("Hit edge... Re directing")
                    #edge = False

                if WSN_boundary == False:
                    #drone.set_rand_direction()
                    #newPos = drone.position.get_new_position(drone.direction, drone.speed)

                    pos = drone.get_drone_position()

                    drone.travel_to_location((pos.get_x(),pos.get_y()), network.C)
                    #anim.update(network, drones)

                    print("going to center")


                elif cell_boundary == False:
                    fly = False
                    break
                #elif energy < safety_factor:

                    #print("Drone reached minimum battery capacity ... to return to BS??")
                    #fly = False

                else:
                    drone.set_drone_position(drone.position.get_new_position(drone.direction, drone.speed))
                    anim.update(network, drones)


    anim.done()
    pass

