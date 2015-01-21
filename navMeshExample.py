# ----------------------------------------------------------------------------
# jerdin@yandex.ru
# http://creativecommons.org/licenses/by/4.0/
# ----------------------------------------------------------------------------

import sys
import random
import zipfile
from PIL import Image, ImageDraw
from NavMeshReader import NavMeshReader

(imageWidth,imageHeight)=(1024,1024)
imageBorder=25

im = Image.new("RGB", (imageWidth, imageHeight))

imageWidth -= imageBorder*2
imageHeight -= imageBorder*2

pdraw = ImageDraw.Draw(im)

# Get raw navmesh from zipped chunk file and parse it
zf = zipfile.ZipFile(sys.argv[1])
bytes = zf.read("worldNavmesh")

navMesh=NavMeshReader(bytes)

zf.close()

#Calculate scale to fit all coordinates in resulting picture
elv = navMesh.polygons[0].elevation
boundsX = navMesh.polygons[0].edges[0]
boundsX = (boundsX[0],boundsX[0])
boundsY = navMesh.polygons[0].edges[0]
boundsY = (boundsY[1],boundsY[1])

for line in navMesh.polygons:
	elv=( min(elv[0],line.elevation[0]), max(elv[1],line.elevation[1]) )
	for key in line.edges: 
		boundsX=( min(boundsX[0],key[0]), max(boundsX[1],key[0]) )
		boundsY=( min(boundsY[0],key[1]), max(boundsY[1],key[1]) )

scaleX=(boundsX[1]-boundsX[0])
shiftX=boundsX[0]

scaleY=(boundsY[1]-boundsY[0])
shiftY=boundsY[0]

#Extract vertice data, scale it and draw polygon with new coordinates
for line in navMesh.polygons: 
	vertices=[]
	for key in line.edges: vertices.append( (int((key[0]-shiftX)*imageWidth/scaleX) +imageBorder,imageHeight-int((key[1]-shiftY)*imageHeight/scaleY) + imageBorder) )
	r1=random.randrange(50,250)
	r2=random.randrange(50,250)
	r3=random.randrange(50,250)
	step=((((line.elevation[0]+line.elevation[1])/2.0)-elv[0])/(elv[1]-elv[0]))
	r=(int(255*step),0,int(255-255*step),255)
#	print("Vertices to Draw: %s" % vertices)
	pdraw.polygon(vertices, fill=r, outline=(r1,r2,r3,255))

im.save("%s.png" % sys.argv[1], "PNG")