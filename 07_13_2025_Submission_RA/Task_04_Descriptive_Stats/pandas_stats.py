import pandas as pd
import time
from IPython.display import display

def pandas_stats_py(ds_path_list: list[str]):
  start_time = time.time()
  print("Statistics By Dataset level started")
  for csv_path in ds_path_list:
    df = pd.read_csv(csv_path)
    display(csv_path.split('/')[-1][0:-4])
    display(df.describe(include='all').T)
    print(" ")
    print(" ")

    if "currency" in df.columns:
      print("Statistics For FB Ads Dataset at currency level started")
      df = df.groupby("currency")
      for group_name, group_df in df:
        print(group_name)
        display(group_df.describe(include='all').T)
        print(" ")
        print(" ")
      print("Statistics For FB Ads Dataset at currency level Completed")

    elif "Page Category" in df.columns:
      print("Statistics For FB posts Dataset at Page Category level started")
      df = df.groupby("Page Category")
      for group_name, group_df in df:
        print(group_name)
        display(group_df.describe(include='all').T)
        print(" ")
        print(" ")
      print("Statistics For FB posts Dataset at Page Category level Completed")

    else:
      print("Statistics For TW posts Dataset at source level started")
      df = df.groupby("source")
      for group_name, group_df in df:
        print(group_name)
        display(group_df.describe(include='all').T)
        print(" ")
        print(" ")
      print("Statistics For TW posts Dataset at source level Completed")

  print("Statistics By Dataset level started")
  end_time = time.time()
  print("Time Taken in Seconds: ", end_time - start_time)


if __name__ == "__main__":
    ds_path_list = ['/content/drive/MyDrive/Research Analyst/2024_fb_ads_president_scored_anon.csv','/content/drive/MyDrive/Research Analyst/2024_fb_posts_president_scored_anon.csv','/content/drive/MyDrive/Research Analyst/2024_tw_posts_president_scored_anon.csv']
    pandas_stats_py(ds_path_list)

