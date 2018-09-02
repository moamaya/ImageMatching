""" Marlo Amaya, Peoplesoft ID: 1091324
    Program #4: Part 1 Finding 9 close images
    COSC 1306, Summer 2017
    This program scans through jpg files used by image_path.py to print a table with images close to a query img"""




def image_histogram(im):
    from PIL import Image
    import numpy as np
    
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
    distance = float(((distance)**(1/2)))
    #print(distance)
    return distance

