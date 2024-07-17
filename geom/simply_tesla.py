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

#для построения половины сетки в продольном сечении i = 1, иначе i = 0
i = 1

# угол наклона ушка
alpha = 60

# кол-во ушек
num = 4

# ширина канала
w = 100 #мкм

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
step = box_L1 / (math.sin((90-alpha)*math.pi/180.0))

# длина отводящей магистрали
box_h = w + 0.5 * box_L1 + w * 100

# длина основной магистрали
L = (w + box_L1) * (num * step_k) + alpha * 0.25 * w

# шаг для box_mesh
step_box = box_L1 / (math.sin((90-alpha)*math.pi/180.0))

# размер бокса по X
box_mesh_X = (w / (math.sin((90-alpha)*math.pi/180.0))) * 1.5

# ось вращения
rot = 0.25

# плотность сетки
min_size = 2.5
max_size = 6

geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

# основной канал
Box_1 = geompy.MakeBoxDXDYDZ(L, w, w)

# Внешнее ухо
Fuse_1 = geompy.MakeFuseList(
    [
        geompy.MakeBoxDXDYDZ(box_L1, w, box_h),
        geompy.TranslateDXDYDZ(geompy.MakeCylinder(O, OY, r1, w), r1, 0, box_h)
    ],
    True,
    True
    )

geompy.TranslateDXDYDZ(Fuse_1, rot * L , 0, -box_h)

# ось поворота "ушек"
Vertex_1 = geompy.MakeVertex(rot * L + 2 * r1, 0, w)
Vertex_2 = geompy.MakeVertex(rot * L + 2 * r1, w, w)
Line_1 = geompy.MakeLineTwoPnt(Vertex_1, Vertex_2)

# ось поворота бокса для обрезания внутреннего "ушка"
Line_1_1 = geompy.MakeTranslation(
    Line_1,
    - ((2 * r1) /  (math.sin((90-alpha)*math.pi/180.0)) - w /  (math.sin((90-alpha)*math.pi/180.0))),
    0,
    0,
    )
geompy.addToStudy( Line_1_1, 'Line_1_1')

# бокс для обрезания внутреннего уха
boxTOcut = geompy.MakeRotation(
    geompy.MakeTranslation(geompy.MakeBoxDXDYDZ(3 * L, w, w * 1000), 0, 0, -1 * (w * 1000 - w)),
    Line_1_1,
    -0.1 * alpha*math.pi/180.0
    )
geompy.addToStudy( boxTOcut, 'boxTOcut')

# ось отражения для случаев когда кол-во "ушек" > 1
Vertex_3 = geompy.MakeVertex(0, 0.5 * w, 0.5 * w)
Vertex_4 = geompy.MakeVertex(w, 0.5 * w, 0.5 * w)
Line_2 = geompy.MakeLineTwoPnt(Vertex_3, Vertex_4)

# поворот "уха"
Rotation_1 = geompy.MakeRotation(Fuse_1, Line_1, alpha*math.pi/180.0)

# Внутреннее ухо
Fuse_2 = geompy.MakeFuseList(
    [
        geompy.MakeBoxDXDYDZ(box_L2, w, box_h),
        geompy.MakeTranslation(geompy.MakeCylinder(O, OY, r2, w), r2, 0, box_h)
    ],
    True,
    True
    )

Rotation_2 = geompy.MakeRotation(
    geompy.MakeTranslation(Fuse_2, rot * L  + (r1 - r2), 0, -box_h),
    Line_1,
    alpha*math.pi/180.0
    )

# обрезание внутреннего уха
cut_in = geompy.MakeCutList(Rotation_2, [boxTOcut], True)

#Сглаживание для внутреннего уха


Cut_1 = geompy.MakeCutList(Rotation_1, [cut_in], True)

Translation_3 = geompy.MakeTranslation(
    geompy.MakeBoxDXDYDZ(3 * L, w, w * 1000),
    -0.5 * (3 * L) ,
    0,
    -1 * (w * 1000 - w)
    )

#
Cut_2 = geompy.MakeCutList(Cut_1, [Translation_3], True)

simply_tesla = geompy.MakeFuseList([Box_1, Cut_2], True, True)

## грани для сглаживания на основное ухо
#smooth=\
    #geompy.GetShapesOnBoxIDs(
        #geompy.MakeBox(w, w, w + 1, L - w, 0, 0),
        #simply_tesla,
        #geompy.ShapeType["EDGE"],
        #GEOM.ST_IN
        #)

##сглаживание
#Cut_2 =\
    #geompy.MakeCutList(
    #geompy.MakeFillet(simply_tesla, w * 0.5, geompy.ShapeType["EDGE"], smooth),
    #[Translation_3],
    #True
    #)
#simply_tesla = geompy.MakeFuseList([Box_1, Cut_2], True, True)

# сглаживание на внешнее ухо (большой угол)
smooth2 =\
    geompy.GetShapesOnBoxIDs(
    geompy.MakeBox(
        (L * rot - 1) - r1 / (math.sin((90-alpha)*math.pi/180.0)),
        w,
        w + 1,
        (L * rot + 1) - r1 / (math.sin((90-alpha)*math.pi/180.0)),
        0,
        0
        ),
    simply_tesla,
    geompy.ShapeType["EDGE"],
    GEOM.ST_IN
    )
print(smooth2)

#сглаживание
Cut_2 =\
    geompy.MakeCutList(
    geompy.MakeFillet(simply_tesla, w * 15, geompy.ShapeType["EDGE"], smooth2),
    [Translation_3],
    True
    )
simply_tesla = geompy.MakeFuseList([Box_1, Cut_2], True, True)

 # зона усложненной сетки
box_split =\
    geompy.MakeCylinder(
        Vertex_1, # базовая точка
        geompy.MakeVectorDXDYDZ(0, 1, 0), # вектор
        box_mesh_X, # радиус
        w * 2
    )
t_box_split = geompy.MakeTranslation(
    box_split,
    -(step_box - (w / (math.sin((90-alpha)*math.pi/180.0))) * 0.5),
    -w,
    -(w * 0.5)
    )

box_mix =\
    geompy.MakeCylinder(
        Vertex_1, # базовая точка
        geompy.MakeVectorDXDYDZ(0, 1, 0), # вектор
        box_mesh_X, # радиус
        w * 2 # высота
    )
t_box_mix = geompy.MakeTranslation(
    box_mix,
    0,
    -w,
    -(w * 0.5)
    )

simply_box = geompy.MakeFuseList ([t_box_mix, t_box_split], True, True)

# цикл создания более одного уха

Cut_n = Cut_2
simply_tesla_n = simply_tesla
t_box_split_mirr = t_box_split
t_box_mix_mirr = t_box_mix
simply_box_n = simply_box
#while i < num:
for R in range(num - 1):
    Mirror_n = geompy.MakeMirrorByAxis(Cut_n, Line_2)
    Mirror_n2 = geompy.MakeTranslation(Mirror_n, step, 0, 0)
    simply_tesla_num = geompy.MakeFuseList([simply_tesla_n, Mirror_n2], True, True)
    Cut_n = Mirror_n2
    simply_tesla_n = simply_tesla_num
    # боксы для мелкой сетки
    #t_box_split_n = geompy.MakeMirrorByAxis(t_box_split_mirr, Line_2)
    t_box_split_n2 = geompy.MakeTranslation(t_box_split_mirr, step, 0, 0)

    #t_box_mix_n = geompy.MakeMirrorByAxis(t_box_mix_mirr, Line_2)
    t_box_mix_n2 = geompy.MakeTranslation(t_box_mix_mirr, step, 0, 0)

    simply_box_num = geompy.MakeFuseList([simply_box_n, t_box_split_n2, t_box_mix_n2])
    simply_box_n = simply_box_num

    t_box_split_mirr = t_box_split_n2
    t_box_mix_mirr = t_box_mix_n2
#    i  = i + 1

#[wall_f] = geompy.SubShapes(simply_tesla_n, [13])


# плоскости для граничных условий

if i == 1:
    simply_tesla_half = geompy.MakeCutList(
    simply_tesla_num,
    [
        geompy.MakeBox(-w, w * 0.5, -L, L + w, w * 2, L)
    ],
    True
    )

    [wall_f] =\
        geompy.GetShapesOnPlaneWithLocation(
            simply_tesla_half,
            geompy.ShapeType["FACE"],
            geompy.MakeVectorDXDYDZ(0, 1, 0),
            geompy.MakeVertex(0, 0, 0),
            GEOM.ST_ON
        )
    wall_b = geompy.MakeTranslation(wall_f, 0, w * 0.5, 0)
    # получение ID объектов для вычета их из построения вязкого подслоя сетки
    # направлением для нормали будет ось Х
    ent_ID =\
        geompy.GetShapesOnPlaneWithLocation(
            wall_f,
            geompy.ShapeType["EDGE"],
            geompy.MakeVectorDXDYDZ(1, 0, 0),
            geompy.MakeVertex(0, 0, 0),
            GEOM.ST_ON
        )
    out_ID =\
        geompy.GetShapesOnPlaneWithLocation(
            wall_f,
            geompy.ShapeType["EDGE"],
            geompy.MakeVectorDXDYDZ(1, 0, 0),
            geompy.MakeVertex(L, 0, 0),
            GEOM.ST_ON
        )
    list_ID =\
    [
        geompy.GetSubShapeID(simply_tesla_half, ent_ID[0]),
        geompy.GetSubShapeID(simply_tesla_half, out_ID[0])
    ]
    geompy.addToStudy( simply_tesla_half, 'simply_tesla_half')
    geompy.addToStudyInFather( simply_tesla_half, wall_f, 'wall_f' )

if i == 0:
    [wall_f] =\
        geompy.GetShapesOnPlaneWithLocation(
            simply_tesla_num,
            geompy.ShapeType["FACE"],
            geompy.MakeVectorDXDYDZ(0, 1, 0),
            geompy.MakeVertex(0, 0, 0),
            GEOM.ST_ON
        )
    wall_b = geompy.MakeTranslation(wall_f, 0, w, 0)
    # получение ID объектов для вычета их из построения вязкого подслоя сетки
    # направлением для нормали будет ось Х
    ent_ID =\
        geompy.GetShapesOnPlaneWithLocation(
            wall_f,
            geompy.ShapeType["EDGE"],
            geompy.MakeVectorDXDYDZ(1, 0, 0),
            geompy.MakeVertex(0, 0, 0),
            GEOM.ST_ON
        )
    out_ID =\
        geompy.GetShapesOnPlaneWithLocation(
            wall_f,
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

    geompy.addToStudyInFather( simply_tesla_num, wall_f, 'wall_f' )

ent = geompy.MakePlane(O, OX, 2000 + L)
out = geompy.MakeTranslation(ent, L, 0, 0)


geompy.addToStudy( simply_tesla_num, 'simply_tesla_num')


geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
#geompy.addToStudy( Box_2, 'Box_2' )
#geompy.addToStudy( Cylinder_1, 'Cylinder_1' )
geompy.addToStudy( Fuse_1, 'Fuse_1' )
geompy.addToStudy( Box_1, 'Box_1' )
geompy.addToStudy( Vertex_1, 'Vertex_1' )
geompy.addToStudy( Vertex_2, 'Vertex_2' )
geompy.addToStudy( Line_1, 'Line_1' )
geompy.addToStudy( Vertex_3, 'Vertex_3' )
geompy.addToStudy( Vertex_4, 'Vertex_4' )
geompy.addToStudy( Line_2, 'Line_2' )
geompy.addToStudy( Rotation_1, 'Rotation_1' )
#geompy.addToStudy( Box_3, 'Box_3' )
#geompy.addToStudy( Cylinder_2, 'Cylinder_2' )
#geompy.addToStudy( Translation_1, 'Translation_1' )
geompy.addToStudy( Fuse_2, 'Fuse_2' )
#geompy.addToStudy( Translation_2, 'Translation_2' )
geompy.addToStudy( Rotation_2, 'Rotation_2' )
geompy.addToStudy( Cut_1, 'Cut_1' )
#geompy.addToStudy( Box_4, 'Box_4' )
geompy.addToStudy( Translation_3, 'Translation_3' )
geompy.addToStudy( Cut_2, 'Cut_2' )
geompy.addToStudy( simply_tesla, 'simply_tesla')
geompy.addToStudy( Mirror_n, 'Mirror_n' )
geompy.addToStudy( Mirror_n2, 'Mirror_n2' )
geompy.addToStudy( simply_tesla_n, 'simply_tesla_n')
#geompy.addToStudy( simply_tesla_num, 'simply_tesla_num')
geompy.addToStudy( box_split, 'box_split')
geompy.addToStudy( t_box_split, 't_box_split')
geompy.addToStudy( box_mix, 'box_mix')
geompy.addToStudy( t_box_mix, 't_box_mix')
geompy.addToStudy( t_box_mix_mirr, 't_box_mix_mirr')
geompy.addToStudy( t_box_split_mirr, 't_box_split_mirr')
geompy.addToStudy( simply_box_num, 'simply_box_num')
#geompy.addToStudy(box_e_o, 'box_e_o')
#geompy.addToStudy( wall_f, 'wall_f' )
geompy.addToStudy( wall_b, 'wall_b' )
geompy.addToStudy( ent, 'ent' )
geompy.addToStudy( out, 'out' )


###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
#smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:

 # multiples meshes built in parallel, complex and numerous mesh edition (performance)
NumOfSegments = 20

if i == 0:
    Mesh_1 = smesh.Mesh(simply_tesla_num,'Mesh_1')
    Regular_1D = Mesh_1.Segment()

    # распределение слоев выдавливания
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
    NETGEN_2D_Parameters_1.SetGrowthRate( 0.0075)
    NETGEN_2D_Parameters_1.SetChordalError( -1 )
    NETGEN_2D_Parameters_1.SetChordalErrorEnabled( 0 )
    NETGEN_2D_Parameters_1.SetUseSurfaceCurvature( 1 )
    NETGEN_2D_Parameters_1.SetFuseEdges( 1 )
    #NETGEN_2D_Parameters_1.SetQuadAllowed( 1 )

    Viscous_Layers_2D_1 = NETGEN_1D_2D.ViscousLayers2D(1,3,1.1, list_ID,1)
    Viscous_Layers_2D_1.SetTotalThickness( 0.1 )
    Viscous_Layers_2D_1.SetNumberLayers( 3 )
    Viscous_Layers_2D_1.SetStretchFactor( 1 )
    Viscous_Layers_2D_1.SetEdges(list_ID , 1 )

    # плотность сетки
    NETGEN_2D_Parameters_1.SetMinSize( min_size )
    NETGEN_2D_Parameters_1.SetLocalSizeOnShape(simply_box_num, 3)
    NETGEN_2D_Parameters_1.SetMaxSize( max_size )
    isDone = Mesh_1.Compute()

    aCriteria = []
    aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_BelongToPlane,SMESH.FT_Undefined,wall_b)
    aCriteria.append(aCriterion)
    aFilter_2 = smesh.GetFilterFromCriteria(aCriteria)
    aFilter_2.SetMesh(Mesh_1.GetMesh())
    wall_b_1 = Mesh_1.GroupOnFilter( SMESH.FACE, 'wall_b', aFilter_2 )
    [ wall_f_1, wall_b_1 ] = Mesh_1.GetGroups()

    aCriteria = []
    aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_BelongToPlane,SMESH.FT_Undefined,ent)
    aCriteria.append(aCriterion)
    aFilter_3 = smesh.GetFilterFromCriteria(aCriteria)
    aFilter_3.SetMesh(Mesh_1.GetMesh())
    ent_1 = Mesh_1.GroupOnFilter( SMESH.FACE, 'ent', aFilter_3 )
    [ wall_f_1, wall_b_1, ent_1 ] = Mesh_1.GetGroups()

    aCriteria = []
    aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_BelongToPlane,SMESH.FT_Undefined,out)
    aCriteria.append(aCriterion)
    aFilter_4 = smesh.GetFilterFromCriteria(aCriteria)
    aFilter_4.SetMesh(Mesh_1.GetMesh())
    out_1 = Mesh_1.GroupOnFilter( SMESH.FACE, 'out', aFilter_4 )
    [ wall_f_1, wall_b_1, ent_1, out_1 ] = Mesh_1.GetGroups()

if i == 1:
    NumOfSegments = NumOfSegments // 2
    Mesh_1 = smesh.Mesh(simply_tesla_half,'Mesh_1')
    Regular_1D = Mesh_1.Segment()

    # распределение слоев выдавливания
    Number_of_Segments_1 = Regular_1D.NumberOfSegments(NumOfSegments, None, [])
    Number_of_Segments_1.SetConversionMode( 1 )
    Number_of_Segments_1.SetTableFunction( [0, 1, 0.05, 0.25, 0.5, 0.1, 1, 0.1] )
    Prism_3D = Mesh_1.Prism()

    wall_f_1 = Mesh_1.GroupOnGeom(wall_f,'wall_f',SMESH.FACE)
    NETGEN_1D_2D = Mesh_1.Triangle(algo=smeshBuilder.NETGEN_1D2D,geom=wall_f)
    NETGEN_2D_Parameters_1 = NETGEN_1D_2D.Parameters()
    NETGEN_2D_Parameters_1.SetSecondOrder( 0 )
    NETGEN_2D_Parameters_1.SetOptimize( 1 )
    NETGEN_2D_Parameters_1.SetFineness( 5 )
    NETGEN_2D_Parameters_1.SetGrowthRate( 0.0075)
    NETGEN_2D_Parameters_1.SetChordalError( -1 )
    NETGEN_2D_Parameters_1.SetChordalErrorEnabled( 0 )
    NETGEN_2D_Parameters_1.SetUseSurfaceCurvature( 1 )
    NETGEN_2D_Parameters_1.SetFuseEdges( 1 )
    #NETGEN_2D_Parameters_1.SetQuadAllowed( 1 )

    Viscous_Layers_2D_1 = NETGEN_1D_2D.ViscousLayers2D(1,3,1.1, list_ID,1)

    Viscous_Layers_2D_1.SetTotalThickness( 1 )
    Viscous_Layers_2D_1.SetNumberLayers( 3 )
    Viscous_Layers_2D_1.SetStretchFactor( 1 )
    Viscous_Layers_2D_1.SetEdges(list_ID , 1 )

    # плотность сетки
    NETGEN_2D_Parameters_1.SetMinSize( min_size )
    NETGEN_2D_Parameters_1.SetLocalSizeOnShape(simply_box_num, 3)
    NETGEN_2D_Parameters_1.SetMaxSize( max_size )
    isDone = Mesh_1.Compute()

    aCriteria = []
    aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_BelongToPlane,SMESH.FT_Undefined,wall_b)
    aCriteria.append(aCriterion)
    aFilter_2 = smesh.GetFilterFromCriteria(aCriteria)
    aFilter_2.SetMesh(Mesh_1.GetMesh())
    wall_b_1 = Mesh_1.GroupOnFilter( SMESH.FACE, 'wall_b', aFilter_2 )
    [ wall_f_1, wall_b_1 ] = Mesh_1.GetGroups()

    aCriteria = []
    aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_BelongToPlane,SMESH.FT_Undefined,ent)
    aCriteria.append(aCriterion)
    aFilter_3 = smesh.GetFilterFromCriteria(aCriteria)
    aFilter_3.SetMesh(Mesh_1.GetMesh())
    ent_1 = Mesh_1.GroupOnFilter( SMESH.FACE, 'ent', aFilter_3 )
    [ wall_f_1, wall_b_1, ent_1 ] = Mesh_1.GetGroups()

    aCriteria = []
    aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_BelongToPlane,SMESH.FT_Undefined,out)
    aCriteria.append(aCriterion)
    aFilter_4 = smesh.GetFilterFromCriteria(aCriteria)
    aFilter_4.SetMesh(Mesh_1.GetMesh())
    out_1 = Mesh_1.GroupOnFilter( SMESH.FACE, 'out', aFilter_4 )
    [ wall_f_1, wall_b_1, ent_1, out_1 ] = Mesh_1.GetGroups()
#Sub_mesh_1 = NETGEN_1D_2D.GetSubMesh()

### Set names of Mesh objects
#smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
#smesh.SetName(NETGEN_1D_2D.GetAlgorithm(), 'NETGEN 1D-2D')
#smesh.SetName(Prism_3D.GetAlgorithm(), 'Prism_3D')
#smesh.SetName(NETGEN_2D_Parameters_1, 'NETGEN 2D Parameters_1')
#smesh.SetName(Viscous_Layers_2D_1, 'Viscous Layers 2D_1')
#smesh.SetName(Number_of_Segments_1, 'Number of Segments_1')
smesh.SetName(wall_f_1, 'wall_f')
smesh.SetName(wall_b_1, 'wall_b')
smesh.SetName(ent_1, 'ent')
#smesh.SetName(Sub_mesh_1, 'Sub-mesh_1')
smesh.SetName(out_1, 'out')
#smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')


if salome.sg.hasDesktop():
    salome.sg.updateObjBrowser()
