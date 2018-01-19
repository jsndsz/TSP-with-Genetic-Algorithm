""" This program attempts to solve the TSP with the use of Genetic algorithm
    Coordinate points are generated at random between 0 and 100. 
    Initital and final states are shown.
    The problem is dynamic and any  number of cities can be given
    Random indexed lists of the initial state are generated.
    Each list is given a weightage on the total distance it is currently at.
    The top 10 states are chosen and crossed to generated the children.
    These are slightly mutated (indexes changed) to imporve results
    
    """

import random
import time

class geneticAlgorithm(object):
    
    def getDistance(self,P1,P2): #Distance between 2 points
        self.P1 = P1
        self.P2 = P2
        distance = ((self.P1[0]-self.P2[0])**2 + (self.P1[1]-self.P2[1])**2)**(1/2)
        return distance

    def generateCoordinates(self): #Coordinates generated at random
        x = random.randint(0,101)
        y = random.randint(0,101)
        return [x,y]
 
    def generateRandom(self,s,n):  #Generating random states with indexs jumbled
        self.s = s
        self.n = n
        changeIndexOne = random.randint(1,self.n-1)
        changeIndexTwo = random.randint(1,self.n-1)
        transState = s[:] 
        dummy1 = transState[changeIndexOne]
        dummy2 = transState[changeIndexTwo]
        transState[changeIndexOne] = dummy2
        transState[changeIndexTwo] = dummy1
        return transState
    
    
    def crossOver(self,p1,p2,n): #The cross over of 2 parents to produce 2 children
        self.p1 = p1
        self.p2 = p2
        self.num = n
        
        r = random.randint(1,self.num-1)
        s = self.num - r
        c1 = self.p1[:r]
        c2 = self.p2[:s]
        for count in range(1,self.num):
            if self.p2[count] not in c1:
                c1.append(self.p2[count])
            if self.p1[count] not in c2:
                c2.append(self.p1[count])
        c1.append('0')
        c2.append('0')
        return (c1,c2)
      
    def calculateDist(self,s,n): #Calculates total distance in a state
        self.calD = s
        self.nu = n
        dist = 0
        total = 0
        for i in range(self.nu):
            xi = self.calD[i]
            yj = self.calD[i+1]
            dist = self.getDistance(self.coord[xi],self.coord[yj])
            total+=dist    
        return total
            

        
    def solver(self):
        
        number = input("How many cities do you want to generate: ")
        self.coord ={}
        cityList = []
        stateList = []
        childList =[]
        self.number = int(number)
        for i in range(self.number):
            a = str(i)
            l = self.generateCoordinates()
            self.coord[a] = l
            cityList.append(a)
        cityList.append('0')
        currentState = cityList[:]

        totalDist = 0
        for i in range(self.number):
            xi = currentState[i]
            yj = currentState[i+1]
            dist = self.getDistance(self.coord[xi],self.coord[yj])
            totalDist += dist
        
        currentDist = totalDist
        initialDist = totalDist
        
        noOfStates = 3*self.number
        for i in range(noOfStates):
            intState = self.generateRandom(currentState,self.number)
            for x in range(int(noOfStates/2)):
                intState = self.generateRandom(intState,self.number)
            finalState = self.generateRandom(intState,self.number)
            stateList.append(finalState)
            
        stateListSorted =[]
     
        for i in range(len(stateList)):
            d = self.calculateDist(stateList[i],self.number)
            stateListSorted.append((d,stateList[i]))
        
        stateListSorted.sort()
        
        lowest = [initialDist,currentState]
        
        stateListTop = stateListSorted[:10]
        
        for i in range(len(stateListTop)-1):
            for j in range(1,len(stateListTop)-1):
                child = self.crossOver(stateListTop[i][1],stateListTop[j][1],self.number)
                childList.append(child[0])
                #child2 = self.crossOver(stateOne[one],stateTwo[two],self.number)
                childList.append(child[1])
                
            
                a = self.calculateDist(child[0],self.number)
                b = self.calculateDist(child[1],self.number)
                
                if a < lowest[0]:
                    lowest[0] = a
                    lowest[1] = child[0]
                
                if b < lowest[0]:
                    lowest[0] = b
                    lowest[1] = child[1]
                    
            
        for i in range(len(childList)):
            mutate = self.generateRandom(childList[i],self.number)
            mutateDist = self.calculateDist(mutate,self.number)
            if mutateDist < lowest[0]:
                lowest[0] = mutateDist
                lowest[1] = mutate
            
        childDistance = []
        
        for c in range(20):
            dist = 0
            totalDist = 0
            send = childList[c]
            childDistance.append(self.calculateDist(send,self.number))

        pval = lowest[0]
        value = min(childDistance)
        if pval < value:
            value = pval
            currentState = lowest[1]
        else:    
            ind = childDistance.index(value)
            currentState = childList[ind]
            
        print("Initial state looked like this: ",cityList,"\n")
        print("Point coordinates were: ",self.coord,"\n")
        print("Initial distance was: %.2f km \n" %initialDist)
        print("Final state looks like: ",currentState, "\n")
        print("Optimized distance is: %.2f km \n" %value)


def main():
    start = time.time()
    gA = geneticAlgorithm() 
    gA.solver()
    end = time.time()
    print("Time measure: %.2f sec" % (end-start))

if __name__ == "__main__":
    main()  