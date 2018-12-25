#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import log
import sys
import os
import feature

try:
    from osgeo import ogr, osr, gdal

    log.info('Import of ogr from osgeo worked.  Hurry up!\n')
except ImportError:
    sys.exit('ERROR: cannot find GDAL/OGR modules!\n')


def check_gdal_version():
    """
    检查GDAL版本
    :return:
    """
    version_num = int(gdal.VersionInfo('VERSION_NUM'))
    if version_num < 1100000:
        sys.exit('ERROR: Python bindings of GDAL 1.10 or later required')
    log.info('GDAL VERSION NUM:%s\n' % version_num)


#  GDAL error handler functionlogging
def gdal_error_handler(err_class, err_num, err_msg):
    err_type = {
        gdal.CE_None: 'None',
        gdal.CE_Debug: 'Debug',
        gdal.CE_Warning: 'Warning',
        gdal.CE_Failure: 'Failure',
        gdal.CE_Fatal: 'Fatal'
    }
    err_msg = err_msg.replace('\n', ' ')
    err_class = err_type.get(err_class, 'None')
    log.error('Error Number:%s Error Type:%s Error Message:%s' % (err_num, err_class, err_msg))


class ShapeDrawing(object):
    """
    图纸计算
    """
    __slots__ = ('__inPath', '__outPath', '__inDataSource', '__outDataSource', '__ESRI_Driver')

    def __init__(self, inPath='', outPath=''):
        check_gdal_version()
        # Enable GDAL/OGR exceptions  gdal.DontUseExceptions()
        gdal.UseExceptions()
        # install error handler
        gdal.PushErrorHandler(gdal_error_handler)
        self.__ESRI_Driver = ogr.GetDriverByName('ESRI Shapefile')
        self.__inPath = inPath
        self.__outPath = outPath
        self.__inDataSource = None
        self.__outDataSource = None

    def __del__(self):
        gdal.PopErrorHandler()
        self.__inPath = None
        self.__outPath = None
        if self.__inDataSource is not None:
            self.__inDataSource.Destroy()
        self.__inDataSource = None
        if self.__outDataSource is not None:
            self.__outDataSource.Destroy()
        self.__outDataSource = None

    @property
    def inPath(self):
        return self.__inPath

    @inPath.setter
    def inPath(self, path):
        self.__inPath = path
        self.__inDataSource = None

    @property
    def outPath(self):
        return self.__outPath

    @outPath.setter
    def outPath(self, path):
        self.__outPath = path
        self.__outDataSource = None

    def getInDataSource(self, path=''):
        if path.strip():
            self.__inPath = path
            self.__outDataSource = None
        if self.__inDataSource is None:
            driver = ogr.GetDriverByName('ESRI Shapefile')
            self.__inDataSource = driver.Open(self.__inPath, 0)  # 0 means read-only. 1 means writeable.
            if self.__inDataSource is None:
                log.debug('Shape file could not open from %s' % self.__inPath)
                sys.exit(1)
            log.debug('Shape file opened from %s' % self.__inPath)
        return self.__inDataSource

    def getOutDataSource(self, path=''):
        """
        获取输出数据源
        :return: outDataSource
        """
        log.debug('getOutDataSource(%s)' % path)
        if path.strip():
            if os.path.exists(path):
                self.__ESRI_Driver.DeleteDataSource(path)
            return self.__ESRI_Driver.CreateDataSource(path)
        elif self.__outDataSource is None:
            # Remove output shapefile if it already exists
            if os.path.exists(self.__outPath):
                self.__ESRI_Driver.DeleteDataSource(self.__outPath)
            # Create the output shapefile
            self.__outDataSource = self.__ESRI_Driver.CreateDataSource(self.__outPath)
        return self.__outDataSource

    def acquire_new_layer_by_layer(self, in_layer, file_name, geomType):
        outShapefile = os.path.join(os.path.split(self.__inPath)[0], file_name)
        outDataSource = self.getOutDataSource(outShapefile)
        out_lyr_name = os.path.splitext(os.path.split(outShapefile)[1])[0]
        outLayer = outDataSource.CreateLayer(out_lyr_name, geom_type=geomType)
        inLayerDefn = in_layer.GetLayerDefn()
        for i in range(0, inLayerDefn.GetFieldCount()):
            fieldDefn = inLayerDefn.GetFieldDefn(i)
            outLayer.CreateField(fieldDefn)
        log.debug('acquire_new_layer_by_layer filename:%s, geomType:%s -->%s' % (file_name, geomType, str(outLayer)))
        return outLayer

    def createFilterSelect2NewShapefile(self, path=''):
        ds = self.getInDataSource()
        layer = ds.GetLayer()
        log.debug('createFilterSelect2NewShapefile(%s) %s' % (path, layer.GetGeomType()))
        # 创建outLayer self.acquire_new_layer_by_layer(layer, 'arc_filter.shp', ogr.wkbLineString)此方法不可用，不清楚原因
        outShapefile = os.path.join(os.path.split(self.__inPath)[0], 'arc_filter.shp')
        outDataSource = self.getOutDataSource(outShapefile)
        out_lyr_name = os.path.splitext(os.path.split(outShapefile)[1])[0]
        outLayer = outDataSource.CreateLayer(out_lyr_name, geom_type=ogr.wkbLineString)
        inLayerDefn = layer.GetLayerDefn()
        for i in range(0, inLayerDefn.GetFieldCount()):
            fieldDefn = inLayerDefn.GetFieldDefn(i)
            outLayer.CreateField(fieldDefn)
        log.debug('acquire_new_layer_by_layer %s' % (str(outLayer)))
        layer.SetAttributeFilter("EntityType = 'ARC' or Handle = '292296' or Handle = '292297'")
        feature.write_select_feature2layer(layer, outLayer)
