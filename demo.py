from ctu import reader,display, transform
from matplotlib import pyplot as plt

slices = reader.ReadCT("C:\\Users/farah/Desktop/COVID-19/Healthy/2", select_only_size=1024)
#display.Plot3D(slices,350)

img = reader.getImageHU(slices[100])
label, mask, masked_image = transform.LungMask(img)

plt.subplot(1,4,1)
plt.imshow(img, cmap='gray')
plt.title("Input", fontsize=10)
plt.axis('off')

plt.subplot(1,4,2)
plt.imshow(label)
plt.title("Clustering", fontsize=10)
plt.axis('off')

plt.subplot(1,4,3)
plt.imshow(mask, cmap='gray')
plt.title("Lung Mask", fontsize=10)
plt.axis('off')

plt.subplot(1,4,4)
plt.imshow(masked_image, cmap='gray')
plt.title("Masked Image", fontsize=10)
plt.axis('off')

plt.show()
