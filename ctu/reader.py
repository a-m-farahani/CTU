import pydicom as dcm
import numpy as np
import scipy.ndimage
from skimage import measure
from skimage import morphology
from matplotlib import pyplot as plt
import os
import warnings

def ReadCT(ct_dir, select_only_size=None):
    file_list = os.listdir(ct_dir)
    if len(file_list)<2:
        print(ct_dir, " -> Invalid CT directory address.")
        return None
    elif len(file_list) > 2000:
        warnings.warn("Too many slices. It might cause memory issues.")        

    # Reading CT slices that exist in ct_dir
    slices = []
    for slc in file_list:
        ds = dcm.read_file(ct_dir + "/" + slc)
        if select_only_size is not None:
            if ds.pixel_array.shape[0] == select_only_size:
                slices.append(ds)
        #print(slc, " --> ", ds.pixel_array.shape)
    #slices.sort(key = lambda slc: int(slc.InstanceNumber))


    try:
        thickness = abs(slices[len(slices)//2].ImagePositionPatient[2] - slices[len(slices)//2 + 1].ImagePositionPatient[2])
    except:
        thickness = abs(slices[len(slices)//2].SliceLocation - slices[len(slices)//2 + 1].SliceLocation)
    for slc in slices:
        slc.SliceThickness = thickness
    
    return slices
    

def ReadSlice(slice_path):
    try:
        ds = dcm.read_file(slice_path)
        return ds
    except:
        print("Error in reading file \"", slice_path, "\"")
        return None



def getImage(dicom_dataset):
    img = dicom_dataset.pixel_array
    min_ = img.min()
    max_ = img.max()

    img = (img-min_)/(max_-min_ + 1e-6)
    img = img * 255
    return img.astype(np.uint8)


def getImageHU(dicom_dataset):
    hu = dcm.pixel_data_handlers.util.apply_modality_lut(dicom_dataset.pixel_array,dicom_dataset)
    return hu.astype(np.int16)

def getWindowedImage(dicom_dataset, wtype=None):
    """
    Rescales a CT scan Slice image to a specific windowing
    inputs:
        dicom_dataset: a dicom DataSet
        wtype: a string or tuple, tuple consists (WindowCenter, WindowWidth) or string can be
            'lung', 'brain', 'bone', 'liver', 'tissues', 'mediastinum'
    output:
        a numpy 2-d array of result image
    """
    if wtype is None:
        wc = -600
        ww = 1500
    elif type(wtype) == str:
        tmp = getWindowValues(wtype)
        wc = tmp[0]
        ww = tmp[1]
    elif type(wtype) == tuple:
        wc = wtype[0]
        ww = wtype[1]
    else:
        print("Error. -> Invalid wtype argument.")
        return None

    hf_img = dcm.pixel_data_handlers.util.apply_modality_lut(dicom_dataset.pixel_array,dicom_dataset)
    dicom_dataset.WindowCenter = wc
    dicom_dataset.WindowWidth = ww
    res = dcm.pixel_data_handlers.util.apply_voi_lut(hf_img, dicom_dataset, index=0)
    return res

def getWindowValues(wtype="lung"):
    hf_values = {
        "lung": (-600, 1500),
        "mediastinum": (50, 350),
        "tissues" : (50, 400),
        "liver": (30, 150),
        "brain": (40, 80),
        "bone" : (400, 1800) }
    return hf_values[wtype]



