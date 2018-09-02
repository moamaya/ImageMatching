""" Marlo Amaya, Peoplesoft ID: 1091324
    Program #4: Part 2 Finding the 3 lowest values for Euclidean and Hamming distances
    COSC 1306, Summer 2017
    This program scans through jpg files and creates two lists for 20 query images, and compares them to all 1000 images. """


import time

#Path to the images
path = '/Users/MarloAmaya/Library/Mobile Documents/com~apple~CloudDocs/Summer 2017/COSC 1306/HW/Additional Files/PA4/images/images'

startTime = time.time()

def image_histogram(image_path):
    from PIL import Image
    import numpy as np
    im = Image.open(image_path)
    im_vals1 = np.zeros(256)
    im_vals2 = np.zeros(256)
    im_vals3 = np.zeros(256)
    r,g,b = im.split()
    pixels_r = list(r.getdata())
    pixels_g = list(g.getdata())
    pixels_b = list(b.getdata())
    pix_r = np.array(pixels_r)
    pix_g = np.array(pixels_g)
    pix_b = np.array(pixels_b)
    for idx in range (0, len(pix_r)):
        im_vals1[pix_r[idx]] += 1
        im_vals2[pix_g[idx]] += 1
        im_vals3[pix_b[idx]] += 1
    histogram = list(im_vals1) + list(im_vals2) + list(im_vals3)
    return histogram


"""c = image_histogram(path+'/0.jpg')
print('Histogram for querry img is: ',c)
sum = 0
for i in c:
    sum = sum+i
print('Sum is ','=',sum)"""

#list of histograms
def matrix_list(m):
    x = []
    for i in range(m):
        y = image_histogram(path+"/"+str(i)+'.jpg')
        x.append(y)
    return x

#euclidean distance
def euclidean_distance(list1,list2):
    distance = 0
    len1, len2 = len(list1), len(list2)
    if len1 != len2:
        if len1 > len2:
            list1 = list1[:-(len1 - len2)]
        else:
            list2 = list2[:-(len2 - len1)]

    for i in range(len(list2)):
        distance = distance + (list1[i]-list2[i])**2
    distance = float(((distance/len(list2))**(1/2)))
    #print(distance)
    return distance

def hamming(list1,list2):
    count = 0
    len1, len2 = len(list1), len(list2)
    if len1 != len2:
        if len1 > len2:
            list1 = list1[:-(len1 - len2)]
        else:
            list2 = list2[:-(len2 - len1)]

    for i in range(len(list2)):
        if list1[i] != list2[i]:
            count += 1
    #print(count)
    return count



hist = matrix_list(1000)
#Euc_main == the distances of all histograms to the query img
euc_main = []
ham_main = []
query = []
for x in range(0, 1001, 50):
    if x == 0:
        query.append(str(x))
    else:
        query.append(str(x-1))


for j in query:
    j = int(j)
    ham_one = []
    euc_one = []
    for i in range(len(hist)):
        euc_one.append(euclidean_distance(hist[j], hist[i]))
        ham_one.append(hamming(hist[j], hist[i]))

    euc_main.append(euc_one)
    ham_main.append(ham_one)

#Now we sort_all the lists within euc_main and ham_main
sort_eucmain = []
sort_hammain = []
for i in range(len(euc_main)):
    sort_eucmain.append(sorted(euc_main[i]))
    sort_hammain.append(sorted(ham_main[i]))

#Now we get the 3 lowest values of each list, and we skip and value that is 0 since that will be the same image

three_euc = []
three_ham = []

for i in range(len(sort_eucmain)):
    euc1 = []
    ham1 = []
    for j in range(len(sort_eucmain[i])):
        if len(euc1) < 3 and sort_eucmain[i][j] != 0.0 and sort_eucmain[i][j] not in euc1 and sort_hammain[i][j] not in ham1:
            euc1.append(sort_eucmain[i][j])
            ham1.append(sort_hammain[i][j])
    three_euc.append(euc1)
    three_ham.append(ham1)

#Now that the 3 lowest values for each list are in new lists, we can find the locations of each one inn the main lists to be able to get their index number
ham3 = []
euc3 = []
for i in range(len(euc_main)):
    euc3b = []
    ham3b = []
    for j in range(3):
        euc3b.append(euc_main[i].index(three_euc[i][j]))
        ham3b.append(ham_main[i].index(three_ham[i][j]))
    euc3.append(euc3b)
    ham3.append(ham3b)

print('The two lists below are in sets of the 3 lowest values for each query image:')
print(euc3)
print(ham3)

from texttable import Texttable

t = Texttable()

row = [[]]
j = 0
for i in range(0,1001,50):

    if i == 0:
        row.append([str(i)+'.jpg', str(euc3[j]), str(ham3[j])])
    else:
        i = i - 1
        row.append([str(i) + '.jpg', str(euc3[j]), str(ham3[j])])
    j += 1

t.add_rows(row)
t.header(['Query Image','Closest using Euclidean','Closest using Hamming'])

print(t.draw())

endTime = time.time()
workTime = ((endTime - startTime))
print(workTime)