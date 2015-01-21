# ----------------------------------------------------------------------------
# jerdin@yandex.ru
# http://creativecommons.org/licenses/by/4.0/
# ----------------------------------------------------------------------------
# BW worldNavmesh format:
# [Block start]
#  [Block header]
#   DWORD: header, unknown 4 zero-bytes
#   FLOAT: girth
#   DWORD: Number of polygons in current block
#   DWORD: Number of vertices in current block
#  [Block header length 16 bytes]
#
#  [Polygons:]
#   FLOAT: minimal elevation
#   FLOAT: maximal elevation
#   DWORD: number of edges
#  [Polygons: 12 bytes*number of polygons]
#
#  [Edges: ]
#   FLOAT: X value
#   FLOAT: Y value
#   DWORD: adjacent polygon index, 0xFFFF0000 for other chunk, 0xFFFFFFFF for empty space
#  [Edges: 12 bytes*number of edges, for each polygon]
# [Block end]
#   
# One file can contain multiple blocks
# ----------------------------------------------------------------------------
import struct

class NavMeshPolygon(object):
	def __init__( self, data ):
		self.elevation=(data[0],data[1])
		self.edges=[]
		self.edgesCount=data[2]
	# End edgesCount function

# End class NavMeshPolygon 

class NavMeshReader(object):
	"""
	Class reading NavMesh data from buffer
	data=NavMeshReader( bytes ) # get whole data from buffer
	poly=data.polygons[5] # get polygon
	(x,y,adjacentIndex)=poly.edge[0] #get edge vertice
	"""
	def __init__( self, inp, bufLen=-1 ):
		self.fmt = '=ffL'
		self.fmtHeader = '=ffLL'
		self.offset = 0
		self.numPolys=0
		self.polygons=[]
		maxOffset=len( inp ) if bufLen<0 else bufLen
		self.parse( inp )

		while self.offset<maxOffset: self.parse( inp ) #parse moar one time if need
	#End __init__ function

	def parse( self, inp ):

		(header,girth,numPolys,numVerts)=self.readBlock(inp, self.fmtHeader)

		for i in range(numPolys):
			data=self.readBlock(inp, self.fmt)
			self.polygons.append(NavMeshPolygon(data))

		for poly in self.polygons[self.numPolys:]:
			for i in range( poly.edgesCount ):
				edge=self.readBlock(inp, self.fmt)
				poly.edges.append(edge)
		self.numPolys += numPolys
	# End parse function

	def readBlock( self, bytes, fmt ):
		structSize = struct.calcsize(fmt)
		data = struct.unpack(fmt, bytes[self.offset:self.offset+structSize])
		self.offset += structSize
		return data
	# End readBlock function

# End class navMeshReader 
