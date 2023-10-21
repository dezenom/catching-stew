import pickle
import os
from typing import Any

class save_loadsystem():
    def __init__(self,extension,folder):
        self.extension = extension
        self.folder = folder
    def save_data(self, data, name):
        data_file = open(self.folder+"/"+name+self.extension, "wb")
        pickle.dump(data, data_file)

    def load_data(self, name):
        data_file = open(self.folder+"/"+name+self.extension, "rb")
        data = pickle.load(data_file)
        return data
    
    def check_file(self,file_name):
        return os.path.exists(self.folder+"/"+file_name+self.extension)
    
    def save_all_data(self,data_list,filenames_list):
        for index, data in enumerate(data_list):
            self.save_data(data,filenames_list[index])
    
    def load_all_data(self,files_to_load,defaults):
        variables = []
        for index, file in enumerate(files_to_load):
            if self.check_file(file):
                variables.append(self.load_data(file))
            else:
                variables.append(defaults[index])

        if len(variables) > 1:
            return tuple(variables)
        else:
            return variables[0]