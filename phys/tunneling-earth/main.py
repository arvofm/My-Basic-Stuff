# Project Name: Tunneling Earth
# Project ID  : S-KIN-TunnelingEarth
# Description : This code analyzes the tunneling earth problem, which is, the motion of an object falling through an hypothetical tunnel
#   through the center of the Earth. The code starts with indexing simple harmonic motion equations, which is derived from the differential
#   equations that follows from Newton's Third Law. The lists of motion, velocity, and acceleration of the falling body are then plotted to
#   see a visual. Additionally, the period of the motion is calculated and noted in the figure.
#
#   (i) Configuration variables can be found at the bottom of this file.
#

import math
import matplotlib.pyplot as plt

def GeneratePosition(time:list, angular_frequency:float, R0:float, V0:float, isPositionKm:bool):
    """
    Generate position values over time.

    Parameters:
    - time: List of time values.
    - angular_frequency: Angular frequency calculated based on configuration properties.
    - R0: Initial position.
    - V0: Initial velocity.
    - isPositionKm: Boolean flag indicating whether the position should be in kilometers.

    Returns:
    - List of position values over time.
    """

    r = []
    for i in time:
        r.append((R0*math.cos(angular_frequency*i) + (V0/angular_frequency) * math.sin(angular_frequency*i)) / (1000 if isPositionKm else 1))

    return r


def GenerateVelocity(time:list, angular_frequency:float, R0:float, V0:float, isVelocityKmH:bool):
    """
    Generate velocity values over time.

    Parameters:
    - time: List of time values.
    - angular_frequency: Angular frequency calculated based on configuration properties.
    - R0: Initial position.
    - V0: Initial velocity.
    - isVelocityKmH: Boolean flag indicating whether the velocity should be in kilometers per hour.

    Returns:
    - List of velocity values over time.
    """

    v = []
    for i in time:
        v.append((V0*math.cos(angular_frequency*i) - R0*angular_frequency*math.sin(angular_frequency*i)) * (3.6 if isVelocityKmH else 1))

    return v


def GenerateAcceleration(position:list, angular_frequency:float, isPositionInKm:bool):
    """
    Generate acceleration values based on position.

    Parameters:
    - position: List of position values.
    - angular_frequency: Angular frequency calculated based on configuration properties.
    - isPositionInKm: Boolean flag indicating whether the position is in kilometers.

    Returns:
    - List of acceleration values over time.
    """

    a = []
    for r in position:
        a.append(- angular_frequency * angular_frequency * r * (1000 if isPositionInKm else 1))

    return a

def FindPeriod(time:list, position:list, R0:float, isPositionKm:bool):
    """
    Finds the time at which a specified position is reached in the given time series.

    Parameters:
    - time (list): A list of time values.
    - position (list): A list of corresponding position values.
    - R0 (float): The target position to be found.

    Returns:
    - float or zero: The time at which the specified position is first reached.
      Returns 0 if the position is not found in the provided data.
    """

    error_rate = 0.01 if isPositionKm else 10
    for i in range(2, len(position)):
        if (abs(position[i] - (R0 / (1000 if isPositionKm else 1))) <= error_rate):
            return time[i]

    return 0


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


def PlotPosition(plotter, time:list, position:list, isPositionKm:bool, useGrid:bool):
    """
    Plot position values over time.

    Parameters:
    - plotter: Matplotlib subplot for plotting.
    - time: List of time values.
    - position: List of position values.
    - isPositionKm: Boolean flag indicating whether the position is in kilometers.

    Returns:
    - 0 (if successful).
    """

    plotter.plot(time, position, color="black", linewidth=2)
    plotter.set_title("Position vs. Time")
    plotter.set_xlabel("Time $(s)$", fontsize=16)
    plotter.set_ylabel("Position " + "$(km)$" if isPositionKm else "$(m)$", fontsize=16)
    plotter.grid(True if useGrid else False)

    return 0


def PlotVelocity(plotter, time:list, velocity:list, isVelocityKmH:bool, useGrid:bool):
    """
    Plot velocity values over time.

    Parameters:
    - plotter: Matplotlib subplot for plotting.
    - time: List of time values.
    - velocity: List of velocity values.
    - isVelocityKmH: Boolean flag indicating whether the velocity is in kilometers per hour.

    Returns:
    - 0 (if successful).
    """

    plotter.plot(time, velocity, color="black", linewidth=2)
    plotter.set_title("Velocity vs. Time")
    plotter.set_xlabel("Time $(s)$", fontsize=16)
    plotter.set_ylabel("Velocity " + "$(km/h)$" if isVelocityKmH else "$(m/s)$", fontsize=16)
    plotter.grid(True if useGrid else False)

    return 0


def PlotAcceleration(plotter, time:list, acceleration:list, useGrid:bool):
    """
    Plot acceleration values over time.

    Parameters:
    - plotter: Matplotlib subplot for plotting.
    - time: List of time values.
    - acceleration: List of acceleration values.

    Returns:
    - 0 (if successful).
    """

    plotter.plot(time, acceleration, color="black", linewidth=2)
    plotter.set_title("Acceleration vs. Time")
    plotter.set_xlabel("Time $(s)$", fontsize=16)
    plotter.set_ylabel("Acceleration $(m/s^2)$", fontsize=16)
    plotter.grid(True if useGrid else False)

    return 0


############################################################################################################################

def main(PLANET_DENSITY, G, R0, V0, TIME_INTERVAL, TIME_LIMIT, VELOCITY_IN_KM_H, POSITION_IN_KM, GRID, PERIOD_IN_SEC):

    # Angular frequency derived from gravitational force and extracting Earth mass, which is M = 4/3*pi*r^3*d
    # then, a + (4/3*pi*d*G)x = 0
    angular_frequency = math.sqrt(4/3 * math.pi * PLANET_DENSITY * G)
    # Generate time stamps
    time = GenerateTime(TIME_LIMIT, TIME_INTERVAL)
    # Generate position stamps
    position = GeneratePosition(time, angular_frequency, R0, V0, POSITION_IN_KM)
    # Generate velocity stamps
    velocity = GenerateVelocity(time, angular_frequency, R0, V0, VELOCITY_IN_KM_H)
    # Generate acceleration stamps
    acceleration = GenerateAcceleration(position, angular_frequency, POSITION_IN_KM)
    # Look if there is a period
    period = FindPeriod(time, position, R0, POSITION_IN_KM)

    # Plot all
    fig, ax = plt.subplots(3, 1)
    PlotPosition(ax[0], time, position, POSITION_IN_KM, GRID)
    PlotVelocity(ax[1], time, velocity, VELOCITY_IN_KM_H, GRID)
    PlotAcceleration(ax[2], time, acceleration, GRID)

    # If there is a period, insert it as a text in figure
    if (period):
        fig.text(0.5, 0.05, f"Period: {period}s" if PERIOD_IN_SEC else f"Period: {period // 60}min {period % 60}s", fontsize=12, ha='center', va='center')

    plt.tight_layout()
    plt.show()

    return 0


if (__name__ == "__main__"):
    #
    # Main Variables
    #
    PLANET_DENSITY = 5515                       # 5515 is for the Earth (kg m^-3)
    G = 6.67430 * 10**(-11)                     # Gravitational Constant (m^3 kg^-1 s^-2)
    PLANET_RADIUS = (6378 + 6357)*1000 / 2      # 6378 is maximum, 6357 is minimum, for the Earth (m)

    #
    # Configuration Variables
    #
    VELOCITY_IN_KM_H = True                 # Instead of meters per second (m/s)
    POSITION_IN_KM = True                   # Instead of meters (m)
    PERIOD_IN_SEC = False                   # Instead of minutes (min)
    GRID = False                            # Enable grid for plots
    TIME_LIMIT = 10000                      # To what extent the time should be considered
    TIME_INTERVAL = 100                     # The time interval from zero to TIME_LIMIT, higher values result in lower quality with high performance
    R0 = PLANET_RADIUS                      # Initial position to start the harmonic motion of "Tunelling Earth" problem
    V0 = 0                                  # Initial speed

    #
    #   Main Function
    #
    main(PLANET_DENSITY, G, R0, V0, TIME_INTERVAL, TIME_LIMIT, VELOCITY_IN_KM_H, POSITION_IN_KM, GRID, PERIOD_IN_SEC)

    exit(0)
