#!/usr/bin/python
# coding: utf-8
import log
from osgeo import ogr


class BaseFeat(object):
    __slots__ = ('__feat',)

    def __init__(self, feat):
        self.__feat = feat


class LineFeat(BaseFeat):
    pass


class ARCFeat(BaseFeat):
    pass


class CircleFeat(BaseFeat):
    pass


def printFeature(feat):
    try:
        lyr = feat.GetField('Layer')
        handle = feat.GetField('Handle')
        entityType = feat.GetField('EntityType')
        lineType = feat.GetField('LineType')
        color = feat.GetField('Color')
        colorType = feat.GetField('ColorType')
        lineWidth = feat.GetField('LineWidth')
        constWidth = feat.GetField('ConstWidth')
        sizeScale = feat.GetField('SizeScale')
        # 提取feature的几何形状
        geom = feat.GetGeometryRef()
        log.debug(
            'Layer:%s,EntityType:%s,Handle:%s,LineType:%s,Color:%s,ColorType:%s,LineWidth:%s,ConstWidth:%s,SizeScale:%s'
            '\n geom:%s'
            % (lyr, entityType, handle, lineType, color, colorType, lineWidth, constWidth, sizeScale, str(geom)))
    except ValueError:
        log.error('GetField id fail!')


def write_select_feature2layer(layer, outLayer):
    log.debug('write_select_feature2layer %s --> %s' % (str(layer), str(outLayer)))
    # Get the output Layer's Feature Definition
    outLayerDefn = outLayer.GetLayerDefn()
    layer.ResetReading()
    for inFeat in layer:
        # 打印Feature内容
        printFeature(inFeat)
        # Create output Feature
        outFeature = ogr.Feature(outLayerDefn)
        # Add field values from input Layer
        for i in range(0, outLayerDefn.GetFieldCount()):
            outFeature.SetField(outLayerDefn.GetFieldDefn(i).GetNameRef(),
                                inFeat.GetField(i))
        geom = inFeat.GetGeometryRef()
        outFeature.SetGeometry(geom.Clone())
        # Add new feature to output Layer
        outLayer.CreateFeature(outFeature)
        inFeat.Destroy()
