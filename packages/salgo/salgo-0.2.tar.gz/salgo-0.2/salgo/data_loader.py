import os
import pandas as pd
from .trainer import train

def load_data():
    current_dir = os.path.dirname(__file__)
    data = pd.read_csv(os.path.join(current_dir, 'data.csv'))
    print(data, "\n")
    train(data)