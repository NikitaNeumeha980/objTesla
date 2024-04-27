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
step = 2 * r1 /math.sin(alpha * math.pi/180)

# Длина основного канала
L = numSteps * step * 1.75

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
      L * 0.5 - step * 1.25,
      - w * 0.5,
      0
    )
  ],
  True, True
)

tesla_valve = geompy.MakePrismVecH(simply_tesla_num, OZ, w * half)

# геометрические группы
[wall_f] =\
    geompy.GetShapesOnPlaneWithLocation(
        tesla_valve,
        geompy.ShapeType["FACE"],
        geompy.MakeVectorDXDYDZ(0, 0, 1),
        geompy.MakeVertex(0, 0, 0),
        GEOM.ST_ON
    )

[wall_b] =\
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
        geompy.MakeVertex(- step * 1.25, 0, 0),
        GEOM.ST_ON
    )

#[out] =\
    #geompy.GetShapesOnPlaneWithLocation(
        #tesla_valve,
        #geompy.ShapeType["FACE"],
        #geompy.MakeVectorDXDYDZ(1, 0, 0),
        #geompy.MakeVertex(L * 0.5 - step * 1.25, 0, 0),
        #GEOM.ST_ON
    #)

geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Sketch_1, 'Sketch_1' )
geompy.addToStudy( Sketch_2, 'Sketch_2' )
geompy.addToStudy( simply_tesla_num, 'simply_tesla_num')
geompy.addToStudy( tesla_valve, 'tesla_valve')
geompy.addToStudy( wall_f, 'wall_f')
geompy.addToStudy( wall_b, 'wall_b')
geompy.addToStudy( ent, 'ent')
#geompy.addToStudy( out, 'out')

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
