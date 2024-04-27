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
geomObj_1 = geompy.MakeMarker(0, 0, 0, 1, 0, 0, 0, 1, 0)
sk = geompy.Sketcher2D()
sk.addPoint(0.0000000, 0.0000000)
sk.addArcAngleRadiusLength(30.0000000, 300.0000000, 180.0000000)
sk.addSegmentY(0.0000000)
sk.close()
Sketch_1 = sk.wire(geomObj_1)
geomObj_2 = geompy.MakeMarker(0, 0, 0, 1, 0, 0, 0, 1, 0)
sk = geompy.Sketcher2D()
sk.addPoint(-50.0000000, 86.6025404)
sk.addArcAngleRadiusLength(30.0000000, 200.0000000, 180.0000000)
sk.addSegmentAngleY(0.0000000, 0.0000000)
sk.close()
Sketch_2 = sk.wire(geomObj_2)
geomObj_3 = geompy.MakeFaceWires([Sketch_1, Sketch_2], 1)
geomObj_4 = geompy.MakeFaceHW(4200.000000000001, 100, 1)
geomObj_5 = geompy.MakeTranslation(geomObj_4, 900.0000000000002, -50, 0)
simply_tesla = geompy.MakeFuseList([geomObj_3, geomObj_5], True, False)
geomObj_6 = geompy.MakeVertex(0, -50, 0)
geomObj_7 = geompy.MakeVertex(100, -50, 0)
geomObj_8 = geompy.MakeLineTwoPnt(geomObj_6, geomObj_7)
geomObj_9 = geompy.MakeFaceWires([Sketch_1, Sketch_2], 1)
geomObj_10 = geompy.MakeTranslation(geomObj_9, 0, 0, 0)
geomObj_11 = geompy.MakeTranslation(geomObj_9, 1500, 0, 0)
geomObj_12 = geompy.MakeTranslation(geomObj_9, 750.0000000000001, 0, 0)
geomObj_13 = geompy.MakeMirrorByAxis(geomObj_12, geomObj_8)
geomObj_14 = geompy.MakeTranslation(geomObj_9, 2250, 0, 0)
geomObj_15 = geompy.MakeMirrorByAxis(geomObj_14, geomObj_8)
geomObj_16 = geompy.MakeFaceHW(4200.000000000001, 100, 1)
geomObj_17 = geompy.MakeTranslation(geomObj_16, 600.0000000000002, -50, 0)
simply_tesla_num = geompy.MakeFuseList([geomObj_10, geomObj_11, geomObj_13, geomObj_15, geomObj_17], True, False)
[Face_1,Face_2,Face_3,Face_4,Face_5] = geompy.ExtractShapes(simply_tesla_num, geompy.ShapeType["FACE"], True)
Fuse_1 = geompy.MakeFuseList([Face_1, Face_2, Face_3, Face_4, Face_5], True, True)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Sketch_1, 'Sketch_1' )
geompy.addToStudy( Sketch_2, 'Sketch_2' )
geompy.addToStudy( simply_tesla, 'simply_tesla' )
geompy.addToStudy( simply_tesla_num, 'simply_tesla_num' )
geompy.addToStudyInFather( simply_tesla_num, Face_1, 'Face_1' )
geompy.addToStudyInFather( simply_tesla_num, Face_2, 'Face_2' )
geompy.addToStudyInFather( simply_tesla_num, Face_3, 'Face_3' )
geompy.addToStudyInFather( simply_tesla_num, Face_4, 'Face_4' )
geompy.addToStudyInFather( simply_tesla_num, Face_5, 'Face_5' )
geompy.addToStudy( Fuse_1, 'Fuse_1' )


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
