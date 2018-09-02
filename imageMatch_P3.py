

import os, sys, time, re
import multiprocessing
from multiprocessing import Pool
from PIL import Image
import pylab as pl
import numpy as np
import glob
import logging
format= '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s() - %(message)s'
format= '%(asctime)s - %(filename)s:%(lineno)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=format)
logger = logging.getLogger(__name__)

def main():
    from argparse import ArgumentParser
    
    parser = ArgumentParser()
    
    parser.add_argument("-q", "--query", dest="queryImage",
                    help="specify the query image", metavar="QUERY IMAGE NAME")
    parser.add_argument("-d", "--dataset", dest="databaseSearch",
                    help="specify the image dataset to search", metavar="IMAGE DATASET TO SEARCH")
    parser.add_argument("-m", "--multi", dest="multiProcess",
                                        help="specify 1 for multi or 0 for serial processing", metavar="MULTIPROCESS=TRUE")
                            
    args = parser.parse_args()
    mult = args.multiProcess
    
    if args.queryImage is None:
        print("Please specify the name of query image")
        print("use the -h option to see usage information")
        sys.exit(2)
    
    if args.databaseSearch is None:
        print("Please specify the path to image database to search")
        print("use the -h option to see usage information")
        sys.exit(2)

    if args.multiProcess is None:
        print("Please specify 1 for multi or 0 for serial processing")
        print("use the -h option to see usage information")
        sys.exit(2)

    file_filter = args.databaseSearch + ".jpg" # This is the path to database with images to search over
    image_filepath1 = args.queryImage # This is the query image
    image_list = []

    for filename in glob.glob(file_filter): #assuming jpg
        image_list.append(filename)

    image_no = len(image_list) # No. of images in the database
    logger.debug("*"*20)
    logger.debug("Image Search Starting")

    if int(mult) == 1:
        nprocs = multiprocessing.cpu_count()
    else:
        nprocs = 1

    startTime = time.time()

    num_image_per_proc = int(image_no/nprocs)

    startNo = []
    endNo = []
    for i in range(nprocs):
        startNo.append(i*num_image_per_proc)
        endNo.append((i+1)*num_image_per_proc)

    group_len = len(startNo)
    endNo[group_len-1] = image_no

    param1 = []
    param2 = []
    for i in range(nprocs):
        param1.append(image_filepath1)
        param2.append(image_list[startNo[i]:endNo[i]])

    params = zip(param1, param2)

    pool = multiprocessing.Pool()

    if int(mult) == 1:
        sims = pool.map(compute_similarity, params)
    else:
        sims = list(map(compute_similarity, params))

    hash_vals = []
    for i in range(len(sims)):
        hash_vals += list(sims[i])

    matched = list(zip(hash_vals, image_list)) # Create of tuple of distance values and images in the database
    matched.sort() # Sort the tuple by the distance values from lowest to highest
    
    best_matched = matched[0:9] # We are only interested in the top 9 closest matches
    #mark the end time
    endTime = time.time()
    
    workTime = "%0.1f"%((endTime - startTime)*1000)
    logger.debug("Image Search using Histogram  => took %s ms"%( workTime ))

# We want to display the results of the image search
    f = pl.figure()
    pl.clf()
    pl.subplots_adjust(left=.01, right=.99, bottom=.01, top=.91)
    img = Image.open(image_filepath1)
    pl.subplot(5,2,1)
    pl.title('Query Image')
    pl.xticks(())
    pl.yticks(())
    arr = np.asarray(img)
    f.add_subplot(5, 2, 1)
    pl.imshow(arr)

    for items, (a,b) in enumerate(best_matched):
        logger.debug("Image Search found %s with distance %s"%(b, a ))
        pl.subplot(5, 2, items+2)
        pl.title('Similar Image')
        img = Image.open(b)
        pl.xticks(())
        pl.yticks(())
        arr = np.asarray(img)
        f.add_subplot(5, 2, items+2)
        pl.imshow(arr)

    pl.show()
    logger.debug("Image Search Finished")

def compute_similarity(params):
    query, dataset = params
    sim_vals = []
    batch_images = len(dataset)
    for idx in range(0, batch_images):
        image_filepath2 = dataset[idx]
        simdist = image_similarity_histogram(query,image_filepath2)
        sim_vals.append(simdist)
    return sim_vals

def image_similarity_histogram(image_filepath1,image_filepath2):
    from hw_histogram_and_distance import image_histogram
    from hw_histogram_and_distance import euclidean_distance

    image1 = Image.open(image_filepath1)
    image2 = Image.open(image_filepath2)
    
    image1 = get_thumbnail(image1)
    image2 = get_thumbnail(image2)
    
    histogram1 = image_histogram(image1)
    histogram2 = image_histogram(image2)
    
    # use euclidean distance to compare
    dist = euclidean_distance(histogram1,histogram2)

    return dist

def get_thumbnail(image, size=(128,128), stretch_to_fit=False, greyscale=False):
    " get a smaller version of the image - makes comparison much faster/easier"
    if not stretch_to_fit:
        image.thumbnail(size, Image.ANTIALIAS)
    else:
        image = image.resize(size); # for faster computation
    if greyscale:
        image = image.convert("L")  # Convert it to grayscale.
    return image

if __name__ == "__main__":
    main()

