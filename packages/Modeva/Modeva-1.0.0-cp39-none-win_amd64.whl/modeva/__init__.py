import warnings
warnings.filterwarnings("ignore")

from .data.local_dataset import LocalDataSet as DataSet
from .models.local_model_zoo import LocalModelZoo as ModelZoo
from .factsheet.local_factsheet import LocalFactSheet as FactSheet

import sys
import logging
logging.disable(sys.maxsize)

__all__ = ["DataSet", "ModelZoo", "FactSheet"]

__version__ = '1.0.0'
__date__ = "2024.06"
__author__ = 'Modeva Dev Team'
