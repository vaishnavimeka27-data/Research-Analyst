import polars as pl          
import time
from IPython.display import display

def polars_stats(ds_path_list: list[str]):
    def print_group_stats(df: pl.DataFrame, key: str):
        for val, gdf in df.partition_by(key, as_dict=True).items():
            print(val)
            display(gdf.describe())
            print()

    start = time.time()
    print("Statistics By Dataset level started")

    for csv_path in ds_path_list:
        df = pl.read_csv(csv_path)

        fname = csv_path.split("/")[-1][:-4]
        display(fname)                  
        
        display(df.describe())

        if "currency" in df.columns:
            print("Statistics For FB Ads Dataset at currency level started")
            print_group_stats(df, "currency")
            print("Statistics For FB Ads Dataset at currency level Completed")

        elif "Page Category" in df.columns:
            print("Statistics For FB posts Dataset at Page Category level started")
            print_group_stats(df, "Page Category")
            print("Statistics For FB posts Dataset at Page Category level Completed")

        else:
            print("Statistics For TW posts Dataset at source level started")
            print_group_stats(df, "source")
            print("Statistics For TW posts Dataset at source level Completed")

        print()

    print("Statistics By Dataset level Completed")
    print(f"Time Taken in Seconds: {time.time() - start:.2f}")


if __name__ == "__main__":
    ds_path_list = ['/content/drive/MyDrive/Research Analyst/2024_fb_ads_president_scored_anon.csv','/content/drive/MyDrive/Research Analyst/2024_fb_posts_president_scored_anon.csv','/content/drive/MyDrive/Research Analyst/2024_tw_posts_president_scored_anon.csv']
    polars_stats(ds_path_list)