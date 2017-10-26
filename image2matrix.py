#! /usr/bin/python
# -*- coding: utf-8 -*-

from scipy import misc
import glob
import numpy as np
import matplotlib

for image_path in glob.glob("/home/osmaralg/Desktop/RompiBot/oficina.png"):
    image = misc.imread(image_path)
    print (image.shape)
    print (image.dtype)



png = []
for image_path in glob.glob("/home/osmaralg/Desktop/RompiBot/oficina.png"):
    png.append(misc.imread(image_path))    

im = np.asarray(png)

ocupado = []
print 'Importing done...', im.shape

print im 

for i in range(0,800):
    for j in range(0,800):
        if im[0,i,j]<128:
            im[0,i,j]=1
            istr=str(i)
            jstr=str(j)
            dos = istr+jstr
            coordenada = [istr,jstr]
            ocupado.append(coordenada)
        else:
            im[0,i,j]=0

matriz = np.asarray(ocupado)

print "Ocupado:", matriz
