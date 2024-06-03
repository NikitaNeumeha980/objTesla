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
sk.addArcAngleRadiusLength(30.0000000, 1500.0000000, 180.0000000)
sk.addSegmentY(0.0000000)
sk.close()
Sketch_1 = sk.wire(geomObj_1)
geomObj_2 = geompy.MakeMarker(0, 0, 0, 1, 0, 0, 0, 1, 0)
sk = geompy.Sketcher2D()
sk.addPoint(-250.0000000, 433.0127019)
sk.addArcAngleRadiusLength(30.0000000, 1000.0000000, 180.0000000)
sk.addSegmentAngleY(0.0000000, 0.0000000)
sk.close()
Sketch_2 = sk.wire(geomObj_2)
geomObj_3 = geompy.MakeFaceWires([Sketch_1, Sketch_2], 1)
geomObj_4 = geompy.MakeFaceHW(36000.00000000001, 500, 1)
geomObj_5 = geompy.MakeTranslation(geomObj_4, 12000, -250, 0)
simply_tesla = geompy.MakeFuseList([geomObj_3, geomObj_5], True, False)
geomObj_6 = geompy.MakeVertex(0, -250, 0)
geomObj_7 = geompy.MakeVertex(500, -250, 0)
geomObj_8 = geompy.MakeLineTwoPnt(geomObj_6, geomObj_7)
geomObj_9 = geompy.MakeFaceWires([Sketch_1, Sketch_2], 1)
geomObj_10 = geompy.MakeTranslation(geomObj_9, 0, 0, 0)
geomObj_11 = geompy.MakeTranslation(geomObj_9, 12000, 0, 0)
geomObj_12 = geompy.MakeTranslation(geomObj_9, 6000.000000000001, 0, 0)
geomObj_13 = geompy.MakeMirrorByAxis(geomObj_12, geomObj_8)
geomObj_14 = geompy.MakeTranslation(geomObj_9, 18000, 0, 0)
geomObj_15 = geompy.MakeMirrorByAxis(geomObj_14, geomObj_8)
geomObj_16 = geompy.MakeFaceHW(36000.00000000001, 500, 1)
geomObj_17 = geompy.MakeTranslation(geomObj_16, 7500.000000000002, -250, 0)
simply_tesla_num = geompy.MakeFuseList([geomObj_10, geomObj_11, geomObj_13, geomObj_15, geomObj_17], True, True)
geomObj_18 = geompy.MakePrismVecH(simply_tesla_num, OZ, 250)
geomObj_19 = geompy.MakeVertex(-6001.000000000001, 1, 501)
geomObj_20 = geompy.MakeVertex(-5999.000000000001, -1, -501)
geomObj_21 = geompy.MakeBoxTwoPnt(geomObj_19, geomObj_20)
geomObj_22 = geompy.MakeTranslation(geomObj_21, 0, 0, 0)
geomObj_23 = geompy.MakeVertex(-6001.000000000001, 1, 501)
geomObj_24 = geompy.MakeVertex(-5999.000000000001, -1, -501)
geomObj_25 = geompy.MakeBoxTwoPnt(geomObj_23, geomObj_24)
geomObj_26 = geompy.MakeTranslation(geomObj_25, 6000.000000000001, 0, 0)
geomObj_27 = geompy.MakeMirrorByAxis(geomObj_26, geomObj_8)
geomObj_28 = geompy.MakeVertex(-6001.000000000001, 1, 501)
geomObj_29 = geompy.MakeVertex(-5999.000000000001, -1, -501)
geomObj_30 = geompy.MakeBoxTwoPnt(geomObj_28, geomObj_29)
geomObj_31 = geompy.MakeTranslation(geomObj_30, 12000, 0, 0)
geomObj_32 = geompy.MakeVertex(-6001.000000000001, 1, 501)
geomObj_33 = geompy.MakeVertex(-5999.000000000001, -1, -501)
geomObj_34 = geompy.MakeBoxTwoPnt(geomObj_32, geomObj_33)
geomObj_35 = geompy.MakeTranslation(geomObj_34, 18000, 0, 0)
geomObj_36 = geompy.MakeMirrorByAxis(geomObj_35, geomObj_8)
tesla_valve = geompy.MakeFillet(geomObj_18, 5000, geompy.ShapeType["EDGE"], [16, 107, 37, 58])
geomObj_37 = geompy.MakeVectorDXDYDZ(0, 0, 1)
geomObj_38 = geompy.MakeVertex(0, 0, 0)
[wall_b] = geompy.GetShapesOnPlaneWithLocation(tesla_valve, geompy.ShapeType["FACE"], geomObj_37, geomObj_38, GEOM.ST_ON)
geomObj_39 = geompy.MakeVectorDXDYDZ(0, 0, 1)
geomObj_40 = geompy.MakeVertex(0, 0, 250)
[wall_f] = geompy.GetShapesOnPlaneWithLocation(tesla_valve, geompy.ShapeType["FACE"], geomObj_39, geomObj_40, GEOM.ST_ON)
[geomObj_41] = geompy.SubShapeAll(wall_f, geompy.ShapeType["FACE"])
geomObj_42 = geompy.MakeVectorDXDYDZ(1, 0, 0)
geomObj_43 = geompy.MakeVertex(-10500, 0, 0)
[ent] = geompy.GetShapesOnPlaneWithLocation(tesla_valve, geompy.ShapeType["FACE"], geomObj_42, geomObj_43, GEOM.ST_ON)
geomObj_44 = geompy.MakeVectorDXDYDZ(1, 0, 0)
geomObj_45 = geompy.MakeVertex(25500.00000000001, 0, 0)
[out] = geompy.GetShapesOnPlaneWithLocation(tesla_valve, geompy.ShapeType["FACE"], geomObj_44, geomObj_45, GEOM.ST_ON)
geomObj_46 = geompy.MakeVectorDXDYDZ(1, 0, 0)
geomObj_47 = geompy.MakeVertex(-10500, 0, 0)
[geomObj_48] = geompy.GetShapesOnPlaneWithLocation(ent, geompy.ShapeType["FACE"], geomObj_46, geomObj_47, GEOM.ST_ON)
geomObj_49 = geompy.MakeVectorDXDYDZ(1, 0, 0)
geomObj_50 = geompy.MakeVertex(25500.00000000001, 0, 0)
[geomObj_51] = geompy.GetShapesOnPlaneWithLocation(out, geompy.ShapeType["FACE"], geomObj_49, geomObj_50, GEOM.ST_ON)
geomObj_52 = geompy.MakeVectorDXDYDZ(0, 0, 1)
geomObj_53 = geompy.MakeVertex(0, 0, 250)
[geomObj_54] = geompy.GetShapesOnPlaneWithLocation(wall_f, geompy.ShapeType["FACE"], geomObj_52, geomObj_53, GEOM.ST_ON)
geomObj_55 = geompy.MakeVertex(0, 0, -250)
geomObj_56 = geompy.MakeVectorDXDYDZ(0, 0, 1)
geomObj_57 = geompy.MakeCylinder(geomObj_55, geomObj_56, 1000, 1000)
geomObj_58 = geompy.MakeVertex(-5500.000000000001, 0, -250)
geomObj_59 = geompy.MakeVectorDXDYDZ(0, 0, 1)
geomObj_60 = geompy.MakeCylinder(geomObj_58, geomObj_59, 1000, 1000)
simply_box = geompy.MakeFuseList([geomObj_57, geomObj_60], True, True)
geomObj_61 = geompy.MakeTranslation(simply_box, 0, 0, 0)
geomObj_62 = geompy.MakeTranslation(simply_box, 12000, 0, 0)
geomObj_63 = geompy.MakeTranslation(simply_box, 6000.000000000001, 0, 0)
geomObj_64 = geompy.MakeTranslation(simply_box, 18000, 0, 0)
simply_box_num = geompy.MakeFuseList([geomObj_61, geomObj_62, geomObj_63, geomObj_64], True, False)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Sketch_1, 'Sketch_1' )
geompy.addToStudy( Sketch_2, 'Sketch_2' )
geompy.addToStudy( simply_tesla, 'simply_tesla' )
geompy.addToStudy( simply_tesla_num, 'simply_tesla_num' )
geompy.addToStudy( tesla_valve, 'tesla_valve' )
geompy.addToStudyInFather( tesla_valve, wall_b, 'wall_b' )
geompy.addToStudyInFather( tesla_valve, wall_f, 'wall_f' )
geompy.addToStudyInFather( tesla_valve, ent, 'ent' )
geompy.addToStudyInFather( tesla_valve, out, 'out' )
geompy.addToStudy( simply_box, 'simply_box' )
geompy.addToStudy( simply_box_num, 'simply_box_num' )

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
#smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                 # multiples meshes built in parallel, complex and numerous mesh edition (performance)

NETGEN_3D_Parameters_1 = smesh.CreateHypothesisByAverageLength( 'NETGEN_Parameters', 'NETGENEngine', 3651.37, 0 )
NETGEN_3D_Parameters_1.SetMaxSize( 80 )
NETGEN_3D_Parameters_1.SetMinSize( 30 )
NETGEN_3D_Parameters_1.SetSecondOrder( 0 )
NETGEN_3D_Parameters_1.SetOptimize( 1 )
NETGEN_3D_Parameters_1.SetFineness( 5 )
NETGEN_3D_Parameters_1.SetGrowthRate( 0.01 )
NETGEN_3D_Parameters_1.SetNbSegPerEdge( 3 )
NETGEN_3D_Parameters_1.SetNbSegPerRadius( 5 )
NETGEN_3D_Parameters_1.SetChordalError( -1 )
NETGEN_3D_Parameters_1.SetChordalErrorEnabled( 0 )
NETGEN_3D_Parameters_1.SetUseSurfaceCurvature( 1 )
NETGEN_3D_Parameters_1.SetFuseEdges( 1 )
NETGEN_3D_Parameters_1.SetQuadAllowed( 0 )
NETGEN_3D_Parameters_1.SetLocalSizeOnShape(simply_box_num, 33)
NETGEN_3D_Parameters_1.UnsetLocalSizeOnEntry("tesla_valve")
Mesh_1 = smesh.Mesh(tesla_valve,'Mesh_1')
status = Mesh_1.AddHypothesis( tesla_valve, NETGEN_3D_Parameters_1 )
NETGEN_1D_2D_3D = Mesh_1.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
Viscous_Layers_1 = NETGEN_1D_2D_3D.ViscousLayers(12,1,1,[ 159, 186, 90 ],1,smeshBuilder.SURF_OFFSET_SMOOTH)
wall_b_1 = Mesh_1.GroupOnGeom(wall_b,'wall_b',SMESH.FACE)
wall_f_1 = Mesh_1.GroupOnGeom(wall_f,'wall_f',SMESH.FACE)
ent_1 = Mesh_1.GroupOnGeom(ent,'ent',SMESH.FACE)
out_1 = Mesh_1.GroupOnGeom(out,'out',SMESH.FACE)
[ wall_b_1, wall_f_1, ent_1, out_1 ] = Mesh_1.GetGroups()
isDone = Mesh_1.Compute()
Viscous_Layers_1.SetTotalThickness( 12 )
Viscous_Layers_1.SetNumberLayers( 1 )
Viscous_Layers_1.SetStretchFactor( 1 )
Viscous_Layers_1.SetMethod( smeshBuilder.FACE_OFFSET )
Viscous_Layers_1.SetFaces( [ 159, 186, 90 ], 1 )


## Set names of Mesh objects
smesh.SetName(NETGEN_1D_2D_3D.GetAlgorithm(), 'NETGEN 1D-2D-3D')
smesh.SetName(Viscous_Layers_1, 'Viscous Layers_1')
smesh.SetName(NETGEN_3D_Parameters_1, 'NETGEN 3D Parameters_1')
smesh.SetName(wall_b_1, 'wall_b')
smesh.SetName(wall_f_1, 'wall_f')
smesh.SetName(ent_1, 'ent')
smesh.SetName(out_1, 'out')
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
