from scipy.io import loadmat


data=loadmat('maze.mat')
mazemap=data['map']

#def planner(map, start_row, start_column):   
def planner(map):
    i_goal=-1
    j_goal=-1
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if (map[i][j]==2):
                i_goal=i
                j_goal=j 
                break      
    fillmatrix(map,i_goal,j_goal,0) 

def fillmatrix(map,i_key,j_key,iteration):
    # finished=1 # no spaces to fill
    counter=0
    Indecies=[]
    # if (zerosFound(map)):
    #     pass
    # else:
    #     return map

    if (map[i_key-1][j_key]==0):# upper
         map[i_key-1][j_key]=map[i_key][j_key]+1
         counter+=1
         Indecies.append([i_key-1,j_key])

    if (map[i_key][j_key+1]==0):# right
         map[i_key][j_key+1]=map[i_key][j_key]+1
         counter+=1
         Indecies.append([i_key,j_key+1]) 

    if (map[i_key+1][j_key]==0):# down
         map[i_key+1][j_key]=map[i_key][j_key]+1
         counter+=1
         Indecies.append([i_key+1,j_key]) 

    if (map[i_key][j_key-1]==0):# left
         map[i_key][j_key-1]=map[i_key][j_key]+1
         counter+=1
         Indecies.append([i_key,j_key-1])

    if (map[i_key-1][j_key+1]==0):# upper right
         map[i_key-1][j_key+1]=map[i_key][j_key]+1
         counter+=1
         Indecies.append([i_key-1,j_key+1]) 

    if (map[i_key+1][j_key+1]==0):# lower right
         map[i_key+1][j_key+1]=map[i_key][j_key]+1
         counter+=1
         Indecies.append([i_key+1,j_key+1])

    if (map[i_key+1][j_key-1]==0):# lower left
         map[i_key+1][j_key-1]=map[i_key][j_key]+1
         counter+=1
         Indecies.append([i_key+1,j_key-1]) 

    if (map[i_key-1][j_key-1]==0):# upper left
         map[i_key-1][j_key-1]=map[i_key][j_key]+1
         counter+=1
         Indecies.append([i_key-1,j_key-1])

    # if (counter==0):
    #     return map
    if (iteration==0):
        fillmatrix(map,i_key-1,j_key,1) # up of the goal

    if (iteration==1):
        fillmatrix(map,i_key+1,j_key+1,2) # right of the goal   
  
    if (iteration==2):
        fillmatrix(map,i_key+1,j_key-1,3) # down of the goal

    if (iteration==3):
        fillmatrix(map,i_key-1,j_key-1,4) # left of the goal 

    if (iteration==4):
        fillmatrix(map,i_key-1,j_key+2,5) # upper right of the goal 

    if (iteration==5):
        fillmatrix(map,i_key+2,j_key,6) # lower right of the goal

    if (iteration==6):
        fillmatrix(map,i_key,j_key-2,7) # lower left of the goal 

    if (iteration==7):
        fillmatrix(map,i_key-2,j_key,8) # upper left of the goal

    if (iteration==8):
        fillmatrix(map,i_key,j_key-2,0) # upper left of the goal
    # for i in range(map.shape[0]):
    #     for j in range(map.shape[1]):
    #         if (map[i][j]==0):
    #             finished=0 # space found
    #             break

    # while (finished==0):

    #     for i in range(map.shape[0]):
    #         for j in range(map.shape[1]):
    #             if (map[i][j]==0):
    #                 finished=0

    #     if (((i_key-1)<0) or ((i_key+1)>map.shape[0]-1) or ((j_key+1)>map.shape[1]-1) or ((j_key-1)<0)):# ):#no upper bec out of boundaries
    #         pass
    # for i in range(1,map.shape[0]):
    #     for j in range(1,map.shape[1]):



def zerosFound(map):
    counter=0
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if (map[i][j]==0):
                counter+=1 # space found
                break
    if (counter==0):            
        return 0
    else:
        return 1                

planner(mazemap)    