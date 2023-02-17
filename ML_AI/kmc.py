#!/usr/bin/env python3

import sys
import argparse
from random import uniform
from random import randint
import math
from collections import defaultdict, OrderedDict
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description = "Learning Exercise: K-means Clustering Algorithm for k number of centroids.")
parser.add_argument("-k","--k_centroids",metavar="",type=int,help="Number of centroids to use (default is 3, must be at least 2)",default=3)
parser.add_argument("-i","--max_iterations",metavar="",type=int,help="Maximum number of iterations per restart (default is 10)",default=10)
parser.add_argument("-r","--restarts",metavar="",type=int,help="Maximum number of times to restart algorithm from different start points (default is 3)",default=3)
parser = parser.parse_args()

points = {0:[(1.5,12),(2,8),(3.2,7),(3,10.1),(3.5,8),(2,11.2),(2,9),(1,7),(1,1),(1.5,2),(1,3),(3,2)],
        1:[(6.5,2),(8,1),(9,2.3),(8,1.7),(6.5,1.8),(8.3,3),(9,3.1),(8.7,2.6),(7,3),(5,5),(5.5,6),(4.7,6),(6,4.1),(5.8,4.2)],
        2:[(7,7),(8,8),(7.8,8.7),(7,10),(6,11),(8,10),(6.8,9.5),(7.2,8),(8,12),(8.5,11.5),(5.7,8)]}

def get_boundaries(p): # get x and y boundaries to generate centroid positions
    x = []
    y = []
    for i in p.keys():
        for j in p[i]:
            x.append(j[0])
            y.append(j[1])
    return float(min(x)), float(max(x)), float(min(y)), float(max(y))

def generate_centroids(k, min_x, max_x, min_y, max_y):
    centroids = defaultdict(list)
    for i in range(k):
        centroids[str(i)] = [uniform(min_x, max_x), uniform(min_y, max_y)]
    centroids = OrderedDict(sorted(centroids.items()))
    return centroids

def plot_figure(points, centroids, outname):
    r = lambda: randint(0,255)
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
    x2 = []
    y2 = []
    for i in points[2]:
        x2.append(i[0])
        y2.append(i[1])
    plt.scatter(x0,y0, color = "blue", label = "Group 1")
    plt.scatter(x1,y1, color = "green", label = "Group 2")
    plt.scatter(x2,y2, color = "red", label = "Group 3")
    if centroids != False:
        count = 0
        for i in centroids:
            #print(i[0], i[1])
            plt.scatter(i[0], i[1], color = '#%02X%02X%02X' % (r(),r(),r()), label = f"Centroid {count}")
            count += 1
    plt.xlim(right = 12)
    plt.legend(loc="upper right")
    plt.savefig(outname)
    plt.close()

def find_nearest_centroid(points,centroids):
    centroid_groups = defaultdict(list)
    for i in points.keys():
        for j in points[i]:
            count = 0
            temp = False
            tempd = 0
            centroid_dists = {}
            for c in centroids:
                distance = math.sqrt((c[0] - j[0])**2 + (c[1] - j[1])**2)
                centroid_dists[str(count)] = distance
                count += 1
            for i in centroid_dists.keys():
                if (temp == False) or (centroid_dists[i] < tempd):
                    temp = i
                    tempd = centroid_dists[i]
            centroid_groups[temp].append(tuple(j))
    centroid_groups = OrderedDict(sorted(centroid_groups.items()))
    return centroid_groups
    
def create_new_centroids(centroid_groups):
    new_centroids = defaultdict(list)
    for group in centroid_groups:
        av_x = sum([i[0] for i in centroid_groups[group]])/len(centroid_groups[group])
        av_y = sum([i[1] for i in centroid_groups[group]])/len(centroid_groups[group])
        new_centroids[group] = [av_x, av_y]
    new_centroids = OrderedDict(sorted(new_centroids.items()))
    return new_centroids

def check_change(centroid_groups_prev, new_centroid_groups):
    check = True
    for i in new_centroid_groups.keys():
        if set(centroid_groups_prev[i]).issubset(set(new_centroid_groups[i])) and set(new_centroid_groups[i]).issubset(set(centroid_groups_prev[i])):
            check = True
        else:
            check = False
            break
    return check

def main():
    min_x, max_x, min_y, max_y = get_boundaries(points)
    centroids = generate_centroids(parser.k_centroids, min_x, max_x, min_y, max_y)
    print("First centroids:")
    print(centroids.values())
    plot_figure(points,centroids.values(), "centroids_plot.png")
    centroid_groups_prev = find_nearest_centroid(points,centroids.values())
    print("First Centroid Groups:")
    print(centroid_groups_prev)
    new_centroids = create_new_centroids(centroid_groups_prev)
    print("\nNext Centroids:")
    print(new_centroids)
    plot_figure(points,new_centroids.values(), "centroids_plot2.png")
    new_centroid_groups = find_nearest_centroid(points,new_centroids.values())
    print("Next Centroid Groups:")
    print(new_centroid_groups)
    icount = 1
    while check_change(centroid_groups_prev,new_centroid_groups) != True:
        if icount <= parser.max_iterations:
            temp = new_centroid_groups
            new_centroids = create_new_centroids(centroid_groups_prev)
            new_centroid_groups = find_nearest_centroid(points,new_centroids.values())
            centroid_groups_prev = temp
            icount += 1
            print("Iteration " + str(icount))
        else:
            print("max iterations reached")
            break

    print(f"K-Means Clustering Complete ({icount} Iterations) - Final Clusters:")
    print(new_centroid_groups.items())





if __name__ == "__main__":
    main()

