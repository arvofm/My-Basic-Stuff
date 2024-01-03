# Project Name: Two Dimensional Friction
# Project ID  : S-Friction2
#   Description : This code analyzes and plots a system where an object performs a 2D motion in the presence of gravity with air friction considered.
#   The position is plotted. The assumption is that the body of the falling object can be thought of as a sphere.
#
#   (i) Configuration variables can be found at the bottom of this file.
#

import math
import matplotlib.pyplot as plt

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

def WriteToFile(dataX, dataY, filePath):
    """
    Write X-Y paired data to the given filepath.

    Parameters:
    - dataX (list): Data which includes X.
    - dataY (list): Data which includes Y.
    - filePath (str): Filepath to write.

    Returns:
    - int: Return 0 if succeeded.
    """

    with open(filePath, 'w') as file:
        for x, y in zip(dataX, dataY):
            file.write(f"{x}\t{y}\n")

    return 0


def main(INITIAL_VELOCITY, INITIAL_HEIGHT, GRAVITY, AIR_DENSITY, OBJECT_FRONT_RADIUS, DRAG_COEFFICIENT, OBJECT_MASS, TIME_INTERVAL, TIME_LIMIT, GRID, TITLE, LAUNCH_ANGLE):

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
    LAUNCH_ANGLE = math.radians(LAUNCH_ANGLE)

    # Initialize components
    accelerationY = [0]*number_of_steps
    accelerationX = [0]*number_of_steps
    velocityX = [0]*number_of_steps
    velocityY = [0]*number_of_steps
    positionX = [0]*number_of_steps
    positionY = [0]*number_of_steps
    accelerationY[0] = -GRAVITY - drag_constant * INITIAL_VELOCITY**2 / OBJECT_MASS
    velocityX[0] = INITIAL_VELOCITY*math.cos(LAUNCH_ANGLE)
    velocityY[0] = INITIAL_VELOCITY*math.sin(LAUNCH_ANGLE)
    positionY[0] = INITIAL_HEIGHT
    positionX[0] = 0

    # Fill the components with systemmaticly fit values
    for i in range(number_of_steps-1):
        drag_direction = 1 if velocityY[i] < 0 else -1
        positionY[i+1] = positionY[i] + velocityY[i] * TIME_INTERVAL + accelerationY[i] * TIME_INTERVAL**2 / 2
        positionX[i+1] = positionX[i] + velocityX[i] * TIME_INTERVAL + accelerationX[i] * TIME_INTERVAL**2 / 2
        velocityY[i+1] = (velocityY[i] + accelerationY[i] * TIME_INTERVAL)
        velocityX[i+1] = (velocityX[i] + accelerationX[i] * TIME_INTERVAL)
        accelerationY[i+1] = ((-GRAVITY + (drag_constant * velocityY[i]**2 * drag_direction / OBJECT_MASS)) if velocityY[i] > -terminal_velocity else 0) if INITIAL_VELOCITY > 0 else ((-GRAVITY + (drag_constant * velocityY[i]**2 * drag_direction / OBJECT_MASS)) if velocityY[i] < -terminal_velocity else 0)
        accelerationX[i+1] = (drag_constant * math.pow(velocityX[i], 2)  * drag_direction / OBJECT_MASS) if velocityX[i] < terminal_velocity else accelerationX[i]
        if (INITIAL_POSITION > 0 and positionY[i+1] < 0):
            break

    # Sparse all arrays of compenents
    positionY_to_plot = SparseArray(positionY)
    positionX_to_plot = SparseArray(positionX)

    WriteToFile(positionX_to_plot, positionY_to_plot, "S-fric2D.dat")

    # Plots
    plt.plot(positionX_to_plot, positionY_to_plot, label="Position $[m]$")
    plt.xlabel("Position x [m]")
    plt.ylabel("Position z [m]")
    plt.legend()
    plt.grid(GRID)
    plt.title(TITLE)
    plt.figtext(0.5, 0.06, f"Initial Velocity: {INITIAL_VELOCITY} m/s", fontsize=12, ha='center', va='center')
    plt.figtext(0.5, 0.04, f"Launch Angle: {LAUNCH_ANGLE} deg", fontsize=12, ha='center', va='center')
    plt.figtext(0.5, 0.02, f"Terminal Velocity: {terminal_velocity} m/s", fontsize=12, ha='center', va='center')
    plt.show()


    return 0


if __name__ == "__main__":

    # Assuming the 1D point particle can be thought of as a spherical body...
    INITIAL_VELOCITY = 50                                   # (m/s)
    LAUNCH_ANGLE = 45                                       # (deg)
    INITIAL_POSITION = 5                                    # (m)
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
    if main(INITIAL_VELOCITY, INITIAL_POSITION, GRAVITY, AIR_DENSITY, OBJECT_FRONT_RADIUS, DRAG_COEFFICIENT, OBJECT_MASS, TIME_INTERVAL, TIME_LIMIT, GRID, TITLE, LAUNCH_ANGLE):
        exit(1)
    else:
        exit(0)
