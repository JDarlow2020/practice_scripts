#!/usr/bin/env python3
# Python3 script to find group of an unknown point using K-Nearest-Neighbour algorithm
# test arguments
#p = (2,5) # returns -1 (neither) with k = 4
#p = (2,8) # returns 0 (group 1)
#p = (5,2) # returns 1 (group 2)
#k = 4
import sys
import math
import matplotlib.pyplot as plt
import argparse
parser = argparse.ArgumentParser(description = "Practice K-Nearest-Neighbour supervised learning algorithm for categorising a point into one of two groups in a scatter plot. If no groups are provided as input, test groups are provided as default.", epilog = "Please see GitHub Link")
parser.add_argument("-g1","--group1",metavar="",type=list,help="Scatter plot coordinates for group 1")
parser.add_argument("-g2","--group2",metavar="",type=list,help="Scatter plot coordinates for group 2")
parser.add_argument("-x","--xpoint",metavar="",type=int,help="Scatter plot x coordinate for a point to categorise", required=True)
parser.add_argument("-y","--ypoint",metavar="",type=int,help="Scatter plot y coordinate for a point to categorise", required=True)
parser.add_argument("-k","--k_nearest",metavar="",type=int,help="Number of K-Nearest-Neighbours to use (default is 3)",default=3)
parser.add_argument("-q","--quiet",default=False,action="store_true",help="Run in quiet mode")
parser = parser.parse_args()

a = [parser.xpoint,parser.ypoint]

if not parser.group1 and not parser.group2:
    points = {0:[(1,12),(2,5),(3,6),(3,10),(3.5,8),(2,11),(2,9),(1,7)],
            1:[(5,3),(3,2),(1.5,9),(7,2),(6,1),(3.8,1),(5.6,4),(4,2),(2,5)]}
#else:
#    define points variable

def plot_figure(points, point=False):
    '''
    Plots simple scatter graph of two groups of points and an additional point to be categorised by KNN

    Parameters:
        points - a dictionary of training points for two groups having two keys - 0 and 1
        point - a single point to plot given as a list or tuple e.g. (x,y)
    '''
    x0 = []
    y0 = []
    for i in points[0]:
        x0.append(i[0])
        y0.append(i[1])
    x1 = []
    y1 = []
    for i in points[1]:
        x1.append(i[0])
        y1.append(i[1])
    plt.scatter(x0,y0, color = "blue", label = "Group 1")
    plt.scatter(x1,y1, color = "green", label = "Group 2")
    if point != False:
        plt.scatter(point[0], point[1], color = "red", label = "Input Point")
    plt.legend(loc="upper right")
    plt.savefig("scatter_plot.png")

def classifyAPoint(points,p,k=parser.k_nearest):
    '''
    Classify point p using k nearest neighbor algorithm. Assumes only two groups (0 and 1).

    Parameters:
        points - a dictionary of training points for two groups having two keys - 0 and 1
        p - a list or tuple test data point e.g. (x,y)
        k - the number of nearest neighbours to consider, default is 3
    '''
    if parser.k_nearest % 2 == 0:
        print("Warning - using an even number of nearest neighbours is not advised as it can result in uncategorised output")
    plot_figure(points, p)
    distance={}
    for group in points:
        for feature in points[group]:

            #calculate the euclidean distance of p from points in groups, add to distance dictionary
            euclidean_distance = math.sqrt((feature[0]-p[0])**2 +(feature[1]-p[1])**2)
            distance[str(euclidean_distance)] = ((feature,euclidean_distance,group))

    # sort the distance list in ascending order and select first k distances
    dist_list = [float(i) for i in distance.keys()]
    dist_list.sort()
    dist_list = [str(i) for i in dist_list]
    distance = {i: distance[i] for i in dist_list}
    dist_list = list(distance.keys())[:k]
    distance = {i: distance[i] for i in dist_list}
    freq1 = 0 #frequency of group 0
    freq2 = 0 #frequency of group 1
    if not parser.quiet:
        print(f"Nearest {k} neighbours to point {p}:")
    for d in distance.keys():
        if not parser.quiet:
            print(f"Coordinates: {distance[d][0]}\tDistance: {distance[d][1]}\tGroup: {distance[d][-1]}")
        if distance[d][-1] == 0:
            freq1 += 1
        elif distance[d][-1] == 1:
            freq2 += 1
    if freq1>freq2:
        return 0 
    elif freq2>freq1:
        return 1
    else:
        return -1

def main():
    # Dictionary of training points having two keys - 0 (group 1) and 1 (group 2)
    print(f"The group classified to unknown point is: {classifyAPoint(points,a,parser.k_nearest)+1}")

if __name__ == '__main__':
    main()