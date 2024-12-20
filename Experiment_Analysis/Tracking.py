import os 
import pandas as pd
import numpy as np
import h5py
import seaborn as sns 
import matplotlib.pyplot as plt
import imageio.v2 as imageio



def fill_data(df):
  '''
  ===IN PROGRESS===
  finds missing t rows in df and fills with last known data
  '''
  print("generating data...")
  i_max = df["t"].max()
  new_rows = []

  # Process each unique ID
  for idd in df["id"].unique():
      track_df = df[df["id"] == idd]
      i_init = track_df["t"].min()
      
      ts = set(range(i_init, i_max + 1)) - set(track_df["t"])
      
      for t in sorted(ts):
          prev_row = track_df[track_df["t"] == t - 1]
          if not prev_row.empty:
            t_row = {
                "t": t,
                "x": prev_row["x"].values[0],  # Use previous row's "x"
                "y": prev_row["y"].values[0],  # Use previous row's "y"
                "id": idd,
                "id_num": idd.split("r")[0] if "r" in idd else None,
                "region": idd.split("r")[1] if "r" in idd else None,
            }
          new_rows.append(t_row)

  # add generated data
  if new_rows:
      df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)

  # sort
  df.sort_values(by=["id", "t"], inplace=True)
  df.reset_index(drop=True, inplace=True)
  
  return df

  

def remove_incomplete_tracks(df, buffer_frame: int):
   '''removes tracks whos length is less than max time - buffer frame'''
   print(f"parsing through {len(df['id'].unique())} tracks...")
   max_track_length = df["t"].values.max()

   df_return = pd.DataFrame()
   short_tracks_count = 0 
   groups = df.groupby(["id"])
   for id_str, group in groups: 
      if len(group) < max_track_length - buffer_frame: 
        short_tracks_count += 1
        continue
      else: 
         df_return = pd.concat([df_return, group], ignore_index=True)
    
   print(f"removed {short_tracks_count} tracks due to length...")
   print(f"returning {len(df['id'].unique()) - short_tracks_count} tracks...\n")
   return df_return

def add_region_column(df, region_column_name):
  df[region_column_name] = df["id"].str.split("r").str[1]
  return df


def plot_location(df, plot_title: str, region: int, plot_path: str):
  print(f"plotting (x, y)...")

  #color map for scatter plot
  num_tracks = len(df['id'].unique())
  palette = sns.color_palette('pastel', num_tracks)
  color_map = {id_val: color for id_val, color in zip(df["id_num"].unique(), palette)}

  images = []

  df_region =  df[df["region"] == region]
  print(f"plotting {len(df_region['id'].unique())} tracks...")
  max_step = df_region["t"].values.max()
  #plot bounds
  x_min, x_max = df["x"].values.min(), df["x"].values.max()
  y_min, y_max = df["y"].values.min(), df["y"].values.max()


  for i in range(max_step + 1):  
      df_region_i = df_region[df_region["t"] == i]
      if len(df_region_i) == 0:
         continue
      
      #df_region.to_csv(plot_path + ".csv")
      #break

      plt.figure(figsize=(6, 6))
      sns.scatterplot(x="x", y="y", hue = 'id_num', data=df_region_i,  
                      s = 400, 
                      palette = color_map)
      
      plt.grid()
      # LABELING

      plt.xlabel("x", fontsize=18)
      plt.xlim([x_min, x_max])

      plt.ylabel("y", fontsize=18)
      plt.ylim([y_min, y_max])

      #plt.legend(loc = "upper left", title = "id")

      plt.title(rf"{plot_title}$_{{{i}}}$", fontsize=22)
      # SAVE each plot 
      plt.tight_layout()
      plt.savefig("temp_plot.png")  # Temporary save
      images.append(imageio.imread("temp_plot.png"))
      plt.close()  
  

  imageio.mimsave(plot_path, images, fps = 3)
  print(f"plot saved to {plot_path}...")


if __name__ == "__main__":

  #Parameters: 
  base_folder = "/Users/alexandranava/Desktop/EmbryonicCells/EmbryonicCells/Experiment_Analysis/"
  data_folder = f"{base_folder}Experiment_Data/"
  plots_output_folder = f"{base_folder}Plots/" # where to save plots 
  #filename = "dox_gata6Compiled_trackObj.csv"
  filename = "dox_cdx2Compiled_trackObj.csv"
  frame_buffer = 20

  #initialization
  exp_type = filename.replace("Compiled_trackObj.csv", "")
  df = pd.read_csv(data_folder + filename)
  df["region"] = df["id"].str.split("r").str[1]
  df["id_num"] = df["id"].str.split("r").str[0]

  #attempted postprocessing
  #df = remove_incomplete_tracks(df, frame_buffer)
  #df = fill_data(df)

  #plot for every region
  for region in df["region"].unique():
    print(f"\n working on region {region}...")
    plot_location(df, "(x, y)", region, f"{plots_output_folder}xy_{exp_type}_r{region}.gif")
  


