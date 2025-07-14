import csv, math, statistics as st, time
from collections import Counter, defaultdict
from pathlib import Path
from typing import List, Dict, Any, Tuple


def _summarize_column(raw_values: List[str]) -> Dict[str, Any]:
    values = [v for v in raw_values if v not in {"", "NA", "N/A", None}]
    summary: Dict[str, Any] = {"count": len(values)}

    numeric_vals: List[float] = []
    non_num_found = False
    for v in values:
        try:
            numeric_vals.append(float(v))
        except ValueError:
            non_num_found = True
            break

    if not non_num_found:                      
        if numeric_vals:                       
            summary.update(
                min=min(numeric_vals),
                max=max(numeric_vals),
                mean=sum(numeric_vals) / len(numeric_vals),
                std=st.pstdev(numeric_vals) if len(numeric_vals) > 1 else 0.0,
            )
        return summary

    counts = Counter(values)
    if counts:
        top, freq = counts.most_common(1)[0]
        summary.update(n_unique=len(counts), top=top, top_freq=freq)
    return summary


def _print_table(title: str, stats: Dict[str, Dict[str, Any]]):
    print(f"\n=== {title} ===")
    all_keys = sorted({k for s in stats.values() for k in s})
    header = ["column"] + all_keys

    col_width = {h: len(h) for h in header}
    for col, colstats in stats.items():
        col_width["column"] = max(col_width["column"], len(col))
        for k in all_keys:
            val_len = len(f"{colstats.get(k,'')}")
            col_width[k] = max(col_width[k], val_len)

    def _row(vals):
        return " | ".join(str(v).ljust(col_width[h]) for v, h in zip(vals, header))

    print(_row(header))
    print("-|-".join("-" * col_width[h] for h in header))

    for col, colstats in stats.items():
        row_vals = [col] + [colstats.get(k, "") for k in all_keys]
        print(_row(row_vals))
    print()


def _collect_stats(rows):
    cols = defaultdict(list)
    for r in rows:
        for k, v in r.items():
            cols[k].append(v)
    return {c: _summarize_column(v) for c, v in cols.items()}

def base_stats_py(ds_path_list: List[str]):
    start = time.time()
    print("Statistics By Dataset level started\n")

    for csv_path in ds_path_list:
        with open(csv_path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

        fname = Path(csv_path).stem
        print(f"--- Dataset: {fname} ---")

        _print_table("Overall", _collect_stats(rows))

        def group(keys: Tuple[str, ...], label: str):
            if not rows or any(k not in rows[0] for k in keys):
                return
            print(f"Statistics at {label} level started")
            groups = defaultdict(list)
            for r in rows:
                groups[tuple(r[k] for k in keys)].append(r)
            for gkey, grows in groups.items():
                print("Group:", " • ".join(gkey))
                _print_table("Group Summary", _collect_stats(grows))
            print(f"Statistics at {label} level completed\n")

        if "currency" in rows[0]:
            group(("currency",), "currency")
        elif "Page Category" in rows[0]:
            group(("Page Category",), "Page Category")
        else:
            group(("source",), "source")

    print("Statistics By Dataset level completed")
    print(f"Time taken (seconds): {time.time() - start:.2f}")



if __name__ == "__main__":
    datasets = [
        "/content/drive/MyDrive/Research Analyst/2024_fb_ads_president_scored_anon.csv",
        "/content/drive/MyDrive/Research Analyst/2024_fb_posts_president_scored_anon.csv",
        "/content/drive/MyDrive/Research Analyst/2024_tw_posts_president_scored_anon.csv",
    ]
    base_stats_py(datasets)
