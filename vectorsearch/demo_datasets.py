import h5py
import boto3
import shutil
import numpy as np
import os
print("start")
# Setup S3 client
s3 = boto3.client('s3')
bucket_name = 'finnrobl-24'

# File paths
files = [
    'sift-128-euclidean-nested.hdf5',
    'sift-128-euclidean-with-attr.hdf5',
    'sift-128-euclidean-with-relaxed-filters.hdf5',
    'sift-128-euclidean-with-restrictive-filters.hdf5',
    'sift-128-euclidean.hdf5'
]

files = ['sift-128-euclidean-with-relaxed-filters.hdf5']
# Step 1: Download the files from the S3 bucket
for file_name in files:
    s3.download_file(bucket_name, file_name, file_name)
    print(f"Downloaded {file_name} from S3 bucket {bucket_name}")

# # Step 2: Modify the restrictive dataset
# with h5py.File('sift-128-euclidean-with-restrictive-filters.hdf5', 'r+') as restrictive_file:
#     restrictive_file.copy('neighbors_filter_4', 'neighbors')
#     del restrictive_file['neighbors_filter_4']

# # Step 3: Modify the relaxed dataset
with h5py.File('sift-128-euclidean-with-relaxed-filters.hdf5', 'r+') as relaxed_file:
    print(relaxed_file.keys(), relaxed_file['neighbors_filter_5'], relaxed_file['neighbors_filter_5'][0])
    relaxed_file.copy('neighbors_filter_5', 'neighbors')
    del relaxed_file['neighbors_filter_5']

# Step 4: Copy datasets from sift-128-euclidean-with-attr to both restrictive and relaxed files
with h5py.File('sift-128-euclidean-with-attr.hdf5', 'r') as attr_file:
    datasets = ['attributes', 'test', 'train']
    
    for dataset in datasets:
        print(dataset)
#        with h5py.File('sift-128-euclidean-with-restrictive-filters.hdf5', 'r+') as restrictive_file:
#            attr_file.copy(dataset, restrictive_file)
        with h5py.File('sift-128-euclidean-with-relaxed-filters.hdf5', 'r+') as relaxed_file:
            attr_file.copy(dataset, relaxed_file)

    # attributes = attr_file['attributes'][:]
    # parents = attributes[:, 3].as_type(int)  # Last column
    # color = attributes[:, 0]
    # taste = attributes[:, 1]
    # age = attributes[:, 2].astype(int)

"""    with h5py.File('sift-128-euclidean-nested.hdf5', 'r+') as nested_file:
        nested_attr_data = nested_file['attributes'][:]
        parents = nested_attr_data[:, 3].astype(int)
        nested_file.create_dataset('parents', data=parents)

    # new_attributes_data = np.column_stack((color, taste, age))
    # print(new_attributes_data)
    # with h5py.File('sift-128-euclidean-with-attr.hdf5', 'r+') as attr_file_write:
        # del attr_file_write['attributes']
        # attr_file_write.create_dataset('attributes', data=new_attributes_data)


# Step 5: Rename "neighbour_nested" to 'neighbors' in the nested file
with h5py.File('sift-128-euclidean-nested.hdf5', 'r+') as nested_file:
    nested_file.copy('neighbour_nested', 'neighbors')
    # del nested_file['neighbour_nested']

# Step 6: Copy sift-128-euclidean.hdf5 to /tmp/sift-128-euclidean.hdf5
shutil.copy('sift-128-euclidean.hdf5', '/tmp/sift-128-euclidean.hdf5')

# Step 7: Copy nested to /tmp/data-nested
shutil.copy('sift-128-euclidean-nested.hdf5', '/tmp/data-nested.hdf5')
"""
# Step 8: Copy relaxed to /tmp/filter_relaxed.hdf5
shutil.copy('sift-128-euclidean-with-relaxed-filters.hdf5', '/tmp/filter_relaxed.hdf5')

# Step 9: Copy restrictive to /tmp/filter_restrictive.hdf5
# shutil.copy('sift-128-euclidean-with-restrictive-filters.hdf5', '/tmp/filter_restrictive.hdf5')

print("All operations completed successfully.")
