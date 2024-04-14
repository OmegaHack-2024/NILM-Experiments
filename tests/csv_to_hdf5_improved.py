import os
import pandas as pd
from nilmtk.datastore import Key
from nilmtk.measurement import LEVEL_NAMES
from nilm_metadata import convert_yaml_to_hdf5
from nilmtk.utils import get_datastore

# Your CSV file
csv_filename = '/mnt/data/consumo_casa.csv'
# HDF5 file to create
hdf_filename = '/mnt/data/consumo_casa.h5'

# Load CSV into a pandas DataFrame
df = pd.read_csv(csv_filename, parse_dates=True, index_col='Fecha')

# Define metadata for the dataset
metadata = {
    'name': 'consumo_casa',
    'elec_meters': {
        0: {'device_model': 'generic', 'site_meter': True},
    },
    'appliances': [],
    'timezone': 'Europe/London', # Replace with your timezone
}

# Process column names to fit into MultiIndex format (if necessary)
df.columns = pd.MultiIndex.from_product(
    [['power'], ['active'], df.columns],
    names=LEVEL_NAMES
)

# Initialize datastore
store = get_datastore(hdf_filename, format='HDF', mode='w')

# Loop over each column (appliance) and create a corresponding meter in metadata
for i, col in enumerate(df.columns):
    if col[2] == 'Medidor [W]':
        key = Key(building=1, meter=0)
    else:
        key = Key(building=1, meter=i+1)
        metadata['elec_meters'][i+1] = {'device_model': 'generic', 'submeter_of': 0}
        metadata['appliances'].append({'type': col[2], 'instance': 1, 'meters': [i+1]})
    
    # Save time series data to the HDF5 store
    store.put(str(key), df[[col]])

# Save metadata to the HDF5 store
store.save_metadata(metadata)
store.close()

# Convert YAML metadata to HDF5 (if using nilm_metadata, uncomment the line below)
# convert_yaml_to_hdf5('/mnt/data/metadata', hdf_filename)
