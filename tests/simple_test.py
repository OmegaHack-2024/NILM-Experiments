import pandas as pd
from nilmtk import DataSet
from nilmtk.utils import convert_yaml_to_hdf5
from nilmtk.disaggregate import CombinatorialOptimization

# Step 1: Load your CSV data
data = pd.read_csv('app/datasets/consumo_casa.csv')

# Assuming 'data' has columns for different appliances already separated, and a time column
# You will need to convert this data into a format NILMTK can use. This often involves creating an HDF5 file.
# For now, let's pretend we've already converted the data.

# Step 2: Load the dataset using NILMTK
dataset = DataSet('path_to_your_hdf5_file.h5')  # Replace with your HDF5 path
elec = dataset.buildings[1].elec  # Assume building 1

# Step 3: Choose a disaggregation algorithm
model = CombinatorialOptimization()
model.train(elec)

# Step 4: Disaggregate the data
disaggregated_output = model.disaggregate(elec.mains())

# Save output or process it further
disaggregated_output.plot()
