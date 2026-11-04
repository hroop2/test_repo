#!/usr/bin/env python3
"""A tiny pandas example: build a table, then summarise it.

Setup:  pip install -r requirements.txt
Run:    python3 pandas_example.py
"""
import pandas as pd

# A small table of packages we pulled through Artifactory
packages = pd.DataFrame({
    "group":   ["junit", "org.apache.commons"],
    "name":    ["junit", "commons-lang3"],
    "version": ["4.13.2", "3.14.0"],
    "size_kb": [375, 642],
})

print("All packages:")
print(packages)

print(f"\nTotal size: {packages['size_kb'].sum()} KB")
print(f"Largest:    {packages.loc[packages['size_kb'].idxmax(), 'name']}")
