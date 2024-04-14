import pandas as pd
from nilmtk import DataSet
from nilmtk.utils import save_yaml_to_datastore
from nilmtk.measurement import LEVEL_NAMES

def csv_to_hdf5(csv_file, hdf5_file):
    # Load your CSV data
    data = pd.read_csv(csv_file, index_col='Fecha', parse_dates=True)
    # 'Fecha' should be your datetime column, ensure this column is in datetime format

    # Define the metadata for NILMTK compatibility
    metadata = {
        'appliances': [{'type': 'Refrigerator', 'instance': 1},
                       {'type': 'Clothes Washer', 'instance': 1},
                       {'type': 'Clothes Iron', 'instance': 1},
                       {'type': 'Computer', 'instance': 1},
                       {'type': 'Oven', 'instance': 1},
                       {'type': 'Play', 'instance': 1},
                       {'type': 'TV', 'instance': 1},
                       {'type': 'Sound System', 'instance': 1}],
        'name': 'home',
        'timezone': 'Europe/London',  # Change this to your local timezone
        'meter_devices': {
            'my_meter': {
                'model': 'NILMTK Custom',
                'sample_period': 60  # This assumes data is sampled every minute
            }
        }
    }

    # Reformat the DataFrame to fit NILMTK's expected MultiIndex format
    data.columns = pd.MultiIndex.from_product([['power'], ['active'], data.columns],
                                              names=LEVEL_NAMES)
    
    # Save to HDF5 using NILMTK's utility function
    save_yaml_to_datastore(metadata, data, hdf5_file)

# Convert your CSV to HDF5
csv_file = '/mnt/data/consumo_casa.csv'
hdf5_file = '/mnt/data/consumo_casa.h5'
csv_to_hdf5(csv_file, hdf5_file)

# Load the dataset using NILMTK
dataset = DataSet(hdf5_file)
print("Dataset loaded:", dataset.buildings)
