import heapq
import random
import time
def heapSearch( tupArray, k ):
    heap = []
    for item in tupArray:
        #print "item",item[1]
        if len(heap) < k or item[1] > heap[0][1]:
            if len(heap) == k: heapq.heappop( heap )
            heapq.heappush( heap, item )
    return heap


import csv
import numpy as np
def loadTrainingDataset(filename):
    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)

        num_idx = [5, 14, 18, 19, 20, 21, 22, 23, 24, 25, 31, 33]
        cat_idx = []
        for i in range(2, 34):  # exclude refid and label for distance
            if i in num_idx:
                continue
            else:
                cat_idx.append(i)
        #print("cat_idx", cat_idx)
                
        cur_attr = np.zeros(len(dataset)-1)
         
        for y in num_idx:
            for x in range(1, len(dataset)):
            
                #print(dataset[x][y])
                if dataset[x][y] == 'NULL':
                    print("at",x,y)
                dataset[x][y] = float(dataset[x][y])
                cur_attr[x-1] = dataset[x][y]
            min_x = np.min(cur_attr)
            max_x = np.max(cur_attr)
            # normalize data:
            # http://stats.stackexchange.com/questions/70801/how-to-normalize-data-to-0-1-range
            for x in range(1, len(dataset)):
                dataset[x][y] = (dataset[x][y]-min_x)/(max_x-min_x)

        tr = []
        #print "training size", 2*len(dataset)//200
        #for i in range(0, 2*len(dataset)//3):

        for i in range(0, len(dataset)):
            tr.append(dataset[i])

        return tr
        #for x in range(1, 10):
         #   print(trainingSet[x])

def loadTestDataset(filename):
    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)

        num_idx = [4, 13, 17, 18, 19, 20, 21, 22, 23, 24, 30, 32]
        cat_idx = []
        for i in range(1, 33):  # exclude refid for distance
            if i in num_idx:
                continue
            else:
                cat_idx.append(i)
                
        cur_attr = np.zeros(len(dataset)-1)
         
        for y in num_idx:
            for x in range(1, len(dataset)):
            
                #print(dataset[x][y])
                if dataset[x][y] == 'NULL':
                    print("at",x,y)
                dataset[x][y] = float(dataset[x][y])
                cur_attr[x-1] = dataset[x][y]
            min_x = np.min(cur_attr)
            max_x = np.max(cur_attr)
            # normalize data:
            # http://stats.stackexchange.com/questions/70801/how-to-normalize-data-to-0-1-range
            for x in range(1, len(dataset)):
                dataset[x][y] = (dataset[x][y]-min_x)/(max_x-min_x)

        ts = []
        for i in range(0, len(dataset)):
            ts.append(dataset[i])    

        
        #for x in range(1, 10):
         #   print(ts[x])
        return ts



import math
def euclideanDistance(testInstance, trainingSet, num_idx, cat_idx):
    distance = 0
    
    for x in num_idx:
        #print("x",x, testInstance[x-1], trainingSet[x])
        distance += pow((testInstance[x-1] - trainingSet[x]), 2)

    for x in cat_idx:
        if testInstance[x-1] == trainingSet[x]:
            distance += 0
        else:
            distance += 1
        
    return math.sqrt(distance)



import operator 
def getNeighbors(trainingSet, testInstance, k, num_idx, cat_idx):
    distances = []
    for x in range(1,len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], num_idx, cat_idx)
        distances.append((trainingSet[x], dist))
    #distances.sort(key=operator.itemgetter(1))
    neighbors = heapSearch(distances, k)
    #for x in range(k):
    #        neighbors.append(distances[x][0])
    return neighbors


def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        #print "neighbors", neighbors[x][0][1]
        response = neighbors[x][0][1]
        if response in classVotes:
                classVotes[response] += 1
        else:
                classVotes[response] = 1
    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]


def writeToFile(data):
    with open('result-test-hp-35000-40000.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(data)

# Main:


trainingSet = loadTrainingDataset('training-pre.csv')
testSet = loadTestDataset('test-pre.csv')

tr_l = len(trainingSet)
trainingSet= trainingSet[1:tr_l:5]
#print "training size", len(trainingSet)
testSet = testSet[35000:40000]
predictions=[]

num_idx = [5, 14, 18, 19, 20, 21, 22, 23, 24, 25, 31, 33]
cat_idx = []
for i in range(1, 34):  # exclude refid and lable for distance
    if i in num_idx:
        continue
    else:
        cat_idx.append(i)

num_idx2 = [4, 13, 17, 18, 19, 20, 21, 22, 23, 24, 30, 32]
cat_idx2 = []
for i in range(1, 33):  # exclude refid for distance
    if i in num_idx2:
        continue
    else:
        cat_idx2.append(i)

        
k = 3
start = time.time()
for x in range(len(testSet)-1):
        

        neighbors = getNeighbors(trainingSet, testSet[x+1], k, num_idx, cat_idx)
        result = getResponse(neighbors)
        
       
        row = [testSet[x+1][0] ,result]
        
        predictions.append(row)
        if x%20 == 0:
            print "In data line:",x
        #print('> predicted=' + repr(result))

writeToFile(predictions)
print "Finishing: Time taken %g s" % (time.time() - start)



        
#accuracy = getAccuracy(testSet, predictions)
#print('Accuracy: ' + repr(accuracy) + '%' + 'k = ',k)
'''        
for x in range(1, 10):
    print(trainingSet[x])
print("======================================")
for x in range(1, 10):
    print(TestingSet[x])
'''

