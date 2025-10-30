import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import shapiro, levene, kruskal
from datetime import datetime, timedelta

import yaml

try:
    with open("../../config.yaml", "r") as file:
        config = yaml.safe_load(file)

    df = pd.read_csv(config['data']['clean_data']['full_clean'], sep=";")

except:
    print("Yaml configuration file not found!")