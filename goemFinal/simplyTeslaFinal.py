#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.12.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
sys.path.insert(0, r'/home/nikita/obj_tesla_valve/geom')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

# если half=0.5, создается половина геомтрии. Если half=1 создается полная геометрия
half = 0.5
#условия для создания сетки
if half == 0.5:
  mesh_half = 1
else:
  mesh_half = 0

# плотность сетки
max_size = 40
#size_special = min_size * 1.1
#NumOfSegments = 50
#max_size = 75
size_special = max_size * 0.5
min_size = size_special * 0.5

# Ширина канала
w = 500 #mkm

# Угол наклона уха
alpha = 22.5

# кол-во "ушек"
numSteps = 2

# r1 - внешний радиус, r2 - внутренний радиус
r1 = 3 * w
r2 = 2 * w

# шаг для уха
step = 2 * r1 / math.sin(alpha * math.pi/180)

# Длина основного канала
L = numSteps * 2 * step + w * 20


# размер бокса по X
box_mesh_X = w / math.sin(alpha*math.pi/180.0)

# внешнее ухо
sk = geompy.Sketcher2D()
sk.addPoint(0, 0)
sk.addArcAngleRadiusLength(alpha, r1, 180)
sk.addSegmentY(0)
sk.close()
Sketch_1 = sk.wire(geompy.MakeMarker(0, 0, 0, 1, 0, 0, 0, 1, 0))

# внутреннее ухо
sk = geompy.Sketcher2D()
sk.addPoint(
  w * math.cos(math.pi/2 + alpha * math.pi/180),
  w * math.sin(math.pi/2 + alpha * math.pi/180)
)

sk.addArcAngleRadiusLength(alpha, r2, 180.000000)
sk.addSegmentAngleY(0, 0)
sk.close()
Sketch_2 = sk.wire(geompy.MakeMarker(0, 0, 0, 1, 0, 0, 0, 1, 0))

# первое ухо
simply_tesla = geompy.MakeFuseList(
  [
    geompy.MakeFaceWires([Sketch_1, Sketch_2], 1),
    geompy.MakeTranslation(
      geompy.MakeFaceHW(L, w, 1),
      L * 0.5 - step,
      - w * 0.5,
      0
    )
  ],
  True
  )

# ось отражения для случаев когда кол-во "ушек" > 1
Line_1 = geompy.MakeLineTwoPnt(
    geompy.MakeVertex(0, -w * 0.5, 0),
    geompy.MakeVertex(w, -w * 0.5, 0)
    )
geompy.addToStudy( simply_tesla, 'simply_tesla')
# копипаст ушей
first = geompy.MakeFaceWires([Sketch_1, Sketch_2], 1)

simply_tesla_num = geompy.MakeFuseList(
  [
    geompy.MakeTranslation(first, (2 * step)*i , 0, 0)
    for i in range(numSteps)
  ]
  +
  [
    geompy.MakeMirrorByAxis(
      geompy.MakeTranslation(first, (2 * step)*(i + 0.5), 0, 0),
      Line_1
    )
    for i in range(numSteps)
  ]
  +
  [
    geompy.MakeTranslation(
      geompy.MakeFaceHW(L, w, 1),
      #L * 0.5 - step * 1.75,
      L * 0.5 - (step + w * 10),
      - w * 0.5,
      0
    )
  ],
  True, True
)

tesla_valve = geompy.MakePrismVecH(simply_tesla_num, OZ, w * half)
geompy.addToStudy( tesla_valve, 'tesla_valve1')

#сглаживание
filletIDs1 = []
filletIDs2 = []
filletIDs3 = []
filletIDs4 = []
for i in range(numSteps):
    filletIDs1.append(geompy.GetShapesOnBoxIDs(
        geompy.MakeTranslation(
            geompy.MakeBox(
                -step - 1,
                1,
                w + 1,
                -step + 1,
                -1,
                -w - 1
            ),
            (2 * step)*i , 0, 0),
        tesla_valve,
        geompy.ShapeType["EDGE"],
        GEOM.ST_IN
    )
    )
    filletIDs2.append(geompy.GetShapesOnBoxIDs(
        geompy.MakeMirrorByAxis(
                geompy.MakeTranslation(
                    geompy.MakeBox(
                       -step - 1,
                        w * 0.01,
                        w + 1,
                        -step + 1,
                        -w * 0.01,
                        -w - 1
                    ),
                    (2 * step)*(i + 0.5),
                    0,
                    0
                ),
                Line_1
            ),
        tesla_valve,
        geompy.ShapeType["EDGE"],
        GEOM.ST_IN
    )
    )

#test = geompy.MakeBox(
                #-step - w * 0.01,
                #w * 0.01,
                #w + w * 0.01,
                #w * 0.01,
                #-w * 0.01,
                #-w - w * 0.01
            #)


#testIDs = geompy.GetShapesOnBox(geompy.MakeBox(
                #-step - w * 0.01,
                #w * 0.01,
                #w + w * 0.01,
                #w * 0.01,
                #-w * 0.01,
                #-w - w * 0.01
            #),tesla_valve,
        #geompy.ShapeType["EDGE"],
        #GEOM.ST_IN
    #)
##print(testIDs)
#for i in range(len(testIDs)):
    #geompy.addToStudy( testIDs[i], 'testIDs' + str(i))


filletIDs = []
filletIDsForSolution = []

for filletIDs1 in filletIDs1:
    filletIDs += filletIDs1
for filletIDs2 in filletIDs2:
    filletIDs += filletIDs2


tesla_valve = geompy.MakeFillet(
    tesla_valve,
    #w * 10,
    2 * r1,
    geompy.ShapeType["EDGE"],
    filletIDs
    )

for i in range(numSteps):
    filletIDs3.append(geompy.GetShapesOnBoxIDs(
        geompy.MakeTranslation(
            geompy.MakeBox(
                -step - w * 0.01,
                w * 0.01,
                w + w * 0.01,
                w * 0.01,
                -w * 0.01,
                -w - w * 0.01
            ),
            (2 * step)*i , 0, 0),
        tesla_valve,
        geompy.ShapeType["EDGE"],
        GEOM.ST_IN
    )
    )

    filletIDs4.append(geompy.GetShapesOnBoxIDs(
        geompy.MakeMirrorByAxis(
                geompy.MakeTranslation(
                    geompy.MakeBox(
                       -step - w * 0.01,
                        w * 0.01,
                        w + w * 0.01,
                        w * 0.01,
                        -w * 0.01,
                        -w - w * 0.01
                    ),
                    (2 * step)*(i + 0.5),
                    0,
                    0
                ),
                Line_1
            ),
        tesla_valve,
        geompy.ShapeType["EDGE"],
        GEOM.ST_IN
    )
    )

for filletIDs3 in filletIDs3:
    filletIDsForSolution += filletIDs3
for filletIDs4 in filletIDs4:
    filletIDsForSolution += filletIDs4

tesla_valve = geompy.MakeFillet(
    tesla_valve,
    w * 0.04,
    geompy.ShapeType["EDGE"],
    filletIDsForSolution
    )

# геометрические группы
[wall_b] =\
    geompy.GetShapesOnPlaneWithLocation(
        tesla_valve,
        geompy.ShapeType["FACE"],
        geompy.MakeVectorDXDYDZ(0, 0, 1),
        geompy.MakeVertex(0, 0, 0),
        GEOM.ST_ON
    )

[wall_f] =\
    geompy.GetShapesOnPlaneWithLocation(
        tesla_valve,
        geompy.ShapeType["FACE"],
        geompy.MakeVectorDXDYDZ(0, 0, 1),
        geompy.MakeVertex(0, 0, w * half),
        GEOM.ST_ON
    )

[ent] =\
    geompy.GetShapesOnPlaneWithLocation(
        tesla_valve,
        geompy.ShapeType["FACE"],
        geompy.MakeVectorDXDYDZ(1, 0, 0),
        geompy.MakeVertex(- (step + w * 10), 0, 0),
        GEOM.ST_ON
    )

[out] =\
    geompy.GetShapesOnPlaneWithLocation(
        tesla_valve,
        geompy.ShapeType["FACE"],
        geompy.MakeVectorDXDYDZ(1, 0, 0),
        geompy.MakeVertex(((numSteps * 2) - 1) * step + w * 10, 0, 0),
        GEOM.ST_ON
    )

# получение ID объектов для вычета их из построения вязкого подслоя сетки
# направлением для нормали будет ось Х
ent_ID =\
    geompy.GetShapesOnPlaneWithLocation(
        ent,
        geompy.ShapeType["FACE"],
        geompy.MakeVectorDXDYDZ(1, 0, 0),
        geompy.MakeVertex(- (step + w * 10), 0, 0),
        GEOM.ST_ON
    )
out_ID =\
    geompy.GetShapesOnPlaneWithLocation(
        out,
        geompy.ShapeType["FACE"],
        geompy.MakeVectorDXDYDZ(1, 0, 0),
        geompy.MakeVertex(((numSteps * 2) - 1) * step + w * 10, 0, 0),
        GEOM.ST_ON
    )

wall_f_ID =\
    geompy.GetShapesOnPlaneWithLocation(
        wall_f,
        geompy.ShapeType["FACE"],
        geompy.MakeVectorDXDYDZ(0, 0, 1),
        geompy.MakeVertex(0, 0, w * 0.5),
        GEOM.ST_ON
    )

list_ID =\
    [
        geompy.GetSubShapeID(tesla_valve, ent_ID[0]),
        geompy.GetSubShapeID(tesla_valve, out_ID[0]),
        geompy.GetSubShapeID(tesla_valve, wall_f_ID[0])
    ]

# зона усложненной сетки
simply_box = geompy.MakeFuseList(
    [
        geompy.MakeCylinder(
            geompy.MakeVertex(0, 0, -0.5 * w), # базовая точка
            geompy.MakeVectorDXDYDZ(0, 0, 1), # вектор
            box_mesh_X, # радиус
            w * 2 # высота
        ),
        geompy.MakeCylinder(
            geompy.MakeVertex(-(2 * r1 / math.sin(alpha * math.pi/180) - 0.5 * w / math.sin(alpha * math.pi/180)), 0, -0.5 * w), # базовая точка
            geompy.MakeVectorDXDYDZ(0, 0, 1), # вектор
            box_mesh_X, # радиус
            w * 2
        )
    ],
    True,
    True
    )

simply_box_num = geompy.MakeFuseList(
  [
    geompy.MakeTranslation(simply_box, (2 * step)*i , 0, 0)
    for i in range(numSteps)
  ]
  +
  [
    geompy.MakeTranslation(simply_box, (2 * step)*(i + 0.5), 0, 0)
    for i in range(numSteps)
  ],
  True
  )

geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Sketch_1, 'Sketch_1' )
geompy.addToStudy( Sketch_2, 'Sketch_2' )
geompy.addToStudy( simply_tesla_num, 'simply_tesla_num')
geompy.addToStudy( tesla_valve, 'tesla_valve')
geompy.addToStudyInFather( tesla_valve, wall_f, 'wall_f')
geompy.addToStudyInFather( tesla_valve, wall_b, 'wall_b')
geompy.addToStudyInFather( tesla_valve, ent, 'ent')
geompy.addToStudyInFather( tesla_valve, out, 'out')
geompy.addToStudy( simply_box, 'simply_box')
geompy.addToStudy( simply_box_num, 'simply_box_num')

##
## SMESH component
##

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
#smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                 # multiples meshes built in parallel, complex and numerous mesh edition (performance)

NETGEN_3D_Parameters_2 = smesh.CreateHypothesisByAverageLength( 'NETGEN_Parameters', 'NETGENEngine', 3651.37, 0 )
Viscous_Layers_2 = smesh.CreateHypothesis('ViscousLayers')
#Viscous_Layers_2.SetTotalThickness( 1 )
#Viscous_Layers_2.SetNumberLayers( 2 )
#Viscous_Layers_2.SetStretchFactor( 1.1 )
#Viscous_Layers_2.SetMethod( smeshBuilder.NODE_OFFSET )
#Viscous_Layers_2.SetFaces( [], 1 )
#NETGEN_1D_2D_3D_1 = smesh.CreateHypothesis( "NETGEN_2D3D" )
Mesh_2 = smesh.Mesh(tesla_valve,'Mesh_2')
NETGEN_1D_2D = Mesh_2.Triangle(algo=smeshBuilder.NETGEN_1D2D)
NETGEN_2D_Parameters_1 = NETGEN_1D_2D.Parameters()
NETGEN_2D_Parameters_1.SetMaxSize( max_size )
NETGEN_2D_Parameters_1.SetMinSize( min_size )
NETGEN_2D_Parameters_1.SetSecondOrder( 0 )
NETGEN_2D_Parameters_1.SetOptimize( 1 )
NETGEN_2D_Parameters_1.SetFineness( 5 )
NETGEN_2D_Parameters_1.SetGrowthRate( 0.015 )
NETGEN_2D_Parameters_1.SetNbSegPerEdge( 2 )
NETGEN_2D_Parameters_1.SetNbSegPerRadius( (w * 0.04) // 5 )
NETGEN_2D_Parameters_1.SetChordalError( -1 )
NETGEN_2D_Parameters_1.SetChordalErrorEnabled( 0 )
NETGEN_2D_Parameters_1.SetUseSurfaceCurvature( 1 )
NETGEN_2D_Parameters_1.SetNbSurfOptSteps( 5 )
NETGEN_2D_Parameters_1.SetFuseEdges( 1 )
NETGEN_2D_Parameters_1.SetQuadAllowed( 0 )
NETGEN_2D_Parameters_1.SetLocalSizeOnShape(simply_box_num, size_special)
#NETGEN_2D_Parameters_1.SetWorstElemMeasure( 25590 )
#NETGEN_2D_Parameters_1.SetUseDelauney( 32 )
NETGEN_2D_Parameters_1.SetCheckChartBoundary( 10 )
NETGEN_3D = Mesh_2.Tetrahedron()
NETGEN_3D_Parameters_1_1 = NETGEN_3D.Parameters()
NETGEN_3D_Parameters_1_1.SetMaxSize( max_size )
NETGEN_3D_Parameters_1_1.SetMinSize( min_size )
NETGEN_3D_Parameters_1_1.SetOptimize( 1 )
NETGEN_3D_Parameters_1_1.SetFineness( 5 )
NETGEN_3D_Parameters_1_1.SetGrowthRate( 0.015 )
NETGEN_3D_Parameters_1_1.SetLocalSizeOnShape(simply_box_num, size_special)
NETGEN_3D_Parameters_1_1.SetNbVolOptSteps( 8 )
NETGEN_3D_Parameters_1_1.SetWorstElemMeasure( 3 )
NETGEN_3D_Parameters_1_1.SetElemSizeWeight( 0 )
NETGEN_3D_Parameters_1_1.SetCheckOverlapping( 3 )
NETGEN_3D_Parameters_1_1.SetCheckChartBoundary( 3 )
#Viscous_Layers_3 = NETGEN_3D.ViscousLayers(
    #min_size * 0.5,2,1.3,list_ID,1,smeshBuilder.NODE_OFFSET,'Viscous Layers'
#)
Viscous_Layers_1 = NETGEN_3D.ViscousLayers(min_size * 0.5,2,1.4,list_ID,1,smeshBuilder.NODE_OFFSET)
wall_b_2 = Mesh_2.GroupOnGeom(wall_b,'wall_b',SMESH.FACE)
wall_f_2 = Mesh_2.GroupOnGeom(wall_f,'wall_f',SMESH.FACE)
ent_2 = Mesh_2.GroupOnGeom(ent,'ent',SMESH.FACE)
out_2 = Mesh_2.GroupOnGeom(out,'out',SMESH.FACE)





isDone = Mesh_2.Compute()



#Viscous_Layers = Mesh_2.GetGroups()[ 4 ]
#[ wall_b_2, wall_f_2, ent_2, out_2, Viscous_Layers ] = Mesh_2.GetGroups()

###hyp_13.SetLength( 3651.37 ) ### not created Object
##NETGEN_3D_Parameters_1 = smesh.CreateHypothesisByAverageLength( 'NETGEN_Parameters', 'NETGENEngine', 3651.37, 0 )

##NETGEN_3D_Parameters_1.SetMaxSize( max_size )
##NETGEN_3D_Parameters_1.SetMinSize( min_size )

##NETGEN_3D_Parameters_1.SetSecondOrder( 0 )
##NETGEN_3D_Parameters_1.SetOptimize( 1 )
##NETGEN_3D_Parameters_1.SetFineness( 5 )
##NETGEN_3D_Parameters_1.SetGrowthRate( 0.05 )
##NETGEN_3D_Parameters_1.SetNbSegPerEdge( 3 )
##NETGEN_3D_Parameters_1.SetNbSegPerRadius( 5 )
##NETGEN_3D_Parameters_1.SetChordalError( -1 )
##NETGEN_3D_Parameters_1.SetChordalErrorEnabled( 0 )
##NETGEN_3D_Parameters_1.SetUseSurfaceCurvature( 1 )
##NETGEN_3D_Parameters_1.SetFuseEdges( 1 )
##NETGEN_3D_Parameters_1.SetCheckChartBoundary( 104 )
##NETGEN_3D_Parameters_1.SetQuadAllowed( 0 )
##NETGEN_3D_Parameters_1.SetLocalSizeOnShape(simply_box_num, size_special)
##NETGEN_3D_Parameters_1.UnsetLocalSizeOnEntry("tesla_valve")
##NETGEN_3D_Parameters_1.SetCheckChartBoundary( 3 )
##NETGEN_3D_Parameters_1.UnsetLocalSizeOnEntry("tesla_valve")
##NETGEN_3D_Parameters_1.SetNbSurfOptSteps( 5 )
##NETGEN_3D_Parameters_1.SetNbVolOptSteps( 8 )
##Mesh_1 = smesh.Mesh(tesla_valve,'Mesh_1')
##status = Mesh_1.AddHypothesis( tesla_valve, NETGEN_3D_Parameters_1 )
##NETGEN_1D_2D_3D = Mesh_1.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)

##Viscous_Layers_1 = NETGEN_1D_2D_3D.ViscousLayers(1,1,1,list_ID,1,smeshBuilder.NODE_OFFSET)
##Viscous_Layers_1.SetTotalThickness( min_size * 0.3 )
##Viscous_Layers_1.SetNumberLayers( 2 )
##Viscous_Layers_1.SetStretchFactor( 1.1 )
##Viscous_Layers_1.SetMethod( smeshBuilder.NODE_OFFSET )
##Viscous_Layers_1.SetFaces( list_ID, 1 )

##isDone = Mesh_1.Compute()

##wall_b_1 = Mesh_1.GroupOnGeom(wall_b,'wall_b',SMESH.FACE)
##wall_f_1 = Mesh_1.GroupOnGeom(wall_f,'wall_f',SMESH.FACE)
##ent_1 = Mesh_1.GroupOnGeom(ent,'ent',SMESH.FACE)
##out_1 = Mesh_1.GroupOnGeom(out,'out',SMESH.FACE)
##[ wall_b_1, wall_f_1, ent_1, out_1 ] = Mesh_1.GetGroups()

#### Set names of Mesh objects
##smesh.SetName(NETGEN_1D_2D_3D.GetAlgorithm(), 'NETGEN 1D-2D-3D')
##smesh.SetName(Viscous_Layers_1, 'Viscous Layers_1')
##smesh.SetName(NETGEN_3D_Parameters_1, 'NETGEN 3D Parameters_1')
##smesh.SetName(wall_b_1, 'wall_b')
##smesh.SetName(wall_f_1, 'wall_f')
##smesh.SetName(ent_1, 'ent')
##smesh.SetName(out_1, 'out')
##smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')

#####
##### SMESH component
#####

##import  SMESH, SALOMEDS
##from salome.smesh import smeshBuilder

##smesh = smeshBuilder.New()
###smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:

 ### multiples meshes built in parallel, complex and numerous mesh edition (performance)


##Mesh_1 = smesh.Mesh(tesla_valve,'Mesh_1')
##Regular_1D = Mesh_1.Segment()

### распределение слоев выдавливания
##if mesh_half == 1:
    ##Number_of_Segments_1 = Regular_1D.NumberOfSegments(NumOfSegments // 2, None, [])
    ##Number_of_Segments_1.SetConversionMode( 1 )
    ##Number_of_Segments_1.SetTableFunction( [0, 1, 0.05, 0.25, 0.5, 0.1, 1, 0.1] )

##if mesh_half == 0:
    ##Number_of_Segments_1 = Regular_1D.NumberOfSegments(NumOfSegments,None,[])
    ##Number_of_Segments_1.SetConversionMode( 1 )
    ##Number_of_Segments_1.SetTableFunction( [ 0, 1, 0.05, 0.25, 0.5, 0.1, 0.95, 0.25, 1, 1 ] )

##Prism_3D = Mesh_1.Prism()

##wall_f_1 = Mesh_1.GroupOnGeom(wall_f,'wall_f',SMESH.FACE)
##NETGEN_1D_2D = Mesh_1.Triangle(algo=smeshBuilder.NETGEN_1D2D,geom=wall_f)
##NETGEN_2D_Parameters_1 = NETGEN_1D_2D.Parameters()
##NETGEN_2D_Parameters_1.SetSecondOrder( 0 )
##NETGEN_2D_Parameters_1.SetOptimize( 1 )
##NETGEN_2D_Parameters_1.SetFineness( 5 )
##NETGEN_2D_Parameters_1.SetGrowthRate( 0.01)
##NETGEN_2D_Parameters_1.SetChordalError( -1 )
##NETGEN_2D_Parameters_1.SetChordalErrorEnabled( 0 )
##NETGEN_2D_Parameters_1.SetUseSurfaceCurvature( 1 )
##NETGEN_2D_Parameters_1.SetFuseEdges( 1 )
###NETGEN_2D_Parameters_1.SetQuadAllowed( 1 )

##Viscous_Layers_2D_1 = NETGEN_1D_2D.ViscousLayers2D(1,3,1.1, list_ID,1)
##Viscous_Layers_2D_1.SetTotalThickness( max_size * 0.1 )
##Viscous_Layers_2D_1.SetNumberLayers( 1 )
##Viscous_Layers_2D_1.SetStretchFactor( 1 )
##Viscous_Layers_2D_1.SetEdges(list_ID , 1 )

### плотность сетки
##NETGEN_2D_Parameters_1.SetMinSize( min_size )
##NETGEN_2D_Parameters_1.SetLocalSizeOnShape(simply_box_num, size_special)
##NETGEN_2D_Parameters_1.SetMaxSize( max_size )
##isDone = Mesh_1.Compute()

### группы
##wall_b_1 = Mesh_1.GroupOnGeom(wall_b,'wall_b',SMESH.FACE)
##ent_1 = Mesh_1.GroupOnGeom(ent,'ent',SMESH.FACE)
##out_1 = Mesh_1.GroupOnGeom(out,'out',SMESH.FACE)
##[ wall_f_1, wall_b_1, ent_1, out_1 ] = Mesh_1.GetGroups()
###NETGEN_2D = NETGEN_2D_3.GetSubMesh()

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
