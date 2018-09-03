import pydicom as pdc
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import csv

# folder name and image number
dir = 'stage_1_train_images'
img_nr = 91


def get_bb_info(patient_name, bb_info_file_name = 'stage_1_train_labels.csv'):
    rv = []
    with open(bb_info_file_name) as f:
        data = csv.reader(f)
        found = False
        for d in data:
            if d[0] == patient_name:
                found = True
                if d[1] != '':
                    rv.append([float(x) for x in d[1:-1]])
            else:
                if found:
                    # entries for a given patient are contiguous. If it is found then not found, no need to look further
                    return rv
    return rv


# find the file name
all_files = [f for f in os.listdir(dir)]
file_name = all_files[img_nr]

# open the file
ds = pdc.dcmread(dir + '/' + file_name)

# display some of the meta info
print(file_name)
print(ds.Rows)
print(ds.Columns)
print(ds.PixelSpacing)
print(ds.PatientName)
# etc...

# plot the pixel data using matplotlib
fig, ax = plt.subplots(1)
ax.imshow(ds.pixel_array, cmap=plt.cm.bone)

# add bounding boxes if any
for bb in get_bb_info(ds.PatientName):
    rect = patches.Rectangle((bb[0], bb[1]), bb[2], bb[3], linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)

plt.show()