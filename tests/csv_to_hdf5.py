import pandas as pd
from nilmtk.utils import save_yaml_to_datastore
from nilmtk.datastore import Key
from nilmtk.measurement import LEVEL_NAMES
from nilm_metadata import convert_yaml_to_hdf5

# Step 1: Load CSV into a pandas DataFrame
df = pd.read_csv('app/datasets/consumo_casa.csv', parse_dates=True, index_col='Fecha')

# Step 2: Prepare the output HDF5 file path
output_filename = 'app/datasets/consumo_casa.h5'

# Step 3: Create metadata
# This is an example of metadata. You should tailor this to fit your dataset.
metadata = {
    'name': 'consumo_casa',
    'meter_devices': {
        'mains': {'model': 'iAWE', 'sample_period': 60},
        'submeters': {'model': 'iAWE', 'sample_period': 60}
    },
    'appliances': [
        {'type': 'fridge', 'instance': 1},
        {'type': 'washing machine', 'instance': 1},
        {'type': 'dish washer', 'instance': 1},
        # Add all other appliances
    ],
    'timezone': 'Europe/London', # Change as per your dataset
}

# Step 4: Prepare DataFrame for saving to HDF5
df.columns = pd.MultiIndex.from_tuples([("power", "active", col) if col != 'Medidor [W]' else ("power", "apparent", "mains") for col in df.columns], names=LEVEL_NAMES)

# Step 5: Save to HDF5
save_yaml_to_datastore(metadata, df, output_filename, format='HDF')

# Now you have an HDF5 file that can be loaded by NILMTK
dataset = DataSet(output_filename)
elec = dataset.buildings[1].elec
elec.plot()
