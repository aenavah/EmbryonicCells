import os 
import pandas as pd
import numpy as np
import h5py
import seaborn as sns 
import matplotlib.pyplot as plt


def track_file_dir_list() -> list:
  '''
  create a list of strings of global track file paths
  '''
  track_files: list[str] = [] 
  for file in os.listdir(tracks_folder):
      track_files.append(tracks_folder + str(file))
  return track_files

def print_structure(item, indent=0):
    '''print directory structure for item parameter'''
    if isinstance(item, h5py.File) or isinstance(item, h5py.Group):
        for key in item.keys():
            print("  " * indent + f"- {key}")
            print_structure(item[key], indent + 1)
    elif isinstance(item, h5py.Dataset):
        print("  " * indent + f"- {item.name}")

if __name__ == "__Main__":
  #Parameters: 
  base_folder = "/Users/alexandranava/Desktop/EmbryonicCells/"
  tracks_folder = f"{base_folder}Data/tracks/"
  plots_output_folder = f"{base_folder}Plots/" # where to save plots 
  filename = "dox_cdx2Compiled_trackObj.csv"

  #list of track files
  track_file_paths = track_file_dir_list
  # print a nested directory 
  print_structure(h5py.File(track_file_paths[0], "r"), indent = 1)




