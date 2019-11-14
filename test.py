# test for recursive call

#print(int(9/2))

def recur(array):

    #print(len(a))
    if len(array)==1:
        return array[0]
    else:
        array = array[:-1]
        return recur(array)



b = recur([5,2,4])
print(b)

print(str(4))
