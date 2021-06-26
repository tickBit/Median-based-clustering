# Median based clustering
#
# Inspired from old final exams of a data mining (and machine learning) course...
#


import math
import random
import numpy as np
import matplotlib.pyplot as plt
import operator

# Dataset
D = []

# k clusters
k = 7

# the number of data points
for i in range(500):
    D.append([random.randint(-100,100),random.randint(-100,100)])

# Shuffle set D
shuffled_D = D[:] # now shuffled_D is a copy of D
random.shuffle(shuffled_D)

# Initial centroids
# "randomness" as I would do it with pen and paper:
# select two first points from shuffled original dataset

centroids = [[None]]*k
prev_centroids = [[None]]*k

for i in range(k):
    centroids[i] = shuffled_D[i][:]


iterations = 0

# Main loop
while True:

    iterations += 1

    # tässä vaiheessa edelliset centroidit ovat nykyiset centroidit
    for a in range(k):
        prev_centroids[a] = centroids[a][:]  
    
    manhattans = []
            
    for a in range(k):
        lst = [] 
        for i in range(len(D)):
                 
            # Manhattan distances for the centroids
            # save index of a point and the distance of the point from centroid
            lst.extend([(i,abs(D[i][0]-centroids[a][0]) + abs(D[i][1]-centroids[a][1]))])
            
        
        manhattans.append(lst)

    assignments = []
    
    for u in range(len(manhattans[0])):
        dist = []
        
        for a in range(k):
            
            dist.append((manhattans[a][u][0], manhattans[a][u][1], a))
        
        # Get smallest distance. Below
        # index 0 = index related to a point of the dataset
        # index 1 = the distance of a point from centroid a
        # index 2 = cluster
        assignment = min(dist, key=operator.itemgetter(1))
        assignments.append(assignment)
    
    # sort "assignments" according to cluster
    assignments = sorted(assignments, key=operator.itemgetter(2))
    
    points_by_clusters = []
    
    # Save points by cluster
    # Here we create k lists so that the points belonging to cluster k
    # are in list k
    for i in range(k):
        temp = []
        for a in assignments:
            if a[2] == i:
                temp.append(D[a[0]])
        points_by_clusters.append(temp)
    
    valuex = []
    valuey = []
    
    # Organize data for the median...
    for a in range(k):
        tempx = []
        tempy = []
        for p in points_by_clusters[a]:
            tempx.append(p[0])
            tempy.append(p[1])
        valuex.append( tempx )
        valuey.append( tempy )
    
    
    for a in range(k):
        # Calculate the median...
        
        # Median for uneven sets...
        if len(valuex[a]) % 2 != 0:
            # https://simple.wikipedia.org/wiki/Median
            valuex[a].sort()
            valuey[a].sort()
            # Uneven sets: n+1 is here directly because the indexing begins from 0
            centroids[a] = [valuex[a][math.floor(len(valuex[a])/2)], valuey[a][math.floor(len(valuey[a]) / 2)]]
        else:
            valuex[a].sort()
            valuey[a].sort()
            # Even sets: median is mean of the two points in the "center" of the set        
            centroids[a] = [(valuex[a][math.floor((len(valuex[a]))/2)] + valuex[a][math.floor((len(valuex[a])) / 2 - 1)])  / 2.0,
              (valuey[a][math.floor((len(valuey[a]))/2)] + valuey[a][math.floor((len(valuey[a])) / 2 - 1)])  / 2.0]

    # Does the centroids change?
    ready = True
    for a in range(k):
        if prev_centroids[a] != centroids[a]:
            ready = False

    if ready == True: break

    
#
# visualizations
#

clusters = []
for a in range(k):
    temp = []
    for p in points_by_clusters[a]:      
        temp.append([p[0],p[1]])
    clusters.append(temp)

for a in range(k):
    clust = []
    clust = np.array(clusters[a])

    plt.scatter(centroids[a][0], centroids[a][1], marker='*', s=100, color='black')

    plt.scatter(clust[:,0], clust[:,1])


plt.show()

print("Iterations:",iterations)

for a in range(k):
    print("Centroid",(a+1),"=",centroids[a])    