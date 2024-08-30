# Leave it empty. This is just a special file that tells pip that your main module is in this folder. 
# No need to add anything here. Feel free to delete this line when you make your own package.

#from any import EC_Data

import os
from .data_treatment import *
from .project.util_paths import Project_Paths

#from .ec_data import * 

#__path__ = [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_treatment')]

#print("loading arenz_group_python")
#print(__path__)

__version__ = "0.0.100"

__all__ = ["ec_data","EC_Data","CV_Data","CV_Datas","save_key_values","Project_Paths","AutoClaveSynthesis"]


# public interface

#def rowdata():
#    """Try to apply the pattern at the start of the string, returning
#    a Match object, or None if no match was found."""
#    return Project_Paths().rawdata_path



