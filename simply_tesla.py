#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.12.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
sys.path.insert(0, r'/home/nikita/VS_python')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

# угол наклона ушка
alpha = 60

# кол-во ушек
num = 3

# ширина канала
w = 1

# внутренний радиус отводящего ушка
k = 2
r2 = w * k

# внешний радиус отводящего ушка
r1 = r2 + w

# ширина отводящей магистрали
box_L1 = 2 * r1
box_L2 = box_L1 - (r1 - r2) * 2

#смещение ушек
step_k = 2
step = (box_L1 / 1.2 ) / (math.sin((90-alpha)*math.pi/180.0))

# длина отводящей магистрали
box_h = w + box_L1 + w * 10

# длина основной магистрали
L = (w + box_L1) * (num * step_k) + alpha * 0.25 * w

# шаг для box_mesh
step_box = (box_L1 / 2) / (math.sin((90-alpha)*math.pi/180.0))

# размер бокса по X
box_mesh_X = (w / (math.sin((90-alpha)*math.pi/180.0))) * 1.5

# ось вращения
rot = 0.3

geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

# основной канал
Box_1 = geompy.MakeBoxDXDYDZ(L, w, w)

Box_2 = geompy.MakeBoxDXDYDZ(box_L1, w, box_h)
Cylinder_1 = geompy.MakeCylinder(O, OY, r1, w)
geompy.TranslateDXDYDZ(Cylinder_1, r1, 0, box_h)
Fuse_1 = geompy.MakeFuseList([Box_2, Cylinder_1], True, True)
geompy.TranslateDXDYDZ(Fuse_1, rot * L , 0, w * (-10))

# ось поворота "ушек"
Vertex_1 = geompy.MakeVertex(rot * L + r1, 0, w)
Vertex_2 = geompy.MakeVertex(rot * L + r1, w, w)
Line_1 = geompy.MakeLineTwoPnt(Vertex_1, Vertex_2)

# ось отражения для случаев когда кол-во "ушек" > 1
Vertex_3 = geompy.MakeVertex(0, 0.5 * w, 0.5 * w)
Vertex_4 = geompy.MakeVertex(w, 0.5 * w, 0.5 * w)
Line_2 = geompy.MakeLineTwoPnt(Vertex_3, Vertex_4)

# поворот "уха"
Rotation_1 = geompy.MakeRotation(Fuse_1, Line_1, alpha*math.pi/180.0)

Box_3 = geompy.MakeBoxDXDYDZ(box_L2, w, box_h)
Cylinder_2 = geompy.MakeCylinder(O, OY, r2, w)
Translation_1 = geompy.MakeTranslation(Cylinder_2, r2, 0, box_h)
Fuse_2 = geompy.MakeFuseList([Box_3, Translation_1], True, True)
Translation_2 = geompy.MakeTranslation(Fuse_2, rot * L  + (r1 - r2), 0, w * (-10))
Rotation_2 = geompy.MakeRotation(Translation_2, Line_1, alpha*math.pi/180.0)
Cut_1 = geompy.MakeCutList(Rotation_1, [Rotation_2], True)
Box_4 = geompy.MakeBoxDXDYDZ(3 * L, w, w * 1000)
Translation_3 = geompy.MakeTranslation(Box_4, -0.5 * (3 * L) , 0, -1 * (w * 1000 - w))

#
Cut_2 = geompy.MakeCutList(Cut_1, [Translation_3], True)

#
simply_tesla = geompy.MakeFuseList([Box_1, Cut_2], True, True)
# грани для сглаживания на основное ухо
smooth=\
    geompy.GetShapesOnBoxIDs(
        geompy.MakeBox(w, w, w + 1, L - w, 0, 0),
        simply_tesla,
        geompy.ShapeType["EDGE"],
        GEOM.ST_IN
        )
sm_box = geompy.MakeBox(w, w, w, L - w, 0, 0)
geompy.addToStudy(sm_box, 'sm_box')

#сглаживание
Cut_2 =\
    geompy.MakeCutList(
    geompy.MakeFillet(simply_tesla, w * 0.5, geompy.ShapeType["EDGE"], smooth),
    [Translation_3],
    True
    )
simply_tesla = geompy.MakeFuseList([Box_1, Cut_2], True, True)

# плоскости для граничных условий
wall_f = geompy.MakePlane(O, OY, 2000 + L)
wall_b = geompy.MakePlane(Vertex_2, OY, 2000 + L)
ent = geompy.MakePlane(O, OX, 2000 + L)
out = geompy.MakeTranslation(ent, L, 0, 0)

 # зона усложненной сетки
box_split =\
    geompy.MakeCylinder(
        Vertex_1, # базовая точка
        geompy.MakeVectorDXDYDZ(0, 1, 0), # вектор
        box_mesh_X, # радиус
        w
    )
t_box_split = geompy.MakeTranslation(
    box_split,
    -(step_box - (w / (math.sin((90-alpha)*math.pi/180.0))) * 0.5),
    0,
    -(w * 0.5))

box_mix =\
    geompy.MakeCylinder(
        Vertex_1, # базовая точка
        geompy.MakeVectorDXDYDZ(0, 1, 0), # вектор
        box_mesh_X, # радиус
        w # высота
    )
t_box_mix = geompy.MakeTranslation(
    box_mix,
    step_box - (w / (math.sin((90-alpha)*math.pi/180.0))) * 0.5,
    0,
    -(w * 0.5))

simply_box = geompy.MakeFuseList ([t_box_mix, t_box_split], True, True)

box_ent = geompy.MakeBox(0, 0, 0, w, w, w)
box_out = geompy.MakeTranslation(box_ent, L - w, 0, 0)
box_e_o = geompy.MakeFuseList([box_ent, box_out], True, True)

# цикл создания более одного уха
i = 1
Cut_n = Cut_2
simply_tesla_n = simply_tesla
t_box_split_mirr = t_box_split
t_box_mix_mirr = t_box_mix
simply_box_n = simply_box
while i < num:
    Mirror_n = geompy.MakeMirrorByAxis(Cut_n, Line_2)
    Mirror_n2 = geompy.MakeTranslation(Mirror_n, step, 0, 0)
    simply_tesla_num = geompy.MakeFuseList([simply_tesla_n, Mirror_n2], True, True)
    Cut_n = Mirror_n2
    simply_tesla_n = simply_tesla_num
    # боксы для мелкой сетки
    t_box_split_n = geompy.MakeMirrorByAxis(t_box_split_mirr, Line_2)
    t_box_split_n2 = geompy.MakeTranslation(t_box_split_n, step, 0, 0)
    t_box_mix_n = geompy.MakeMirrorByAxis(t_box_mix_mirr, Line_2)
    t_box_mix_n2 = geompy.MakeTranslation(t_box_mix_n, step, 0, 0)
    simply_box_num = geompy.MakeFuseList([simply_box_n, t_box_split_n2, t_box_mix_n2], True, True, True)
    simply_box_n = simply_box_num
    t_box_split_mirr = t_box_split_n2
    t_box_mix_mirr = t_box_mix_n2
    i  = i + 1

#[Face_1] = geompy.SubShapes(simply_tesla_n, [13])

[Face_1] =\
    geompy.GetShapesOnPlaneWithLocation(
        simply_tesla_num,
        geompy.ShapeType["FACE"],
        geompy.MakeVectorDXDYDZ(0, 1, 0),
        geompy.MakeVertex(0, 0, 0),
        GEOM.ST_ON
    )


geompy.addToStudy( simply_tesla_num, 'simply_tesla_num')
geompy.addToStudyInFather( simply_tesla_num, Face_1, 'Face_1' )

# получение ID объектов для вычета их из построения вязкого подслоя сетки
# направлением для нормали будет ось Х
ent_ID =\
    geompy.GetShapesOnPlaneWithLocation(
        Face_1,
        geompy.ShapeType["EDGE"],
        geompy.MakeVectorDXDYDZ(1, 0, 0),
        geompy.MakeVertex(0, 0, 0),
        GEOM.ST_ON
    )
out_ID =\
    geompy.GetShapesOnPlaneWithLocation(
        Face_1,
        geompy.ShapeType["EDGE"],
        geompy.MakeVectorDXDYDZ(1, 0, 0),
        geompy.MakeVertex(L, 0, 0),
        GEOM.ST_ON
    )

list_ID =\
    [
        geompy.GetSubShapeID(simply_tesla_num, ent_ID[0]),
        geompy.GetSubShapeID(simply_tesla_num, out_ID[0])
    ]

geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Box_2, 'Box_2' )
geompy.addToStudy( Cylinder_1, 'Cylinder_1' )
geompy.addToStudy( Fuse_1, 'Fuse_1' )
geompy.addToStudy( Box_1, 'Box_1' )
geompy.addToStudy( Vertex_1, 'Vertex_1' )
geompy.addToStudy( Vertex_2, 'Vertex_2' )
geompy.addToStudy( Line_1, 'Line_1' )
geompy.addToStudy( Vertex_3, 'Vertex_3' )
geompy.addToStudy( Vertex_4, 'Vertex_4' )
geompy.addToStudy( Line_2, 'Line_2' )
geompy.addToStudy( Rotation_1, 'Rotation_1' )
geompy.addToStudy( Box_3, 'Box_3' )
geompy.addToStudy( Cylinder_2, 'Cylinder_2' )
geompy.addToStudy( Translation_1, 'Translation_1' )
geompy.addToStudy( Fuse_2, 'Fuse_2' )
geompy.addToStudy( Translation_2, 'Translation_2' )
geompy.addToStudy( Rotation_2, 'Rotation_2' )
geompy.addToStudy( Cut_1, 'Cut_1' )
geompy.addToStudy( Box_4, 'Box_4' )
geompy.addToStudy( Translation_3, 'Translation_3' )
geompy.addToStudy( Cut_2, 'Cut_2' )
geompy.addToStudy( simply_tesla, 'simply_tesla')
geompy.addToStudy( Mirror_n, 'Mirror_n' )
geompy.addToStudy( Mirror_n2, 'Mirror_n2' )
geompy.addToStudy( simply_tesla_n, 'simply_tesla_n')
geompy.addToStudy( simply_tesla_num, 'simply_tesla_num')
geompy.addToStudy( box_split, 'box_split')
geompy.addToStudy( t_box_split, 't_box_split')
geompy.addToStudy( box_mix, 'box_mix')
geompy.addToStudy( t_box_mix, 't_box_mix')
geompy.addToStudy( t_box_mix_mirr, 't_box_mix_mirr')
geompy.addToStudy( t_box_split_mirr, 't_box_split_mirr')
geompy.addToStudy( simply_box_num, 'simply_box_num')
geompy.addToStudy(box_e_o, 'box_e_o')
geompy.addToStudy( wall_f, 'wall_f' )
geompy.addToStudy( wall_b, 'wall_b' )
geompy.addToStudy( ent, 'ent' )
geompy.addToStudy( out, 'out' )
geompy.addToStudyInFather( simply_tesla_num, Face_1, 'Face_1' )


###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
#smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                 # multiples meshes built in parallel, complex and numerous mesh edition (performance)

Mesh_1 = smesh.Mesh(simply_tesla_num,'Mesh_1')
Regular_1D = Mesh_1.Segment()

# распределение слоев выдавливания
Number_of_Segments_1 = Regular_1D.NumberOfSegments(10,None,[])
Number_of_Segments_1.SetConversionMode( 1 )
Number_of_Segments_1.SetTableFunction( [ 0, 1, 0.05, 0.25, 0.5, 0.1, 0.95, 0.25, 1, 1 ] )

Prism_3D = Mesh_1.Prism()
Face_1_1 = Mesh_1.GroupOnGeom(Face_1,'Face_1',SMESH.FACE)
NETGEN_1D_2D = Mesh_1.Triangle(algo=smeshBuilder.NETGEN_1D2D,geom=Face_1)
NETGEN_2D_Parameters_1 = NETGEN_1D_2D.Parameters()
NETGEN_2D_Parameters_1.SetSecondOrder( 0 )
NETGEN_2D_Parameters_1.SetOptimize( 1 )
NETGEN_2D_Parameters_1.SetFineness( 4 )
NETGEN_2D_Parameters_1.SetGrowthRate( 0.025)
NETGEN_2D_Parameters_1.SetChordalError( -1 )
NETGEN_2D_Parameters_1.SetChordalErrorEnabled( 0 )
NETGEN_2D_Parameters_1.SetUseSurfaceCurvature( 1 )
NETGEN_2D_Parameters_1.SetFuseEdges( 1 )
NETGEN_2D_Parameters_1.SetQuadAllowed( 1 )
Viscous_Layers_2D_1 = NETGEN_1D_2D.ViscousLayers2D(1,3,1.1, list_ID,1)
[ Face_1_1 ] = Mesh_1.GetGroups()
Viscous_Layers_2D_1.SetTotalThickness( 0.1 )
Viscous_Layers_2D_1.SetNumberLayers( 3 )
Viscous_Layers_2D_1.SetStretchFactor( 1 )
Viscous_Layers_2D_1.SetEdges(list_ID , 1 )

[ Face_1_1 ] = Mesh_1.GetGroups()
# плотность сетки
min_size = 0.02
max_size = 0.2
NETGEN_2D_Parameters_1.SetMinSize( min_size )
NETGEN_2D_Parameters_1.SetLocalSizeOnShape(simply_box_num, min_size)
NETGEN_2D_Parameters_1.SetLocalSizeOnShape(box_e_o, min_size)
NETGEN_2D_Parameters_1.SetMaxSize( max_size )

NETGEN_2D_Parameters_1.SetWorstElemMeasure( 24853 )
NETGEN_2D_Parameters_1.SetUseDelauney( 192 )
NETGEN_2D_Parameters_1.SetCheckChartBoundary( 3 )
[ Face_1_1 ] = Mesh_1.GetGroups()
isDone = Mesh_1.Compute()
[ Face_1_1 ] = Mesh_1.GetGroups()
Viscous_Layers_2D_1.SetTotalThickness( 0.01 )
Viscous_Layers_2D_1.SetNumberLayers( 3 )
Viscous_Layers_2D_1.SetStretchFactor( 1 )
Viscous_Layers_2D_1.SetEdges( list_ID, 1 )
[ Face_1_1 ] = Mesh_1.GetGroups()
aCriteria = []
aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_BelongToPlane,SMESH.FT_Undefined,wall_f)
aCriteria.append(aCriterion)
aFilter_1 = smesh.GetFilterFromCriteria(aCriteria)
aFilter_1.SetMesh(Mesh_1.GetMesh())
wall_f_1 = Mesh_1.GroupOnFilter( SMESH.FACE, 'wall_f', aFilter_1 )
[ Face_1_1, wall_f_1 ] = Mesh_1.GetGroups()
aCriteria = []
aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_BelongToPlane,SMESH.FT_Undefined,wall_b)
aCriteria.append(aCriterion)
aFilter_2 = smesh.GetFilterFromCriteria(aCriteria)
aFilter_2.SetMesh(Mesh_1.GetMesh())
wall_b_1 = Mesh_1.GroupOnFilter( SMESH.FACE, 'wall_b', aFilter_2 )
[ Face_1_1, wall_f_1, wall_b_1 ] = Mesh_1.GetGroups()
aCriteria = []
aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_BelongToPlane,SMESH.FT_Undefined,ent)
aCriteria.append(aCriterion)
aFilter_3 = smesh.GetFilterFromCriteria(aCriteria)
aFilter_3.SetMesh(Mesh_1.GetMesh())
ent_1 = Mesh_1.GroupOnFilter( SMESH.FACE, 'ent', aFilter_3 )
[ Face_1_1, wall_f_1, wall_b_1, ent_1 ] = Mesh_1.GetGroups()
aCriteria = []
aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_BelongToPlane,SMESH.FT_Undefined,out)
aCriteria.append(aCriterion)
aFilter_4 = smesh.GetFilterFromCriteria(aCriteria)
aFilter_4.SetMesh(Mesh_1.GetMesh())
out_1 = Mesh_1.GroupOnFilter( SMESH.FACE, 'out', aFilter_4 )
[ Face_1_1, wall_f_1, wall_b_1, ent_1, out_1 ] = Mesh_1.GetGroups()
Sub_mesh_1 = NETGEN_1D_2D.GetSubMesh()


## Set names of Mesh objects
smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
smesh.SetName(NETGEN_1D_2D.GetAlgorithm(), 'NETGEN 1D-2D')
smesh.SetName(Prism_3D.GetAlgorithm(), 'Prism_3D')
smesh.SetName(NETGEN_2D_Parameters_1, 'NETGEN 2D Parameters_1')
smesh.SetName(Viscous_Layers_2D_1, 'Viscous Layers 2D_1')
smesh.SetName(Number_of_Segments_1, 'Number of Segments_1')
smesh.SetName(wall_f_1, 'wall_f')
smesh.SetName(wall_b_1, 'wall_b')
smesh.SetName(ent_1, 'ent')
smesh.SetName(Sub_mesh_1, 'Sub-mesh_1')
smesh.SetName(out_1, 'out')
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')


if salome.sg.hasDesktop():
    salome.sg.updateObjBrowser()
