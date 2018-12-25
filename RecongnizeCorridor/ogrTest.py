#!/usr/bin/python
# coding: utf-8
import log
from osgeo import ogr
import os
import feature

SHAPE_DRIVER = ogr.GetDriverByName('ESRI Shapefile')


def test_capability(path):
    ds = ogr.Open(path, 0)
    if ds is None:
        log.debug('Shape file could not open from', path)
        return
    layer = ds.GetLayer()
    capabilities = [
        ogr.OLCRandomRead,
        ogr.OLCSequentialWrite,
        ogr.OLCRandomWrite,
        ogr.OLCFastSpatialFilter,
        ogr.OLCFastFeatureCount,
        ogr.OLCFastGetExtent,
        ogr.OLCCreateField,
        ogr.OLCDeleteField,
        ogr.OLCReorderFields,
        ogr.OLCAlterFieldDefn,
        ogr.OLCTransactions,
        ogr.OLCDeleteFeature,
        ogr.OLCFastSetNextByIndex,
        ogr.OLCStringsAsUTF8,
        ogr.OLCIgnoreFields
    ]
    log.debug("Layer Capabilities:")
    for cap in capabilities:
        log.debug("  %s = %s" % (cap, layer.TestCapability(cap)))
    ds.Destroy()


def read(path=''):
    """
    读取SHP文件
    :param path:
    :return:
    """
    # 读取数据层
    datasource = SHAPE_DRIVER.Open(path, 0)  # 0 means read-only. 1 means writeable.

    layer = datasource.GetLayer(0)
    # 获取这个数据层里的点数
    n = layer.GetFeatureCount()
    log.debug('Feature count:%d' % n)
    # 读出上下左右边界
    extent = layer.GetExtent()
    log.debug('extent:%s' % str(extent))
    log.debug('ul[%s, %s] lr[%s, %s]' % (extent[0], extent[3], extent[1], extent[2]))
    # 复位
    layer.ResetReading()
    for feature in layer:
        geom = feature.GetGeometryRef()
        print(geom.Centroid().ExportToWkt())

    layer.ResetReading()
    layer_definition = layer.GetLayerDefn()
    for i in range(layer_definition.GetFieldCount()):
        field_name = layer_definition.GetFieldDefn(i).GetName()
        field_type_code = layer_definition.GetFieldDefn(i).GetType()
        field_type = layer_definition.GetFieldDefn(i).GetFieldTypeName(field_type_code)
        field_width = layer_definition.GetFieldDefn(i).GetWidth()
        precision = layer_definition.GetFieldDefn(i).GetPrecision()
        log.debug(field_name + " - " + field_type + " " + str(field_width) + " " + str(precision))


def createExtent2NewShapefile(inPath, outPath):
    ds = SHAPE_DRIVER.Open(inPath, 0)  # 0 means read-only. 1 means writeable.
    layer = ds.GetLayer()
    extent = layer.GetExtent()
    # Create a Polygon from the extent tuple
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(extent[0], extent[2])
    ring.AddPoint(extent[1], extent[2])
    ring.AddPoint(extent[1], extent[3])
    ring.AddPoint(extent[0], extent[3])
    ring.AddPoint(extent[0], extent[2])
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)

    if os.path.exists(outPath):
        SHAPE_DRIVER.DeleteDataSource(outPath)
    outDataSource = SHAPE_DRIVER.CreateDataSource(outPath)
    outLayer = outDataSource.CreateLayer("states_extent", geom_type=ogr.wkbPolygon)
    # Add an ID field
    idField = ogr.FieldDefn("id", ogr.OFTInteger)
    outLayer.CreateField(idField)
    # Create the feature and set values
    featureDefn = outLayer.GetLayerDefn()
    feature = ogr.Feature(featureDefn)
    feature.SetGeometry(poly)
    feature.SetField("id", 1)
    outLayer.CreateFeature(feature)


def createConvexHull2NewShapefile(inPath, outPath):
    ds = SHAPE_DRIVER.Open(inPath, 0)
    layer = ds.GetLayer()
    # Collect all Geometry
    geomcol = ogr.Geometry(ogr.wkbGeometryCollection)
    for feature in layer:
        geomcol.AddGeometry(feature.GetGeometryRef())
    # Calculate convex hull
    convexhull = geomcol.ConvexHull()
    # Save extent to a new Shapefile
    if os.path.exists(outPath):
        SHAPE_DRIVER.DeleteDataSource(outPath)
    outDataSource = SHAPE_DRIVER.CreateDataSource(outPath)
    outLayer = outDataSource.CreateLayer("states_convexhull", geom_type=ogr.wkbPolygon)
    # Add an ID field
    idField = ogr.FieldDefn("id", ogr.OFTInteger)
    outLayer.CreateField(idField)

    # Create the feature and set values
    featureDefn = outLayer.GetLayerDefn()
    feature = ogr.Feature(featureDefn)
    feature.SetGeometry(convexhull)
    feature.SetField("id", 1)
    outLayer.CreateFeature(feature)


def createFilterSelect2NewShapefile(inPath):
    ds = SHAPE_DRIVER.Open(inPath, 0)
    layer = ds.GetLayer()
    log.debug('createFilterSelect2NewShapefile(%s) %s' % (inPath, layer.GetGeomType()))
    # 创建outLayer self.acquire_new_layer_by_layer(layer, 'arc_filter.shp', ogr.wkbLineString)此方法不可用，不清楚原因
    outShapefile = os.path.join(os.path.split(inPath)[0], 'arc_filter.shp')
    if os.path.exists(outShapefile):
        SHAPE_DRIVER.DeleteDataSource(outShapefile)
    outDataSource = SHAPE_DRIVER.CreateDataSource(outShapefile)
    out_lyr_name = os.path.splitext(os.path.split(outShapefile)[1])[0]
    outLayer = outDataSource.CreateLayer(out_lyr_name, geom_type=ogr.wkbLineString)
    inLayerDefn = layer.GetLayerDefn()
    for i in range(0, inLayerDefn.GetFieldCount()):
        fieldDefn = inLayerDefn.GetFieldDefn(i)
        outLayer.CreateField(fieldDefn)
    log.debug('acquire_new_layer_by_layer %s' % (str(outLayer)))
    layer.SetAttributeFilter("EntityType = 'ARC' or Handle = '292296' or Handle = '292297'")
    feature.write_select_feature2layer(layer, outLayer)


def main():
    os.chdir(r'D:\GitHub\SHP&CAD')
    test_capability(r'shijiwenhuajiudian\file_Line.shp')
    read(r'shijiwenhuajiudian\file_Line.shp')
    createExtent2NewShapefile(r'shijiwenhuajiudian\file_Line.shp', r'shijiwenhuajiudian\newExtent.shp')
    createConvexHull2NewShapefile(r'shijiwenhuajiudian\file_Line.shp', r'shijiwenhuajiudian\newConvexhull.shp')
    createFilterSelect2NewShapefile(r'shijiwenhuajiudian\file_Line.shp')


if __name__ == '__main__':
    main()
