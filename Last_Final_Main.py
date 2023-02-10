from scipy.io import loadmat
import numpy as np 
import sys
import matplotlib.pyplot as plt
sys.setrecursionlimit(500000)
import csv
import pprint



# mazemap=np.array([
# [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
# [1,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,1],
# [1,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,2,0,1],
# [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1],
# [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1],
# [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1],
# [1,0,0,0,1,1,1,1,1,0,0,0,0,0,1,1,0,0,0,1],
# [1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1],
# [1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1],
# [1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1],
# [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
# [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1],
# [1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1],
# [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]])

data=loadmat('maze.mat')
mazemap=np.array(data['map'], dtype= np.uint32) 
# mazemap=np.array([
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
# [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2]
# ])

# mazemap=np.array(
#     [
#  [0,0,0,0,0,0,0,0],
#  [2,0,0,1,0,0,0,0], 
# [1,1,0,1,0,0,0,0],
# [0,0,1,1,0,0,0,0],
# [0,0,1,1,0,0,0,0],
# [0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,0,0]
# ]
# )




class Wavefront:
    def __init__(self):
        data=loadmat('maze.mat')
        #print("loaded array is:",data)
        mazemap=np.array(data['map'], dtype= np.uint32)
        #self.planner(matrix)
        #self.z=[]
        i_start=int(input("enter start row(enter 12 for row 13 and so on): "))
        j_start=int(input("enter start col:(enter 1 for col 2 and so on) "))
        #self.planner(matrix,i_start,j_start)
        self.planner(mazemap,i_start,j_start) 


    def planner(self,map,i_start,j_start):
        arr=[]
        for i in range(map.shape[0]):
            for j in range(map.shape[1]):
                if (map[i][j]==2):
                    arr.append([i,j]) 
                    print("goal indices:",i,j)
                    break 

        filledmatrix=self.fillMatrix(map,arr)
        # with open('data.csv',"w+") as file:
        #     writer = csv.writer(file, delimiter=',')
        #     writer.writerows(filledmatrix)
        print("filled matrix is:",filledmatrix)


        z=self.shortest_path(filledmatrix,i_start,j_start)
        print("z is:",z)

        coloredmatrix=np.zeros((len(filledmatrix),len(filledmatrix[0])))
        for i in range(len(filledmatrix)):
            for j in range(len(filledmatrix[0])):
                coloredmatrix[i][j]=150     # white
                if filledmatrix[i][j]==1:
                    coloredmatrix[i][j]=255 # blue      
            
        for i in range(len(z)):
            if (i==len(z)-1):
                coloredmatrix[z[i][0]][z[i][1]]=95 # yellow
            else:    
                coloredmatrix[z[i][0]][z[i][1]]=0 # red

        coloredmatrix[i_start][j_start]=60 # start        

        plt.imshow(coloredmatrix,cmap="RdYlBu")
        plt.show()
               


    def fillMatrix(self,map,arr):
        newArr=[]
        if (len(arr)==0):
            return map   
        for i in range(len(arr)):
            i_key=arr[i][0]
            j_key=arr[i][1]
            heightBoundary=map.shape[0]-1
            widthBoundary=map.shape[1]-1
            if (0<=i_key-1<=heightBoundary):
                if (map[i_key-1][j_key]==0):# upper
                    map[i_key-1][j_key]=map[i_key][j_key]+1
                    newArr.append([i_key-1,j_key])

            if (0<=j_key+1<=widthBoundary):
                if (map[i_key][j_key+1]==0):# right
                    map[i_key][j_key+1]=map[i_key][j_key]+1
                    newArr.append([i_key,j_key+1]) 

            if (0<=i_key+1<=heightBoundary):
                if (map[i_key+1][j_key]==0):# down
                    map[i_key+1][j_key]=map[i_key][j_key]+1
                    newArr.append([i_key+1,j_key]) 

            if (0<=j_key-1<=widthBoundary):
                if (map[i_key][j_key-1]==0):# left
                    map[i_key][j_key-1]=map[i_key][j_key]+1
                    newArr.append([i_key,j_key-1])

            if (0<=i_key-1<=heightBoundary and 0<=j_key+1<=widthBoundary):
                if (map[i_key-1][j_key+1]==0):# upper right
                    map[i_key-1][j_key+1]=map[i_key][j_key]+1
                    newArr.append([i_key-1,j_key+1]) 

            if (0<=i_key+1<=heightBoundary and 0<=j_key+1<=widthBoundary):
                if (map[i_key+1][j_key+1]==0):# lower right
                    map[i_key+1][j_key+1]=map[i_key][j_key]+1
                    newArr.append([i_key+1,j_key+1])

            if(0<=i_key+1<=heightBoundary and 0<=j_key-1<=widthBoundary):
                if (map[i_key+1][j_key-1]==0):# lower left
                    map[i_key+1][j_key-1]=map[i_key][j_key]+1
                    newArr.append([i_key+1,j_key-1]) 

            if(0<=i_key-1<=heightBoundary and 0<=j_key-1<=widthBoundary):
                if (map[i_key-1][j_key-1]==0):# upper left
                    map[i_key-1][j_key-1]=map[i_key][j_key]+1
                    newArr.append([i_key-1,j_key-1])
        
        return self.fillMatrix(map,newArr) 

    #This function checks if there are negative indices
    def checker_index_negative(self,i,j):
        if i<0 or j<0:
            return -1

        #This function gets the shortest path from the start to the goal
    def shortest_path(self,matrix,start,start_2):
        #Create list of neighbours
        list_neighbours=[]
        list_neighbours_2=[]
        #Create list of tuples for the indices of elements of path taken(included start and goal indices)
        list_tuples=[]
        #Acts as a flag when goal is found 
        goalfound=0    
        #Assign start and end indices to i&j    
        i=start
        j=start_2
        # Make a tuple to add to list
        mytuple = (i,j)
        # Append it to the list
        list_tuples.append(mytuple)
        #Loop while goal not found
        while (goalfound)==0:
        #If goal found break the while loop
            if(matrix[i][j]==2):
                goalfound=1
                break
        #Get neighbours and check for each if the index is negative (out of boundaries)
            checker=self.checker_index_negative(i-1,j)
            if(checker!=-1):
                upper=matrix[i-1][j] 
                list_neighbours.append(upper)
            else:
                upper=0

            checker=self.checker_index_negative(i,j+1)
            if(checker!=-1):
               right=matrix[i][j+1] 
               list_neighbours.append(right)
            else:
               right=0

            checker=self.checker_index_negative(i+1,j)
            if(checker!=-1):
               lower=matrix[i+1][j]    
               list_neighbours.append(lower)
            else:
               lower=0
            checker=self.checker_index_negative(i,j-1)
            if(checker!=-1):
               left=matrix[i][j-1]
               list_neighbours.append(left)
            else:
               left=0

            checker=self.checker_index_negative(i-1,j+1)
            if(checker!=-1):
               upperright=matrix[i-1][j+1]
               list_neighbours.append(upperright)
            else:
               upperright=0

            checker=self.checker_index_negative(i+1,j+1)
            if(checker!=-1):
               lowerright=matrix[i+1][j+1]
               list_neighbours.append(lowerright)
            else:
               lowerright=0
            checker=self.checker_index_negative(i+1,j-1)
            if(checker!=-1):
               lowerleft=matrix[i+1][j-1]
               list_neighbours.append(lowerleft)
            else:
               lowerleft=0

            checker=self.checker_index_negative(i-1,j-1)
            if(checker!=-1):
               upperleft=matrix[i-1][j-1]
               list_neighbours.append(upperleft)
            else:
               upperleft=0

        #Loop over list of neighbours and execludes the ones(obstacles)
            for k in range(len(list_neighbours)):
             if list_neighbours[k]!=1:
                list_neighbours_2.append(list_neighbours[k])

            min_val=-1
        #Get the minimium the neighbours to all neighbours except the ones(obstacles)
            min_val=min(list_neighbours_2)
        #The upper is the minimium 
            if (upper==min_val):
             i=i-1
             j=j
            #list_tuples=list(zip(i, j))
            # Make a tuple to add to list
             mytuple = (i,j)
            # Append it to the list
             list_tuples.append(mytuple)
        #The right is the minimium 
            elif(right==min_val):
             i=i
             j=j+1
            #list_tuples=list(zip(i, j))
            # Make a tuple to add to list
             mytuple = (i,j)
            # Append it to the list
             list_tuples.append(mytuple)
        #The lower is the minimium 
            elif(lower==min_val):
             i=i+1
             j=j
            #list_tuples=list(zip(i, j))
            # Make a tuple to add to list
             mytuple = (i,j)
            # Append it to the list
             list_tuples.append(mytuple)
        #The left is the minimium 
            elif(left==min_val):
              i=i
              j=j-1
            #list_tuples=list(zip(i, j))
            # Make a tuple to add to list
              mytuple = (i,j)
            # Append it to the list
              list_tuples.append(mytuple)
        #The upperright is the minimium 
            elif(upperright==min_val):
              i=i-1
              j=j+1
            #list_tuples=list(zip(i, j))
            # Make a tuple to add to list
              mytuple = (i,j)
            # Append it to the list
              list_tuples.append(mytuple)
        #The lowerright is the minimium 
            elif(lowerright==min_val):
               i=i+1
               j=j+1
            #list_tuples=list(zip(i, j))
            # Make a tuple to add to list
               mytuple = (i,j)
            # Append it to the list
               list_tuples.append(mytuple)
        #The lowerleft is the minimium 
            elif(lowerleft==min_val):
               i=i+1
               j=j-1
            #list_tuples=list(zip(i, j))
            # Make a tuple to add to list
               mytuple = (i,j)
            # Append it to the list
               list_tuples.append(mytuple)
        #The upperleft is the minimium 
            elif(upperleft==min_val):
              i=i-1
              j=j-1
            #list_tuples=list(zip(i, j))
            # Make a tuple to add to list
              mytuple = (i,j)
            # Append it to the list
              list_tuples.append(mytuple)
        #Return list of tuples for indices of my path
        return list_tuples  

# def shortest_path(matrix,start,end):
    
#     list_neighbours=[]
#     list_neighbours_2=[]
#     list_tuples=[]

#     goalfound=0        
#     i=start
#     j=end
#     # Make a tuple to add to list
#     mytuple = (i,j)
#     # Append it to the list
#     list_tuples.append(mytuple)
#     while (goalfound)==0:
#      cn=0
#      if(matrix[i][j]==2):
#       goalfound=1
#       # Make a tuple to add to list
#       # Append it to the list
#       break
#      try:
#       upper=matrix[i-1][j]  
#       list_neighbours.append(upper)
#      except:
#       upper=0
#      try:
#       right=matrix[i][j+1] 
#       list_neighbours.append(right)
#      except:
#       right=0
#      try:
#       lower=matrix[i+1][j]    
#       list_neighbours.append(lower)
#      except:
#       lower=0
#      try:
#       left=matrix[i][j-1]
#       list_neighbours.append(left)
#      except:
#       left=0
#      try:
#       upperright=matrix[i-1][j+1]
#       list_neighbours.append(upperright)
#      except:
#       upperright=0
#      try:
#       lowerright=matrix[i+1][j+1]
#       list_neighbours.append(lowerright)
#      except:
#       lowerright=0
#      try:
#       lowerleft=matrix[i+1][j-1]
#       list_neighbours.append(lowerleft)
#      except:
#       lowerleft=0
#      try:
#       upperleft=matrix[i-1][j-1]
#       list_neighbours.append(upperleft)
#      except:
#       upperleft=0

#      for k in range(len(list_neighbours)):
#        if list_neighbours[k]!=1:
#          list_neighbours_2.append(list_neighbours[k])
#      min_val=0
#      min_val=min(list_neighbours_2)
     
#      if (upper==min_val):
#         i=i-1
#         j=j
#         # Make a tuple to add to list
#         mytuple = (i,j)
#         # Append it to the list
#         list_tuples.append(mytuple)
#      elif(right==min_val):
#         i=i
#         j=j+1
#         # Make a tuple to add to list
#         mytuple = (i,j)
#         # Append it to the list
#         list_tuples.append(mytuple)
#      elif(lower==min_val):
#         i=i+1
#         j=j
#         # Make a tuple to add to list
#         mytuple = (i,j)
#         # Append it to the list
#         list_tuples.append(mytuple)
#      elif(left==min_val):
#         i=i
#         j=j-1
#         # Make a tuple to add to list
#         mytuple = (i,j)
#         # Append it to the list
#         list_tuples.append(mytuple)
#      elif(upperright==min_val):
#         i=i-1
#         j=j+1
#         # Make a tuple to add to list
#         mytuple = (i,j)
#         # Append it to the list
#         list_tuples.append(mytuple)
#      elif(lowerright==min_val):
#         i=i+1
#         j=j+1
#         #list_tuples=list(zip(i, j))
#         # Make a tuple to add to list
#         mytuple = (i,j)
#         # Append it to the list
#         list_tuples.append(mytuple)
#      elif(lowerleft==min_val):
#         i=i+1
#         j=j-1
#         #list_tuples=list(zip(i, j))
#         # Make a tuple to add to list
#         mytuple = (i,j)
#         # Append it to the list
#         list_tuples.append(mytuple)
#      elif(upperleft==min_val):
#         i=i-1
#         j=j-1
#         #list_tuples=list(zip(i, j))
#         # Make a tuple to add to list
#         mytuple = (i,j)
#         # Append it to the list
#         list_tuples.append(mytuple)
      
#     return list_tuples



if __name__ == "__main__"  :
 #i_start=int(input("enter start row: "))
 #j_start=int(input("enter start col: "))
 run=Wavefront()