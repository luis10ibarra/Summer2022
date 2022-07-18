import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

import math
import time as t
import base64
from tkinter import *
from tkinter.ttk import Progressbar
from urllib.request import urlopen
import numpy as np

#from Classes import *

#from Classes import Drone

from main import *

import os





###Visual for Cost of UAV travel b/w nodes

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

        self.e1 = Entry(self.master1, textvariable=self.e1Var).grid(row = 2, column = 1, pady = 2)
        self.e2 = Entry(self.master1, textvariable=self.e2Var).grid(row = 4, column = 1, pady = 2)

        self.l0 = Label(self.master1, text="1) WSN Vars", font = ("Ariel",15, 'bold')).grid(row = 0, column = 0)

        self.options0 = ["SimpleNetwork", "StandardNetwork", "ComplexNetwork"]
        self.o0 = OptionMenu(self.master1, self.o0Var, *self.options0).grid(row=1, column=1) #
        self.l1 = Label(self.master1, text="Network Type").grid(row = 1, column = 0)

        self.l2 = Label(self.master1, text="Cell Loc (x,y)").grid(row = 2, column = 0)
        self.l4 = Label(self.master1, text="B.S Loc (x,y)").grid(row = 4, column = 0)


        self.l3 = Label(self.master1, text="Cell Radius (km)").grid(row = 3, column = 0)#
        self.s1 = Scale(self.master1, from_=1, to=5, orient=HORIZONTAL, variable=self.s1Var).grid(row = 3, column = 1)


        ###Drone Parameters


        self.l5 = Label(self.master1, text="Drone Type").grid(row = 1, column = 2)
        self.options1 = ["CheapDrone", "StandardDrone", "ExpensiveDrone"]
        self.o1 = OptionMenu(self.master1, self.o1Var, *self.options1).grid(row = 1, column = 3)

        self.l6 = Label(self.master1, text="Flight Path").grid(row = 2, column = 2)
        self.options2 = ["Hover at Center", "Random Walk", "Hover at Waypoints",  "Random Walk w/ obstacles"]
        self.o2 = OptionMenu(self.master1, self.o2Var, *self.options2).grid(row = 2, column = 3)

        self.l7 = Label(self.master1, text=" # of Drones").grid(row = 3, column = 2)
        self.s2 = Scale(self.master1, from_=1, to=5, orient=HORIZONTAL, variable=self.s2Var).grid(row = 3, column = 3)


        ###Weather Parameters

        self.l11 = Label(self.master1, text="Air Density ").grid(row = 1, column = 4)
        self.l12 = Label(self.master1, text="Wind Speed, Direction").grid(row=2, column=4)
        self.l13 = Label(self.master1, text="Temp (C) ").grid(row=3, column=4)
        self.l14 = Label(self.master1, text="Rainfall % ").grid(row=4, column=4)

        self.e3 = Entry(self.master1, textvariable=self.e3Var).grid(row=1, column=5, pady=2)
        self.e4 = Entry(self.master1, textvariable=self.e3Var).grid(row=2, column=5, pady=2)
        self.e5 = Entry(self.master1, textvariable=self.e3Var).grid(row=3, column=5, pady=2)
        self.e6 = Entry(self.master1, textvariable=self.e3Var).grid(row=4, column=5, pady=2)


        self.l8 = Label(self.master1, text = "2) Drone Vars" , font = ("Ariel",15, 'bold')).grid(row = 0, column = 2)
        self.l9 = Label(self.master1, text="3) Weather Vars" , font = ("Ariel",15, 'bold')).grid(row=0, column=4)

        self.l10 = Label(self.master1, text="4) Start Simulation",  font = ("Ariel",15, 'bold')).grid(row=0, column=6)




        def saveVars():
            """"""
            print("Instantiating inputs")

            cellLoc = self.e1Var.get()
            BSLoc = self.e2Var.get()
            r = self.s1Var.get()

            droneT = self.o1Var.get()
            flightP = self.o2Var.get()
            numDrones = self.s2Var.get()

            networkT = self.o0Var.get()

            self.center = cellLoc

            print([cellLoc, BSLoc], r, droneT, networkT, flightP, numDrones)

            print("New simulation starting ... ")

            #drone_class = StandardDrone(2000, 2000, 2, [(500,250),(500,600),(750,750),(1600,1300),(500,250)])
            #print(drone_class)
            #network = SimpleNetwork(1000, 1000, r, [BSLoc, cellLoc])
            #weather = Weather(0,0,(5,270),0) ###get vars
            #flightP = "1"
            #travel(drone, network, weather, flightP)

        self.save = Button(self.master1, text="SAVE", width=25, command=saveVars).grid(row = 0, column = 7)  ###Command = some function

        self.master1.update()

        self.master1.mainloop()


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



def test_max_distance(drone, network, weather):
    """
    Return the max distance a drone can travel under given conditions
    """
    X = []
    Y = []

    for z in range(1000,1001):
        print(z)
        tempx, tempy = calculate_EC_steady1(drone, network, z)
        #time = round((x/drone.speed)/60,2) #minutes
        #time = round((x / drone.speed), 2)  #seconds
        if tempy < 0:
            print("Max Distance: ", z)
            print("Max time: ", tempx)

            return(drone.name, tempx/60)
        #X.append(int(tempx))
        #Y.append(int(tempy))

    #plt.plot(X,Y)
    #plt.show()



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
                #coverage = float(room.get_num_cleaned_tiles())/room.get_num_tiles()

    anim.done()


def test_model1(drone,network, weather):
    print("testing")
    #print(network.network)

    drones = [drone]  # room_type(2000, 1000, [(0,250),(1000,250),(1500,1750)] ) #2000, 1000, [(0,250),(1000,250),(1500,1750)]
    #[robot_type("DJJ_Mini_2",room_type,2250,15, .250, .30)]
    xBound = network.width
    yBound = network.length
    r = network.radius

    anim = DroneVisualization(1, xBound, yBound, r, network) ##Make sure mapping is correct

    BS = network.BS
    C = network.C

    for waypoint in network.nodes:
        #print("WAYpoint", waypoint)
        temp = drone.get_drone_position()

        currPos = (temp.get_x(),temp.get_y())

        dist = calculate_distance(currPos, waypoint)
        time = int(dist/drone.speed)

        #print("flying to", str(waypoint))

        for i in range(time):

            drone.travel_to_location(currPos, waypoint)
            anim.update(network, drones)

        #print("hovering")
        #t.sleep(5)

    EC = calculate_EC_steady1(drone, network, weather)
    #print(EC)

    anim.done()



