# Project Name: Smooth Data
# Project ID  : S-GEN-SmoothData
# Description : This software reads an X-Y paired dataset in a file, and plots those X-Y pairs. X-Y paired dataset is also smoothed by using moving-average
#   algorithm, and assessed by using chi-square algorithm. Smoothed data is also plotted alongside the original data, with the information of optimum (best)
#   neighboring points (N) chosen in the smoothing process and chi-square assessment for the data. See the main function for details.
#   The X-Y paired dataset can also be generated from scratch, optionally. When the dataset is intended to be generated, a file with the newly generated
#   version of X-Y pairs gets written on a dedicated filepath.
#
#   (!) Configuration variables can be found at the bottom of this file.
#

import matplotlib.pyplot as plt
import math
import random

def generate_dataXY(min: int, max: int, count:int):
    """
    Generate X-Y pairs, Y is in a contunious order and generated randomly, X is from 0 to count.

    Parameters:
    - min (int): Minimum value of Y pairs.
    - max (int): Maximum value of Y pairs.
    - count (int): Number of of X-Y pairs.

    Returns:
    - list: Dataset of X.
    - list: Dataset of Y.
    """

    if (min > max or min <= 0 or max <= 0): exit(1)

    val = random.uniform(min, max)
    dataX = []
    dataY = []

    for i in range(count):
        dataY.append(val)
        dataX.append(i)
        if (round(random.random())):
            val += random.uniform(0, (max+min)/(max-min))
        else:
            val -= random.uniform(0, (max+min)/(max-min))

    return dataX, dataY


def write_dataXY(data, filePath:str):
    """
    Write X-Y paired data to the given filepath.

    Parameters:
    - data (list): Data which includes X-Y pairs.
    - filePath (str): Filepath to write.

    Returns:
    - int: Return 1 if succeeded.
    """
    dataX, dataY = data

    with open(filePath, 'w') as file:
        for x, y in zip(dataX, dataY):
            file.write(f"{x}\t{y}\n")

    return 0


def moving_average(list, N: int):
    """
    Read each point of list and return it with the average of N neighboring data points.

    Parameters:
    - list (list): List of data to be smoothed.
    - N (int): Number of neighboring points.

    Returns:
    - list: List of moving averages.
    """

    if (len(list) < N): exit(1)

    movingAverage = []

    for i in range(len(list)):
        startIndex = max(0, i - N // 2)
        endIndex = min(len(list), i + N // 2 + 1)
        neighbors = list[startIndex:endIndex]
        average = sum(neighbors) / len(neighbors)
        movingAverage.append(average)

    return movingAverage


def chi_square(expected_data, observed_data):
    """
    Calculate the chi-square difference between the expected data and observed data.

    Parameters:
    - expected_data (list): List of input data points.
    - observed_data (list): List of output data points.

    Returns:
    - float: Chi-square difference.
    """

    if (len(observed_data) != len(expected_data)): exit(1)

    chiPositive = chiNegative = 0
    # epsilon (tolerance): handling division by zero
    # This variable is needed to also consider the possibilities where we need to divide by zero.
    epsilon = 1e-10

    for i in range(len(expected_data)):
        chiPositive += ((observed_data[i] - expected_data[i] + epsilon)**2) / (expected_data[i] + epsilon)
        chiNegative += ((observed_data[i] - expected_data[i] - epsilon)**2) / (expected_data[i] - epsilon)

    return round((chiPositive + chiNegative) / 2, -int(math.log(epsilon)))


def chi_square_over_ns(list):
    """
    Generate a chi-square assessment for various number of neighboring data points.

    Parameters:
    - list (list): List of input data points.

    Returns:
    - list: Number of neighboring data points from 0 to given list length
    - list: chi_square assesments for given list and its moving average
    """

    chiSquareArray = []

    # loop starts from 2, because n = 0 and n = 1 are the original data itself
    for n in range(2, len(list), 2):
        chiSquareArray.append(chi_square(list, moving_average(list, n)))

    return chiSquareArray


#########################################################################

def main(filename: str, yLabel: str, xLabel: str, title:str):
    # Lists of variables as data and neighboring data points (N)
    dataX = []
    dataY = []
    N = []

    # Read data from file
    with open(filename, 'r') as file:
        for line in file:
            vals = line.split()
            dataX.append(float(vals[0]))
            dataY.append(float(vals[1]))

    # Generate the values of neighboring data points (N)
    for n in range(2, len(dataY)):      # (!) N = 0 and N = 1 gives the same result as the original data.
        N.append(n)

    # First, define the best N and ChiSquare to their default values
    bestN = 0
    bestChiSquare = float('inf')

    # Determine best chi-square and best N for minimal error in output data
    for n in N:
        chiSquare = chi_square(dataY, moving_average(dataY, n))
        if (chiSquare < bestChiSquare):
            bestChiSquare = chiSquare
            bestN = n

    # Generate smooth datasets with the best N and best chi-square
    smoothDataX = moving_average(dataX, bestN)
    smoothDataY = moving_average(dataY, bestN)

    # Plot the original data and smoothed data
    plt.plot(dataX, dataY, label="Original Data")
    plt.plot(smoothDataX, smoothDataY, label="Smoothed Data")
    plt.ylabel(yLabel)
    plt.xlabel(xLabel)
    plt.legend()
    plt.title(title)
    plt.figtext(0.5, 0.04, f"Best N: {bestN}\nChi-square difference: {bestChiSquare}", fontsize=12, ha='center', va='center')
    plt.show()

    '''
    By using chi_square_over_ns(), we can also plot the chi_square differences for different values of neighboring data points (N)
    This can be done as
    plt.plot(N, chi_square_over_ns(dataY))
    '''

    return 0


if __name__ == "__main__":

    #
    #   Configuration
    #
    generate_and_use_random_data = True     # Change this to "False" if you already have a file as an input.
    # Below three are meaningful only when generate_and_use_random_data is True.
    data_min = 0            # Minimum value of the data to be generated, Y only.
    data_max = 100          # Maximum value of the data to be generated, Y only.
    data_count = 500        # Number of data points to be generated.

    filepath = "input.txt"  # Read data from this file. If generate_and_use_random_data is True, a new file with this name will be generated before the main function is executed.
    yLabel = "Y values"     # Y label of the plot.
    xLabel = "X values"     # X label of the plot.
    title = "X-Y values"    # Title of the plot.

    #
    #   Main Function
    #
    if (generate_and_use_random_data):
        if (not write_dataXY(generate_dataXY(data_min, data_max, data_count), filepath)):
            main(filepath, yLabel, xLabel, title)
        else:
            print("There was an error generating random data.")
            exit(1)
    else:
        main(filepath, yLabel, xLabel, title)

    exit(0)
