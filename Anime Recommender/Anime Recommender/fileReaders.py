my_ratings = []
recommendations=[]

def read_my_ratings(filename):
    my_ratings = []
    with open(filename, 'r', encoding='utf8') as f:
        line = f.readline()
        line = f.readline()
        while line!=None and line!='':
            line = line.split('^',1)
            line[0] = line[0].strip(' \n')
            line[1] = int(line[1].strip(' \n'))
            my_ratings.append(line)
            line = f.readline()

    return my_ratings


def read_my_recommendations(filename,my_animes,num_of_recommendations):  
    recommendations = []  
    with open(filename, 'r', encoding='utf8') as f:
        f.readline()
        # Read and print the entire file line by line
        for i in range(len(my_animes)+num_of_recommendations):
            line = f.readline()
            line = line.split('^',1)
            if float(line[1].strip('\n'))<0:
                break
            else:
                doappend = True
                for i in range(0,len(my_animes)):
                    if my_animes[i][0] == line[0]:
                        doappend = False
                        break
                if doappend:
                    recommendations.append(line[0])
    
    return recommendations

def read_list_of_animes(filename):
    animes = []
    with open(filename, 'r', encoding='utf8') as f:
        line = f.readline()
        while line!=None and line!='':
            animes.append(line)
            line = f.readline()


    return animes        
                    

'''
#Tests for functions
-----------------------

my_ratings = read_my_ratings("my_ratings.txt")
print(my_ratings)

recommendations = read_my_recommendations("Recommendations.csv",my_ratings)
print(recommendations)

my_animes = read_list_of_animes("animetitles.csv")
print(my_animes)'''