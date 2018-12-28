from PIL import Image
import scipy
import scipy.cluster
import scipy.misc
from pprint import pprint
from base64 import b16encode
import requests

def extract(url):
  basewidth = 200
  img = Image.open(requests.get(url, stream=True).raw)
  wpercent = (basewidth/float(img.size[0]))
  hsize = int((float(img.size[1])*float(wpercent)))
  img = img.resize((basewidth,hsize), Image.ANTIALIAS)

  NUM_CLUSTERS = 5

  # Convert image into array of values for each point.
  ar = scipy.misc.np.asarray(img)
  shape = ar.shape

  # Reshape array of values to merge color bands.
  if len(shape) > 2:
      ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

  # Get NUM_CLUSTERS worth of centroids.
  codes, _ = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)

  # Pare centroids, removing blacks and whites and shades of really dark and really light.
  # original_codes = codes
  # for low, hi in [(60, 200), (35, 230), (10, 250)]:
  #   codes = scipy.array([code for code in codes 
  #                          if not ((code[0] < low and code[1] < low and code[2] < low) or
  #                                  (code[0] > hi and code[1] > hi and code[2] > hi))])
  #   if not len(codes): codes = original_codes
  #   else: break

  # Assign codes (vector quantization). Each vector is compared to the centroids
  # and assigned the nearest one.
  vecs, _ = scipy.cluster.vq.vq(ar, codes)

  # Count occurences of each clustered vector.
  counts, bins = scipy.histogram(vecs, len(codes))
  total = scipy.sum(counts)
  codes = codes.astype(int).tolist()
  indices = sorted(range(len(counts)), key=counts.__getitem__, reverse=True)
  print(codes)
  print(indices)
  print('dominant colors:')
  for index in indices:
    code = codes[index]
    print(','.join(str(c) for c in code))

  return [codes[index] for index in indices]

