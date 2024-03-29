from classes import *
#from visualization import * 


#import matplotlib.pyplot as plt

def calculate_distance(loc1,loc2):
    """
    Currently calculating straight line distance between two points
    #eventually include the estimate for curvature of earth (6.009 pset)

    :param loc1: Tuple (x1, y1)
    :param loc2: Tuple (x2, y2)
    :return: dist: Float
    """

    x1, y1 = loc1
    x2, y2 = loc2

    return round(math.sqrt((x2-x1)**2 + (y2-y1)**2), 2)


def calculate_EC_steady1(drone, network, weather, d = None):
    """
    D'Andrea (2014)

    Simplification: Thrust = Weight = (mass * 9.81) / L/D Ratio

    ###Wind & w/o Wind, depending on parameters in weather class

    :param drone: class obj
    :param network: class obj
    :param weather: class obj
    :param d: int (distance drone traveled, if d = None then max distance is calculated)
    :return: EnergyConsumption: Float
    """

    baseStation = network.BS
    nodes = network.nodes

    print("---------------------------------------------------")


    if d == None:
        d = calculate_distance(baseStation, nodes[0])


    #dist2 = calculate_distance(nodes[0], nodes[1])
    #print("Drone travels ", dist2, "meters from ", str(nodes[0]), " to ", str(nodes[1]))

    #dist3 = calculate_distance(nodes[1], baseStation)
    #print("Drone travels ", dist3, "meters from ", str(nodes[1]), " to ", baseStation)

    totalDistance = d * 2 # Flight to center and back
    print("Drone travels ", totalDistance, "meters from ", baseStation, " to ", str(nodes[0]), "and back.")



    thrust = round((drone.weight * 9.801) / drone.L_D, 2)


    energy = round((thrust * totalDistance)/3600, 2) ##In Joules, kgm^2/s^2 ->> Wh
    #energy = (drone.weight * drone.speed) / (370 * drone.L_D*.8)


    if drone.get_drone_name() == "EVO II Pro":
        remainingCapacity = (drone.battery - 1000*energy/ 11.1  ) #In mAh ###2s,##### 3S !
    else:
        remainingCapacity = (drone.battery - 1000 * energy / 7.4)

    print("---------------------------------")
    print(thrust, "Newtons of thrust needed to fly")

    rel_speed = drone.speed - weather.wind_s

    ###Take into consideration the direction of the drone
    print("Drone flying at rel vel. ", rel_speed, "m/s due to wind of", weather.wind_s, "m/s")

    time = round(totalDistance/rel_speed/60,2)
    print(energy, "Wh lost and would take ", time," minutes cruising in flight.")

    print("drone battery remaining : ", round(remainingCapacity, 2) , "mAh")


    return(d, remainingCapacity)






def calculate_EC_steady2(drone, network, weather, d=None):
    """
    D'Andrea (2014)

    Simplification: Thrust = Weight = (mass * 9.81) / L/D Ratio * (1/omega)

    ###Wind * w/o Wind

    :param drone: class obj
    :param network: class obj
    :param weather: class obj
    :param d: int (distance drone traveled, if d = None then max distance is calculated)

    :return: remaining Energy Capacity: (d, EC) Tuple
    """

    baseStation = network.BS
    # drone.position = Position(baseStation[0], baseStation[1])
    nodes = network.nodes

    print("---------------------------------------------------")

    if d == None:
        d = calculate_distance(baseStation, nodes[0])


    totalDistance = d  # * 2 # Flight there and back
    print("Drone travels ", totalDistance, "meters from ", baseStation, " to ", str(nodes[0]), "and back.")

    thrust = (1/1-(weather.wind_s/drone.speed)) * (drone.weight * 9.801) / drone.L_D

    energy = round((thrust * totalDistance) / 3600, 2)  ##In Joules, kgm^2/s^2 ->> Wh
    # energy = (drone.weight * drone.speed) / (370 * drone.L_D*.8)

    if drone.get_drone_name() == "EVO II Pro":
        remainingCapacity = (drone.battery - 1000 * energy / 11.1)  # In mAh ###2s,##### 3S !
    else:
        remainingCapacity = (drone.battery - 1000 * energy / 7.4)

    print("---------------------------------")
    print(thrust, "Newtons of thrust needed to fly w/o wind")

    time = round(totalDistance / drone.speed / 60, 2)
    print(energy, "Wh lost and would take ", time, " minutes cruising in flight.")

    print("drone battery remaining : ", round(remainingCapacity, 2), "mAh")

    return (d, remainingCapacity)


def calculate_EC_hover(drone,network,weather, t = None):
    """

    Hasini et al. (2007)

    Simplifications: P = (m*g)**3/2 / (v * sqrt(2*n*rho*c)

    :param drone: class obj
    :param network: class obj
    :param weather: class obj
    :param t: int (time)
    :return: remaining Energy Capacity: (d, EC) Tuple
    """

    P = (drone.weight*9.801)**(3/2) * (1/(2*3.14*weather.p*.0508*.0508)**(1/2)) ###r = 2 in.
    E = 7.4 * drone.battery * 3600 / 1000

    print(P)
    if t == None:
        #Calculate max hover time given conditions

        t = round(E/P)
        print("Max time, ", t)

    energy = P*t

    remainingCapacity = (drone.battery - energy / 7.4)  # In mAh ###2s,
    return (t, remainingCapacity)



def calculate_EC_DRAG(drone,network, d = None):
    """
    Uses (D'Andrea 2014) model as well as parasitic drag formula 1/2 * p * C_d * A * v^2


    :param drone: class obj
    :param network: class obj
    :param d: int (distance drone traveled, if d = None then max distance is calculated)
    """

    #print("calculating drag")

    baseStation = network.BS #network.network[0]
    nodes = network.nodes[1:]

    #print("---------------------------------------------------")

    #dist1 = calculate_distance(baseStation, nodes[0])
    #totalDistance = int(dist1 * 2)  # Flight there and back
    #print("Drone travels ", totalDistance, "meters from ", baseStation, " to ", str(nodes[0]), "and back.")


    thrust = round( ((drone.weight * 9.801)/drone.L_D + .5*1.225*drone.c* drone.A*drone.speed*drone.speed), 2)

    if d == None:
        d = calculate_distance(baseStation, nodes[0])

    energy = round((thrust * d) / 3600, 2)  ##In Joules, kgm^2/s^2 ->> Wh
    remainingCapacity = (drone.battery - 1000 * energy / 7.4)  # In mAh ###2s,

    #print("---------------------------------")
    #print(thrust, "Newtons of thrust needed to fly with drag")

    time = round(d / drone.speed / 60, 2)
    #print(energy, "Wh lost and would take ", time, " minutes cruising in flight.")

    #print("drone battery remaining : ", round(remainingCapacity, 2), "mAh")

    return(d, remainingCapacity)

    #x = [i for i in range(totalDistance)]
    #y = [thrust * i for i in range(totalDistance)]

    #plt.plot(x,y)
    #plt.show()



def calculate_EC_STAGES(drone,network):
    """
    #Breaking down EC into the 4 (or 3) dif. stages of flight
    #4 stages of flight: Takeoff, hover, steady, land
    + communications (FUTURE?)
    """
    return None





def test_collision(drone,network):
    """
    Function used to test the WSN boundaries and ensure drones are moving correctly
    """

    BS = network.BS
    x1 = BS[0]
    y1 = BS[1]

    print(x1, y1)

    drone.set_drone_position(Position(x1, y1))

    test_random_mov(drone, network)



def travel(drones, network, weather, movement):
    """

    Run the simulation that will show the drones flight path in the WSN

    :param drone: class obj
    :param network: class obj
    :param weather: class obj
    :param movement: movement type
    :return: None
    """


    BS = network.BS
    x1 = BS[0]
    y1 = BS[1]

    #print(x1, y1)

      # room_type(2000, 1000, [(0,250),(1000,250),(1500,1750)] ) #2000, 1000, [(0,250),(1000,250),(1500,1750)]
    #print(drones)
    #for d in drones:
        #d.set_drone_position(Position(x1, y1))


    if movement == "1": ###Waypoint Travel
        print("here")
        #test_model1(drones,network, weather) ##only works with one drone for now

    if movement == "2": ###Random mov 1st (then random mov in wsn)
        test_random_mov(drones, network)
        pass

    if movement == "3":  ###hover?
        test_drone_movement(drones, network)




def GUI(defaultNetwork):
    """
    Opens up GUI given default network
    """
    #width = int(input("input GUI Width:"))
    #length = int(input("input GUI Length:"))

    screen1 = DialogBox()


    #anim = DroneVisualization(0, 500, 500, 0, defaultNetwork)
    #anim.done()








def run_simulation(num_drones, drone_type, speed, width, height, num_trials):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room.

    The simulation is run with num_robots robots of type robot_type, each
    with the input speed and capacity in a room of dimensions width x height
    with the dirt dirt_amount on each tile. Each trial is run in its own SimpleRoom
    with its own robots.

    num_drones:  int ( > 0)
    drone_type: class of robot to be instantiated (i.e. Cheap, Standard, Expensive)

    speed: float (> 0)
    width: int (> 0)
    height: int (> 0)

    num_trials: int ( > 0)

    """

    timeSteps = []
    totalTimeSteps = 0
    meanTimeSteps = 0

    for trial in range(num_trials):

        network = SimpleNetwork(width, height, 1, [(0,250), (500,500)])  # instantiating room
        #drones = [StandardDrone("name", network, 2250, 15, .5, .7, 1.1, .3) for x in range(num_drones)]  # list of robot objects

        BS = network.BS
        x1 = BS[0]
        y1 = BS[1]
        for drone in drones:
            drone.set_drone_position(Position(x1, y1))


        #anim = DroneVisualization()

        numSteps = 0

        for i in range(75): ###While Drones have enough energy
            ###Right now will be an INFINITE loop

            for drone in drones:  # each robot goes through one step
                drone.set_rand_direction()
                for i in range(5):
                    drone.update_position_noWind()

            numSteps += 1

        timeSteps.append(numSteps)  # adds the number of steps for each trial

    # calculating average number of timeSteps
    for t in timeSteps:
        totalTimeSteps += t
    meanTimeSteps = totalTimeSteps / num_trials

    return meanTimeSteps



def show_environment(wsn, drone, weather, metric = True): 

    print('Simulating Environment in metric: ', metric) 
    wsn.show_info() 
    drone.show_info()
    weather.show_info() 




    pass 






if __name__ == '__main__':

    network1 = WSN(2000,2000,50, [(500,250),(1400,1100),(750,750),(1600,1300),(500,250)]) 
    drone1 = Drone("DJJ_Mini_2",network1, 2250, 15, .250, .75, .82, .016)
    weather1 = Weather(16,25.6,(5,270),0)

    show_environment(network1,drone1,weather1, True)
    


    #Travel time with no weather. Max Distance based on dif models 

    #Travel time with no weather, multi stage / Drone.state == 

    #Travel time with Randomness (Weather (gusts), Movement (monte carlo)) 


    #Visualization, GUI? 








    #defaultNetwork = SimpleNetwork(2000, 2000,3, [(0,0),(0,0)])
    #simpleNetwork = SimpleNetwork(2000, 2000, 500, [(500,250),(1400,1100),(750,750),(1600,1300),(500,250)])

    #drone1 = StandardDrone("DJJ_Mini_2",simpleNetwork, 2250, 15, .250, .75, .82, .016)
    #drone2 = StandardDrone("DJJ_MavicAir_2", simpleNetwork, 3500, 15, .570, .75, .82, .0195)
    #drone3 = StandardDrone("EVO II Pro", simpleNetwork, 7100, 15, 1.174, .75, .82, .195)
    #droneFAST = StandardDrone("DJJ_Mini_2", simpleNetwork, 2250, 60, .250, .75, .82, .016)

    #weather_noWind = Weather(16,25.6,(0,0),0)
    #weather_wind = Weather(16,25.6,(5,270),0)



    #GUI(defaultNetwork)


    #run_simulation(2, "Type", 15,1000,1000,1)


    #travel(droneFAST,simpleNetwork, weather_noWind, "2")
    #print("Done")

    #drones = [StandardDrone("DJJ_Mini_2",simpleNetwork, 2250, 70, .250, .75, .82, .016) for x in range(5)]

    #travel(drones, simpleNetwork, weather_noWind, "2")

    #GUI(defaultNetwork)

    #test_collision(droneFAST, simpleNetwork)


    #calculate_EC_steady1(drone1, simpleNetwork)
    #calculate_EC_steady2()
    #calculate_EC_DRAG(drone1, simpleNetwork)
    #calculate_EC_hover(drone1, simpleNetwork)





    ###########
    ####TEST GRAPHS
    #############



    #drones = [drone1, drone2, drone3]
    
    
    #for drone in drones:
        #x = []
        #y = []
        

        #for speed in range(5, 25):
            #drone.set_drone_speed(speed)
        #tempx, tempy = test_max_distance(drone, simpleNetwork, weather)
        #x.append(tempx)
        #y.append(tempy)

        #plt.scatter(x,y, label = drone.get_drone_name())
    #plt.legend()
    #plt.ylabel("Max hover time (min)")
    #plt.xlabel("Drone Type")

    #plt.show()


    ##Travel max distance, then get graphs on drones at dif speeds ... then with multiple drones ... then under dif weather conditions.