# Leave it empty. This is just a special file that tells pip that your main module is in this folder. 
# No need to add anything here. Feel free to delete this line when you make your own package.

#from anyt import EC_Data
"""_summary_
Module for reading binary TDMS files produced by EC4 View\n

ec_data is used to load in the raw files. 

"""
import os
#__path__ = [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'contents')]
__all__ = ["EC_Data","EC_Datas", "ec_data","CV_Data","CV_Datas","save_key_values", "AutoClaveSynthesis","Quantity_Value_Unit"]


from .ec_data import EC_Data 
from .ec_datas import EC_Datas 
from .cv_data import CV_Data
from .cv_datas import CV_Datas 
from .autoclave_synthesis import * 
from .util import Quantity_Value_Unit 
from .util import * 
#from ..project.util_paths import Project_Paths 
from .util_graph import * 
from ..file.key_values_to_file import save_key_values



#Import the submodules
#from . import ec_data