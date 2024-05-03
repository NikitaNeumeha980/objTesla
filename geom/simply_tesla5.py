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
half = 1
#условия для создания сетки
if half == 0.5:
  mesh_half = 1
else:
  mesh_half = 0

# плотность сетки
min_size = 4
max_size = 8
size_special = min_size * 1.1
NumOfSegments = 20


# Ширина канала
w = 100 #mkm

# Угол наклона уха
alpha = 30

# кол-во "ушек"
numSteps = 2

# r1 - внешний радиус, r2 - внутренний радиус
r1 = 3 * w
r2 = 2 * w

# шаг для уха
step = 2 * r1 / math.sin(alpha * math.pi/180)

# Длина основного канала
L = numSteps * step * 2.5


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
    geompy.MakeTranslation(first, (1.25 * step)*i , 0, 0)
    for i in range(numSteps)
  ]
  +
  [
    geompy.MakeMirrorByAxis(
      geompy.MakeTranslation(first, (1.25 * step)*(i + 0.5), 0, 0),
      Line_1
    )
    for i in range(numSteps)
  ]
  +
  [
    geompy.MakeTranslation(
      geompy.MakeFaceHW(L, w, 1),
      L * 0.5 - step * 1.75,
      - w * 0.5,
      0
    )
  ],
  True, True
)

tesla_valve = geompy.MakePrismVecH(simply_tesla_num, OZ, w * half)

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
        geompy.MakeVertex(- step * 1.75, 0, 0),
        GEOM.ST_ON
    )

[out] =\
    geompy.GetShapesOnPlaneWithLocation(
        tesla_valve,
        geompy.ShapeType["FACE"],
        geompy.MakeVectorDXDYDZ(1, 0, 0),
        geompy.MakeVertex(L - step * 1.75, 0, 0),
        GEOM.ST_ON
    )

# получение ID объектов для вычета их из построения вязкого подслоя сетки
# направлением для нормали будет ось Х
ent_ID =\
    geompy.GetShapesOnPlaneWithLocation(
        wall_f,
        geompy.ShapeType["EDGE"],
        geompy.MakeVectorDXDYDZ(1, 0, 0),
        geompy.MakeVertex(- step * 1.75, 0, 0),
        GEOM.ST_ON
    )
out_ID =\
    geompy.GetShapesOnPlaneWithLocation(
        wall_f,
        geompy.ShapeType["EDGE"],
        geompy.MakeVectorDXDYDZ(1, 0, 0),
        geompy.MakeVertex(L - step * 1.75, 0, 0),
        GEOM.ST_ON
    )
list_ID =\
    [
        geompy.GetSubShapeID(tesla_valve, ent_ID[0]),
        geompy.GetSubShapeID(tesla_valve, out_ID[0])
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
    geompy.MakeTranslation(simply_box, (1.25 * step)*i , 0, 0)
    for i in range(numSteps)
  ]
  +
  [
    geompy.MakeTranslation(simply_box, (1.25 * step)*(i + 0.5), 0, 0)
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

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
#smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:

 # multiples meshes built in parallel, complex and numerous mesh edition (performance)


Mesh_1 = smesh.Mesh(tesla_valve,'Mesh_1')
Regular_1D = Mesh_1.Segment()

# распределение слоев выдавливания
if mesh_half == 1:
    Number_of_Segments_1 = Regular_1D.NumberOfSegments(NumOfSegments // 2, None, [])
    Number_of_Segments_1.SetConversionMode( 1 )
    Number_of_Segments_1.SetTableFunction( [0, 1, 0.05, 0.25, 0.5, 0.1, 1, 0.1] )

if mesh_half == 0:
    Number_of_Segments_1 = Regular_1D.NumberOfSegments(NumOfSegments,None,[])
    Number_of_Segments_1.SetConversionMode( 1 )
    Number_of_Segments_1.SetTableFunction( [ 0, 1, 0.05, 0.25, 0.5, 0.1, 0.95, 0.25, 1, 1 ] )

Prism_3D = Mesh_1.Prism()

wall_f_1 = Mesh_1.GroupOnGeom(wall_f,'wall_f',SMESH.FACE)
NETGEN_1D_2D = Mesh_1.Triangle(algo=smeshBuilder.NETGEN_1D2D,geom=wall_f)
NETGEN_2D_Parameters_1 = NETGEN_1D_2D.Parameters()
NETGEN_2D_Parameters_1.SetSecondOrder( 0 )
NETGEN_2D_Parameters_1.SetOptimize( 1 )
NETGEN_2D_Parameters_1.SetFineness( 5 )
NETGEN_2D_Parameters_1.SetGrowthRate( 0.01)
NETGEN_2D_Parameters_1.SetChordalError( -1 )
NETGEN_2D_Parameters_1.SetChordalErrorEnabled( 0 )
NETGEN_2D_Parameters_1.SetUseSurfaceCurvature( 1 )
NETGEN_2D_Parameters_1.SetFuseEdges( 1 )
#NETGEN_2D_Parameters_1.SetQuadAllowed( 1 )

Viscous_Layers_2D_1 = NETGEN_1D_2D.ViscousLayers2D(1,3,1.1, list_ID,1)
Viscous_Layers_2D_1.SetTotalThickness( 2 )
Viscous_Layers_2D_1.SetNumberLayers( 1 )
Viscous_Layers_2D_1.SetStretchFactor( 1 )
Viscous_Layers_2D_1.SetEdges(list_ID , 1 )

# плотность сетки
NETGEN_2D_Parameters_1.SetMinSize( min_size )
NETGEN_2D_Parameters_1.SetLocalSizeOnShape(simply_box_num, size_special)
NETGEN_2D_Parameters_1.SetMaxSize( max_size )
isDone = Mesh_1.Compute()

# группы
wall_b_1 = Mesh_1.GroupOnGeom(wall_b,'wall_b',SMESH.FACE)
ent_1 = Mesh_1.GroupOnGeom(ent,'ent',SMESH.FACE)
out_1 = Mesh_1.GroupOnGeom(out,'out',SMESH.FACE)
[ wall_f_1, wall_b_1, ent_1, out_1 ] = Mesh_1.GetGroups()
#NETGEN_2D = NETGEN_2D_3.GetSubMesh()

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
