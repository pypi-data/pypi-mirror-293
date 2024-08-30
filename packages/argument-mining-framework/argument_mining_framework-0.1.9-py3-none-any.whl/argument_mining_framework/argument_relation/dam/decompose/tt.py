import os
import pandas as pd

# Get the absolute system path
abs_path = os.path.abspath(os.path.dirname(__file__))

# Prepend the absolute path to the file path
file_path = os.path.join(abs_path, "../config/spacy_tag_dep.csv")

# Load the CSV file into a DataFrame
df = pd.read_csv(file_path, encoding="utf-8")

