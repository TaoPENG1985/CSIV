from cmath import nan
from random import random
from tarfile import NUL
from types import resolve_bases
import numpy as np
from pyparsing import alphas
from sklearn import datasets
from sklearn.metrics import mean_squared_error
import math 
from scipy import stats
import os
import time
import pandas as pd
import matplotlib.pyplot as plt


MYmean = [0.01, 0.01 ,0.01, 0.01, 0.01, 0, 0, 0.01,0.01,0.01 ]
MYstd = [7.6,7.85,7.90,7.95,8.6,0.60,0.62,0.64,0.66,0.67]

for i in range(0,10):
    conf_interal_SMV = stats.norm.interval(0.95, loc= MYmean[i], scale = MYstd[i])
    print(conf_interal_SMV)
