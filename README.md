# CTU
<b>CT</b> Scan <b>U</b>tilities. A set of useful methods for working with CT scan <b>dicom</b> files as simple as possible in python.


dependencies:
* pydicom
* numpy
* scipy
* matplotlib
* plotly


<b> Read a single slice from a CT Scan:</b>
```python
from ctu import reader
slice = reader.ReadSlice("path to CT slice")
print(slice)
```
slice is a dicom DataSet object that contains pixel data and other metadata. Dataset object is the primary object and is used in many methods.

<b> Read a CT scan</b>
```python
from ctu import reader
ct_slices = reader.ReadCT("path to a CT Scan directory")
print(len(ct_slices))
```

<b> Plot Slices of a CT Scan:</b>
```python
from ctu import reader, display
slices = reader.ReadCT("path to a CT Scan directory")
display.PlotSlices(slices,wtype='lung',nrows=5,ncols=5, step=2)
````
<p>
    <img src="https://github.com/a-m-farahani/CTU/blob/master/examples/plot_slices.jpg" height="400" title="Slice Plot"/>
</p>
wtype can be a string from ['lung' , 'bone' , 'liver' , 'tissues'] or a tuple which specifies custom WindowCenter and WindowWidth. </br>

<br/><br/><b> Working with Image data </b></br>
<b> Get image in Hounsfield scale:</b>
```python
from ctu import reader, display
slice = reader.ReadSlice("path to a slice")
img = reader.getImageHU(slice)
display.Plot(img)
```
<b> Get image in a certain Windowing condition: </b>
```python
from ctu import reader, display
slice = reader.ReadSlice("path to slice")
img = reader.getWindowedImage(slice, wtype='lung')
display.Plot(img) 
```
<p align="left">
  <img src="https://github.com/a-m-farahani/CTU/blob/master/examples/display_plot_lung.jpg" height="300" title="Lung View">
  <img src="https://github.com/a-m-farahani/CTU/blob/master/examples/display_plot_bone.jpg" height="300" title="Bone View" >
</p>


<b> Plot a CT Scan in 3D </b>
```python
from ctu import reader, display
slices = reader.ReadCT("path to a CT Scan folder")
display.Plot3D(slices, threshold=400)
```
<p align="left">
  <img src="https://github.com/a-m-farahani/CTU/blob/master/examples/display_3dplot.jpg" height="300" title="Bone View 3D">
</p>


<br/><b> Mask body part in CT slices</b>
```python
from ctu import reader, transform
slice = reader.ReadSlice("path to a slice")
img = reader.getWindowedImage(slice, 'lung')
mask, masked_image = transform.BodyMask(img) 
```
<p align="left">
  <img src="https://github.com/a-m-farahani/CTU/blob/master/examples/bodymask.jpg" height="250" title="Body Mask">
</p>

<br/><b> Lung mask of a CT Slice</b>
```python
from ctu import reader, transform
slice = reader.ReadSlice("path to a slice")
img = reader.getImageHU(slice)
label, mask, masked_image = transform.LungMask(img) 
```
<p align="left">
  <img src="https://github.com/a-m-farahani/CTU/blob/master/examples/lungmask.jpg" height="250" title="Lung Mask">
</p>
K-Means clustering is used to detect different parts in image. "lable" is the output of K-Means clustering and "mask" is the computed lung mask.
