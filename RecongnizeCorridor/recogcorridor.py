#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import DrawingHandler
import ogrTest


def main():
    os.chdir(r'D:\GitHub\SHP&CAD')
    # ogrTest.test_capability(r'shijiwenhuajiudian\file_Line.shp')
    # ogrTest.read(r'shijiwenhuajiudian\file_Line.shp')
    # ogrTest.createExtent2NewShapefile(r'shijiwenhuajiudian\file_Line.shp', r'shijiwenhuajiudian\newExtent.shp')
    # ogrTest.createConvexHull2NewShapefile(r'shijiwenhuajiudian\file_Line.shp', r'shijiwenhuajiudian\newConvexhull.shp')
    sd = DrawingHandler.ShapeDrawing(r'shijiwenhuajiudian\file_Line.shp', r'shijiwenhuajiudian\out_default.shp')
    sd.outPath = r'D:\GitHub\SHP&CAD\shijiwenhuajiudian\newExtent.shp'
    sd.createFilterSelect2NewShapefile()


if __name__ == '__main__':
    main()
    pass
