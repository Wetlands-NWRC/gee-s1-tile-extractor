import ee
import geopandas as gpd


AOI = ee.Geometry
DateRange = tuple[str]
Sentinel1DV = ee.ImageCollection
Sentinel1DH = ee.ImageCollection
S1 = ee.Image


class Sentinel1(ee.ImageCollection):
    def __init__(self) -> None:
        """ Extends the ee.ImageCollection class to create a Sentinel1 class """
        super().__init__("COPERNICUS/S1_GRD")


    def insert_groupid(self):
        def _insert_groupid(image: S1) -> S1:
            cent_x = image.geometry().centroid(1).coordinates().get(0).format("%.2f")
            rel_orbit = image.get('relativeOrbitNumber_start').format("%d")
            id = ee.String(rel_orbit).cat('_').cat(cent_x)
            return image.set('group_id', id)
        return self.map(_insert_groupid)


@classmethod
def from_image_collection(cls, collection: Sentinel1DV | Sentinel1DH) -> Sentinel1:
    """ Class Factory methods to create a Feature Collection from a Sentinel1 Image Collection """
    # check to see if the input collection is empty
    if collection.size().eq(0).getInfo():
        raise ValueError('Input collection is empty')
    
    # convert the image collection to a feature collection
    fc = collection.map(lambda image: ee.Feature(image.geometry(), image.toDictionary()))
    
    # create a feature collection object
    return cls(fc)
ee.FeatureCollection.fromImageCollection = from_image_collection


def extract_tiles(aoi: AOI, date_range: DateRange) -> gpd.GeoDataFrame:
    """ Extracts all sen """
    # create a sentinel1 image collection object
    s1 = Sentinel1()
    
    # filter the image collection based on the date range and aoi
    s1 = s1.filterBounds(aoi).filterDate(*date_range)
    
    # insert a group id to the image collection
    s1 = s1.insert_groupid()
    
    # convert the image collection to a feature collection
    fc = ee.FeatureCollection.fromImageCollection(s1)
    
    # convert the feature collection to a geodataframe
    gdf = gpd.GeoDataFrame.from_features(fc.getInfo()['features'])
    gdf['transmitterReceiverPolarisation'] = gdf['transmitterReceiverPolarisation'].apply(', '.join)
    return gdf
    