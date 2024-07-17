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
min_size = 10
max_size = 20
size_special = min_size * 1.1
NumOfSegments = 10

geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

# основной канал
Box_1 = geompy.MakeBoxDXDYDZ(L, w, w)

# ось поворота "ушек"
Line_1 = geompy.MakeLineTwoPnt(
    geompy.MakeVertex(rot * L + 2 * r1, 0, w),
    geompy.MakeVertex(rot * L + 2 * r1, w, w)
    )

# ось отражения для случаев когда кол-во "ушек" > 1
Line_2 = geompy.MakeLineTwoPnt(
    geompy.MakeVertex(0, 0.5 * w, 0.5 * w),
    geompy.MakeVertex(w, 0.5 * w, 0.5 * w)
    )


# ось поворота бокса для обрезания внутреннего "ушка"
Line_1_1 = geompy.MakeTranslation(
    Line_1,
    - ((2 * r1) /  (math.sin((90-alpha)*math.pi/180.0)) - w /  (math.sin((90-alpha)*math.pi/180.0))),
    0,
    0,
    )

# бокс для обрезания внутреннего уха
boxTOcut = geompy.MakeRotation(
    geompy.MakeTranslation(
        geompy.MakeBoxDXDYDZ(3 * L, w, w * 1000),
        0,
        0,
        -1 * (w * 1000 - w)
    ),
    Line_1_1,
    -0.1 * alpha*math.pi/180.0
    )

geompy.addToStudy(Line_1_1, 'Line_1_1')
geompy.addToStudy(Line_1, 'Line_1')
geompy.addToStudy(boxTOcut, 'boxTOcut')

#Внутренее ухо +
# обрезание внутреннего уха
cut_in = geompy.MakeCutList(
    geompy.MakeRotation(
        geompy.MakeTranslation(
            geompy.MakeFuseList(
            [
                geompy.MakeBoxDXDYDZ(box_L2, w, box_h),
                geompy.MakeTranslation(geompy.MakeCylinder(O, OY, r2, w), r2, 0, box_h)
            ],
            True,
            True
            ),
        rot * L  + (r1 - r2),
        0,
        -box_h
        ),
    Line_1,
    alpha*math.pi/180.0
    ),
    [boxTOcut],
    True
    )

# Внешнее ухо
Cut_2 = geompy.MakeCutList(
    geompy.MakeCutList(
        geompy.MakeRotation(
            geompy.TranslateDXDYDZ(
                geompy.MakeFuseList(
                    [
                        geompy.MakeBoxDXDYDZ(box_L1, w, box_h),
                        geompy.TranslateDXDYDZ(geompy.MakeCylinder(O, OY, r1, w), r1, 0, box_h)
                    ],
                    True,
                    True
                ),
                rot * L ,
                0,
                -box_h
            ),
            Line_1,
            alpha*math.pi/180.0
        ),
        [cut_in],
        True
    ),
    [
        geompy.MakeTranslation(
            geompy.MakeBoxDXDYDZ(3 * L, w, w * 1000),
            -0.5 * (3 * L) ,
            0,
            -1 * (w * 1000 - w)
        )
    ],
    True
    )

# основная геометрия
simply_tesla = geompy.MakeFuseList([Box_1, Cut_2], True, True)
geompy.addToStudy( simply_tesla, 'simply_tesla')

#сглаживание
Cut_2 =\
    geompy.MakeCutList(
    geompy.MakeFillet(
        simply_tesla,
        w * 15,
        geompy.ShapeType["EDGE"],
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
    ),
    [
        geompy.MakeTranslation(
            geompy.MakeBoxDXDYDZ(3 * L, w, w * 1000),
            -0.5 * (3 * L) ,
            0,
            -1 * (w * 1000 - w)
        )
    ],
    True
    )
simply_tesla = geompy.MakeFuseList([Box_1, Cut_2], True, True)

# зона усложненной сетки
simply_box = geompy.MakeFuseList (
    [
        geompy.MakeTranslation(
            geompy.MakeCylinder(
                geompy.MakeVertex(rot * L + 2 * r1, 0, w), # базовая точка
                geompy.MakeVectorDXDYDZ(0, 1, 0), # вектор
                box_mesh_X, # радиус
                w * 2 # высота
            ),
            0,
            -w,
            -(w * 0.5)
        ),
        geompy.MakeTranslation(
            geompy.MakeCylinder(
                geompy.MakeVertex(rot * L + 2 * r1, 0, w), # базовая точка
                geompy.MakeVectorDXDYDZ(0, 1, 0), # вектор
                box_mesh_X, # радиус
                w * 2
            ),
            -(step_box - (w / (math.sin((90-alpha)*math.pi/180.0))) * 0.5),
            -w,
            -(w * 0.5)
        )
    ],
    True,
    True
    )

# цикл создания более одного уха
Cut_n = Cut_2
simply_tesla_n = simply_tesla
simply_box_n = simply_box
#while i < num:
for R in range(num - 1):
    Mirror_n = geompy.MakeMirrorByAxis(Cut_n, Line_2)
    Mirror_n2 = geompy.MakeTranslation(Mirror_n, step, 0, 0)
    simply_tesla_num = geompy.MakeFuseList([simply_tesla_n, Mirror_n2], True, True)
    Cut_n = Mirror_n2
    simply_tesla_n = simply_tesla_num
    #боксы для мелкой сетки
    simply_box_n2 = geompy.MakeTranslation(simply_box_n, step, 0, 0)
    simply_box_num = geompy.MakeFuseList([simply_box_n, simply_box_n2])
    simply_box_n = simply_box_num

geompy.addToStudy( simply_box_num,'simply_box_num')

# плоскости для граничных условий
if i == 1:
    simply_tesla_half = geompy.MakeCutList(
    simply_tesla_num,
    [
        geompy.MakeBox(-w, w * 0.5, -L, L + w, w * 2, L)
    ],
    False
    )

    [wall_f] =\
        geompy.GetShapesOnPlaneWithLocation(
            simply_tesla_half,
            geompy.ShapeType["FACE"],
            geompy.MakeVectorDXDYDZ(0, 1, 0),
            geompy.MakeVertex(0, 0, 0),
            GEOM.ST_ON
        )
    wall_b = geompy.MakePlane(
        geompy.MakeVertex(L * 0.5, w * 0.5, w * 0.5),
        OY,
        2000 + L)
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
    wall_b = geompy.MakePlane(
        geompy.MakeVertex(L * 0.5, w, w * 0.5),
        OY,
        2000 + L)
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

    geompy.addToStudy( simply_tesla_num, 'simply_tesla_num')
    geompy.addToStudyInFather( simply_tesla_num, wall_f, 'wall_f' )

ent = geompy.MakePlane(O, OX, 2000 + L)
out = geompy.MakeTranslation(ent, L, 0, 0)

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
#smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:

 # multiples meshes built in parallel, complex and numerous mesh edition (performance)

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
    Viscous_Layers_2D_1.SetTotalThickness( 2.5 )
    Viscous_Layers_2D_1.SetNumberLayers( 3 )
    Viscous_Layers_2D_1.SetStretchFactor( 1 )
    Viscous_Layers_2D_1.SetEdges(list_ID , 1 )

    # плотность сетки
    NETGEN_2D_Parameters_1.SetMinSize( min_size )
    NETGEN_2D_Parameters_1.SetLocalSizeOnShape(simply_box_num, size_special)
    NETGEN_2D_Parameters_1.SetMaxSize( max_size )
    isDone = Mesh_1.Compute()

    aCriteria = []
    aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_BelongToPlane,SMESH.FT_Undefined,wall_b)
    aCriteria.append(aCriterion)
    aFilter_2 = smesh.GetFilterFromCriteria(aCriteria)
    aFilter_2.SetMesh(Mesh_1.GetMesh())
    wall_b_1 = Mesh_1.GroupOnFilter( SMESH.FACE, 'wall_b', aFilter_2 )
    #[ wall_f_1, wall_b_1 ] = Mesh_1.GetGroups()

    aCriteria = []
    aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_BelongToPlane,SMESH.FT_Undefined,ent)
    aCriteria.append(aCriterion)
    aFilter_3 = smesh.GetFilterFromCriteria(aCriteria)
    aFilter_3.SetMesh(Mesh_1.GetMesh())
    ent_1 = Mesh_1.GroupOnFilter( SMESH.FACE, 'ent', aFilter_3 )
    #[ wall_f_1, wall_b_1, ent_1 ] = Mesh_1.GetGroups()

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
    Number_of_Segments_1 = Regular_1D.NumberOfSegments(5, None, [])
    Number_of_Segments_1.SetConversionMode( 1 )
    Number_of_Segments_1.SetTableFunction( [0, 1, 0.05, 0.25, 1, 0.1] )

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

    Viscous_Layers_2D_1.SetTotalThickness( 2.5 )
    Viscous_Layers_2D_1.SetNumberLayers( 3 )
    Viscous_Layers_2D_1.SetStretchFactor( 1 )
    Viscous_Layers_2D_1.SetEdges(list_ID , 1 )

    # плотность сетки
    NETGEN_2D_Parameters_1.SetMinSize( min_size )
    NETGEN_2D_Parameters_1.SetLocalSizeOnShape(simply_box_num, size_special)
    NETGEN_2D_Parameters_1.SetMaxSize( max_size )
    isDone = Mesh_1.Compute()

    aCriteria = []
    aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_BelongToPlane,SMESH.FT_Undefined,wall_b)
    aCriteria.append(aCriterion)
    aFilter_2 = smesh.GetFilterFromCriteria(aCriteria)
    aFilter_2.SetMesh(Mesh_1.GetMesh())
    wall_b_1 = Mesh_1.GroupOnFilter( SMESH.FACE, 'wall_b', aFilter_2 )
    #[ wall_f_1, wall_b_1 ] = Mesh_1.GetGroups()

    aCriteria = []
    aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_BelongToPlane,SMESH.FT_Undefined,ent)
    aCriteria.append(aCriterion)
    aFilter_3 = smesh.GetFilterFromCriteria(aCriteria)
    aFilter_3.SetMesh(Mesh_1.GetMesh())
    ent_1 = Mesh_1.GroupOnFilter( SMESH.FACE, 'ent', aFilter_3 )
    #[ wall_f_1, wall_b_1, ent_1 ] = Mesh_1.GetGroups()

    aCriteria = []
    aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_BelongToPlane,SMESH.FT_Undefined,out)
    aCriteria.append(aCriterion)
    aFilter_4 = smesh.GetFilterFromCriteria(aCriteria)
    aFilter_4.SetMesh(Mesh_1.GetMesh())
    out_1 = Mesh_1.GroupOnFilter( SMESH.FACE, 'out', aFilter_4 )

    [ wall_f_1, wall_b_1, ent_1, out_1 ] = Mesh_1.GetGroups()

smesh.SetName(wall_f_1, 'wall_f')
smesh.SetName(wall_b_1, 'wall_b')
smesh.SetName(ent_1, 'ent')
smesh.SetName(out_1, 'out')


if salome.sg.hasDesktop():
    salome.sg.updateObjBrowser()
































