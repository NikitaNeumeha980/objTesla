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

#для построения половины сетки в продольном сечении i = 1 i2 = 0.5, иначе i = 0, i2 = 1
i = 1
i2 = 0.5

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
min_size = 3
max_size = 6
size_special = min_size * 1.1
NumOfSegments = 10

geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

# основной канал
Box_1 = geompy.MakeTranslation(
    geompy.MakeFaceObjHW(OY, w, L),
    L * 0.5,
    0,
    w * 0.5
    )

# ось поворота "ушек"
Line_1 = geompy.MakeLineTwoPnt(
    geompy.MakeVertex(rot * L + 2 * r1, 0, w),
    geompy.MakeVertex(rot * L + 2 * r1, w, w)
    )

# ось отражения для случаев когда кол-во "ушек" > 1
Line_2 = geompy.MakeLineTwoPnt(
    geompy.MakeVertex(0, 0.5 * w * i2, 0.5 * w),
    geompy.MakeVertex(w, 0.5 * w * i2, 0.5 * w)
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
        geompy.MakeBoxDXDYDZ(3 * L, w * i2, w * 1000),
        0,
        0,
        -1 * (w * 1000 - w)
    ),
    Line_1_1,
    -0.1 * alpha*math.pi/180.0
    )

#Внутренее ухо +
# обрезание внутреннего уха
cut_in = geompy.MakeCutList(
    geompy.MakeRotation(
        geompy.MakeTranslation(
            geompy.MakeFuseList(
            [
                geompy.MakeTranslation(
                    geompy.MakeFaceObjHW(OY, box_h, box_L2),
                    box_L2 * 0.5,
                    0,
                    box_h * 0.5
                    ),
                geompy.MakeTranslation(geompy.MakeDiskPntVecR(O, OY, r2), r2, 0, box_h)
            ]
            ),
        rot * L  + (r1 - r2),
        0,
        -box_h
        ),
    Line_1,
    alpha*math.pi/180.0
    ),
    [boxTOcut],
    )

# Внешнее ухо
Cut_2 = geompy.MakeCutList(
    geompy.MakeCutList(
        geompy.MakeRotation(
            geompy.TranslateDXDYDZ(
                geompy.MakeFuseList(
                    [
                        geompy.MakeTranslation(
                            geompy.MakeFaceObjHW(OY, box_h, box_L1),
                            box_L1 * 0.5,
                            0,
                            box_h * 0.5
                        ),
                        geompy.TranslateDXDYDZ(geompy.MakeDiskPntVecR(O, OY, r1), r1, 0, box_h)
                    ]
                ),
                rot * L ,
                0,
                -box_h
            ),
            Line_1,
            alpha*math.pi/180.0
        ),
        [cut_in]
    ),
    [
        geompy.MakeTranslation(
            geompy.MakeBoxDXDYDZ(3 * L, w * i2, w * 1000),
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
geompy.addToStudy( Cut_2, 'Cut_2')
geompy.addToStudy( cut_in, 'cut_in')
geompy.addToStudy( Box_1, 'Box_1')
#test =  geompy.MakeTranslation(
    #geompy.MakeFaceObjHW(OY, box_h, box_L1),
    #box_L1 * 0.5,
    #0,
    #box_h * 0.5
    #)
#geompy.addToStudy( test,'test')

test =     geompy.MakeFillet2D(
        simply_tesla,
        w * 15,
        geompy.GetShapesOnBoxIDs(
            geompy.MakeBox(
                (L * rot - 1) - r1 / (math.sin((90-alpha)*math.pi/180.0)),
                w,
                w + 1,
                (L * rot + 1) - r1 / (math.sin((90-alpha)*math.pi/180.0)),
                -w,
                0
            ),
    simply_tesla,
    geompy.ShapeType["VERTEX"],
    GEOM.ST_IN
    )
    )

geompy.addToStudy(test, 'test')

test2 = geompy.MakeTranslation(
            geompy.MakeBoxDXDYDZ(3 * L, w , w * 1000),
            -0.5 * (3 * L) ,
            -w * 0.5,
            -1 * (w * 1000 - w)
        )

geompy.addToStudy(test2,'test2')


#сглаживание
Cut_2 =\
    geompy.MakeCutList(
        geompy.MakeFillet2D(
            simply_tesla,
            w * 15,
            geompy.GetShapesOnBoxIDs(
                geompy.MakeBox(
                    (L * rot - 1) - r1 / (math.sin((90-alpha)*math.pi/180.0)),
                    w,
                    w + 1,
                    (L * rot + 1) - r1 / (math.sin((90-alpha)*math.pi/180.0)),
                    -w,
                    0
                ),
        simply_tesla,
        geompy.ShapeType["VERTEX"],
        GEOM.ST_IN
        )
    ),
    [
        geompy.MakeTranslation(
            geompy.MakeBoxDXDYDZ(3 * L, w , w * 1000),
            -0.5 * (3 * L) ,
            -w * 0.5,
            -1 * (w * 1000 - w)
        )
    ],
    True
    )

simply_tesla = geompy.MakeFuseList([Box_1, Cut_2], True, True)
geompy.addToStudy( simply_tesla, 'simply_tesla2')



if salome.sg.hasDesktop():
    salome.sg.updateObjBrowser()









