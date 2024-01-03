# Project Name: One Dimensional Friction
# Project ID  : S-KIN-OneDimFriction
#   Description : This code analyzes and plots a system where a point spherical object performs a 1D motion in the presence of gravity with air friction considered.
#   The velocity and height are plotted. The assumption is that the body of the falling object can be thought of as a sphere.
#
#   (i) Configuration variables can be found at the bottom of this file.
#

import math
import matplotlib.pyplot as plt

def GenerateTime(timeLimit:float, timeInterval:float):
    """
    Generate a list of time values within a specified time limit and interval.

    Parameters:
    - timeLimit: Maximum time limit.
    - timeInterval: Time interval between values.

    Returns:
    - List of time values.
    """

    t = []
    for i in range(int(timeLimit / timeInterval)):
        t.append(i*timeInterval)

    return t

def SparseArray(array):
    """
    Create a sparse array by removing consecutive duplicate elements from the given array.

    Parameters:
    - array: Input array from which to generate the sparse array.

    Returns:
    - Sparse array containing only non-consecutive duplicate elements.
    """

    sparse_array = []
    for i in range(len(array)-1):
        if (array[i] != array[i+1]):
            sparse_array.append(array[i])

    return sparse_array

def WriteToFile(dataX, dataY, dataZ, filePath):
    """
    Write X-Y paired data to the given filepath.

    Parameters:
    - dataX (list): Data which includes X.
    - dataY (list): Data which includes Y.
    - dataZ (list): Data which includes Z.
    - filePath (str): Filepath to write.

    Returns:
    - int: Return 0 if succeeded.
    """

    with open(filePath, 'w') as file:
        for x, y, z in zip(dataX, dataY, dataZ):
            file.write(f"{x}\t{y}\t{z}\n")

    return 0



def main(INITIAL_VELOCITY, INITIAL_POSITION, GRAVITY, AIR_DENSITY, OBJECT_FRONT_RADIUS, DRAG_COEFFICIENT, OBJECT_MASS, TIME_INTERVAL, TIME_LIMIT, GRID, TITLE):

    # Config variable check
    if (INITIAL_POSITION == 0):
        print("ERROR: Initial position cannot be zero")
        return 1

    # Drag constant that comes from the formula
    drag_constant = 0.5 * AIR_DENSITY * 4*math.pi*OBJECT_FRONT_RADIUS**2 * DRAG_COEFFICIENT
    # Number of steps to analyze the system for maximum number of try
    number_of_steps = int(TIME_LIMIT / TIME_INTERVAL)
    # Calculate termina velocity
    terminal_velocity = math.sqrt(OBJECT_MASS * GRAVITY / drag_constant)

    # Initialize components
    acceleration = [0]*number_of_steps
    velocity = [0]*number_of_steps
    position = [0]*number_of_steps
    acceleration[0] = -GRAVITY - drag_constant * INITIAL_VELOCITY**2 / OBJECT_MASS
    velocity[0] = INITIAL_VELOCITY
    position[0] = INITIAL_POSITION

    # Fill the components with systemmaticly fit values
    for i in range(number_of_steps-1):
        drag_direction = 1 if velocity[i] < 0 else -1
        position[i+1] = position[i] + velocity[i] * TIME_INTERVAL + acceleration[i] * TIME_INTERVAL**2 / 2
        velocity[i+1] = (velocity[i] + acceleration[i] * TIME_INTERVAL)
        acceleration[i+1] = ((-GRAVITY + (drag_constant * velocity[i]**2 * drag_direction / OBJECT_MASS)) if velocity[i] > -terminal_velocity else 0) if INITIAL_VELOCITY > 0 else ((-GRAVITY + (drag_constant * velocity[i]**2 * drag_direction / OBJECT_MASS)) if velocity[i] < -terminal_velocity else 0)
        if ((INITIAL_POSITION > 0 and position[i+1] < 0) or (INITIAL_POSITION < 0 and position[i+1] > 0)):
            break

    # Sparse all arrays of compenents
    position_to_plot = SparseArray(position)
    velocity_to_plot = SparseArray(velocity)
    time_velocity = GenerateTime(len(velocity_to_plot)*TIME_INTERVAL, TIME_INTERVAL)
    time_position = GenerateTime(len(position_to_plot)*TIME_INTERVAL, TIME_INTERVAL)

    WriteToFile(time_position, position_to_plot, velocity_to_plot, "S-fric1D.dat")

    # Plots
    plt.plot(time_position, position_to_plot, label="Height $[m]$")
    plt.plot(time_velocity, velocity_to_plot, label="Velocity $[m/s]$")
    plt.xlabel("Time [s]")
    plt.legend()
    plt.grid(GRID)
    plt.title(TITLE)
    plt.figtext(0.5, 0.04, f"Terminal Velocity: {terminal_velocity} m/s", fontsize=12, ha='center', va='center')
    plt.show()


    return 0


if __name__ == "__main__":

    # Assuming the 1D point particle can be thought of as a spherical body...
    INITIAL_VELOCITY = 20                                   # (m/s)
    INITIAL_POSITION = 30                                   # (m)
    GRAVITY = 9.81                                          # Gravitational acceleration g (m/s^2)
    AIR_DENSITY = 1.204                                     # kg/m^3
    OBJECT_FRONT_RADIUS = .5                                # Radius of the spherical object (m)
    DRAG_COEFFICIENT = 0.47                                 # Coefficient of drag
    OBJECT_MASS = 10                                        # Mass of the object (kg)
    TIME_INTERVAL = 0.01                                    # The time interval from zero to TIME_LIMIT, higher values result in lower quality with high performance (s)
    TIME_LIMIT = 20                                         # To what extent the time should be considered
    GRID = False                                            # Enable grid for plots
    TITLE = "Velocity and Position with Quadratic Drag"     # Title of the plot


    #
    # Main Function
    #
    if main(INITIAL_VELOCITY, INITIAL_POSITION, GRAVITY, AIR_DENSITY, OBJECT_FRONT_RADIUS, DRAG_COEFFICIENT, OBJECT_MASS, TIME_INTERVAL, TIME_LIMIT, GRID, TITLE):
        exit(1)
    else:
        exit(0)
