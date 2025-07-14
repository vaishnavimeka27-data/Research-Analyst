## 1  Prerequisites

We need packages to run the code.
Install everything at once:

```bash
python -m pip install pandas polars ipython
```


## 2 Datasets
Make sure the datasets are there inside of a folder.

## 3 Running the scripts

#### 3-a Pure-Python version
Make sure your dataset paths in the order in the line 106 - 110 for file pure_python_stats.py

Order: 
```python
datasets_paths = [
        "/content/drive/MyDrive/Research Analyst/2024_fb_ads_president_scored_anon.csv",
        "/content/drive/MyDrive/Research Analyst/2024_fb_posts_president_scored_anon.csv",
        "/content/drive/MyDrive/Research Analyst/2024_tw_posts_president_scored_anon.csv",
    ]
```

Next in CLI you can directly run the Command:  python stats_base_py.py

#### 3-b Pandas version
Make sure your dataset paths in the order in the line 51 for file pandas_stats.py

Order: 
```python
ds_path_list = ['/content/drive/MyDrive/Research Analyst/2024_fb_ads_president_scored_anon.csv','/content/drive/MyDrive/Research Analyst/2024_fb_posts_president_scored_anon.csv','/content/drive/MyDrive/Research Analyst/2024_tw_posts_president_scored_anon.csv']
```

Next in CLI you can directly run the Command:  python pandas_stats.py

#### 3-c Polars version
Make sure your dataset paths in the order in the line 45 for file polars_stats.py

Order: 
```python
ds_path_list = ['/content/drive/MyDrive/Research Analyst/2024_fb_ads_president_scored_anon.csv','/content/drive/MyDrive/Research Analyst/2024_fb_posts_president_scored_anon.csv','/content/drive/MyDrive/Research Analyst/2024_tw_posts_president_scored_anon.csv']
```

Next in CLI you can directly run the Command:  python polars_stats.py


# Short summary of findings 
1. I find that Polars execution is the faster than Pandas & Base Python. 

# Performance Benchmarks

| Script | Stack | File | Runtime* |
|--------|-------|------|----------|
| **Polars** | `polars` (Rust engine, multithreaded) | `stats_polars.py` | **≈ 3.99 s** |
| Pandas | `pandas` | `stats_pandas.py` | ≈ 18.44 s |
| Pure Python | Standard-library only | `stats_base_py.py` | ≈ 35.34 s |

\* Timings captured on the same google collab machine, single run, using the datasets in my G-Drive Folder
`/content/drive/MyDrive/Research Analyst/`.

---

## Findings

1. **Polars is Fastest**  
   - ~4.6 × faster than pandas  
   - ~9 × faster than the pure-Python implementation  
   - When I looked up online, the speeds come from a Rust backend, vectorised execution, and automatic
     multi-threading.

2. **Pandas offers a good middle ground in this comparison**  
   - When I looked up lonline, I got to know that it uses Pure C/NumPy core, but single-threaded by default and hence pays a
     Python cost when we iterate over groups.  

3. **Pure Python slow**  
   - When I looked up why it is slow, here Every conversion and aggregation runs inside the CPython interpreter.

4. Getting Pandas and Polars to match was easy—`describe()` did most of the work.
The plain-Python version was the pain point; I had to write my own `describe`.
Biggest fixes: strip out blank values, detect numeric vs. text, and avoid `min([])` crashes.
After those tweaks all three scripts finally show the exact same counts and averages.
So yes, matching results was a bit of work—but only because pure Python needed extra handling.
