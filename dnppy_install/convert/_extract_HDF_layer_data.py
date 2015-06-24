__author__ = ['djjensen', 'jwely']

__all__ = ["_extract_HDF_layer_data"]

import gdal
import os

def _extract_HDF_layer_data(hdfpath, layer_indexs = None):
    """
    Extracts one or more layers from an HDF file and returns a dictionary with
    all the data available in the HDF layer for use in further format conversion
    to better supported formats.

    example:
    hdfpath = filepath to an hdf file. (any HDF 4 or 5 datatype)
    layer indexs = [1,2,3]

    the output dict will have keys :
                    ["MasterMetadata", "1", "2", "3"]

    where the "MasterMetadata" values very widely in format depending on
    data source, but should contain georeferencing information and the like.
    Each of the values for those integer keys will be a list of
    values that looks like this.

        [layer name descriptor, projection, geotransform, numpy_array]

    gdal has proven annoying to use, but this function should help you
    get started with programming support for any HDF datatype. Building
    proper geotransormation will require info in the MasterMetadata most
    likely, but there is not an established naming convention that can be
    applied to all datatypes.
    """

    # output dict
    out_info = {}
    layer_names = []

    # open the HDF dataset
    hdf_dataset = gdal.Open(hdfpath)

    try:
        subdatasets = hdf_dataset.GetSubDatasets()

        if layer_indexs is None:
            layer_indexs = range(len(subdatasets))
        elif isinstance(layer_indexs, int):
            layer_indexs = [layer_indexs]

        print("Contents of {0}".format(os.path.basename(hdfpath)))
        for i, dataset_string in enumerate(subdatasets):
            print("  {0}  {1}".format(i, dataset_string[1]))
            if i in layer_indexs:
                layer_names.append(dataset_string[1])

        # give metadata info for the entire layer
        mdict = hdf_dataset.GetMetadata()
        out_info["MasterMetadata"] = mdict
        #for key in mdict:
        #   print key," = ", mdict[key]

        # perform operation on each of the desired layers
        for i,layer in enumerate(layer_indexs):
            subdataset   = gdal.Open(subdatasets[layer][0])
            #projection   = subdataset.GetProjection()
            #geotransform = subdataset.GetGeoTransform()
            #numpy_array  = subdataset.ReadAsArray()

            out_info[i] = subdataset
            print subdataset

        return out_info

    except:
        raise Exception("this function doesn't yet work for HDF5s with just a single layer")



if __name__ == "__main__":
    #try MODIS
    rasterpath = r"C:\Users\jwely\Desktop\troubleshooting\MOD09A1.A2015033.h11v05.005.2015044233105.hdf"
    _extract_HDF_layer_data(rasterpath)

    # try GPM
    rasterpath = r"C:\Users\jwely\Desktop\troubleshooting\3B-HHR-L.MS.MRG.3IMERG.20150401-S233000-E235959.1410.V03E.RT-H5"
    _extract_HDF_layer_data(rasterpath)

    # try TRMM
    rasterpath = r"C:\Users\jwely\Desktop\troubleshooting\3B42.20140101.00.7.HDF"
    _extract_HDF_layer_data(rasterpath)

    # try something else?
    rasterpath = r"C:\Users\jwely\Desktop\troubleshooting\AG100.v003.28.-098.0001.h5"
    _extract_HDF_layer_data(rasterpath)