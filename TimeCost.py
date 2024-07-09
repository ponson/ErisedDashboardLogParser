import pandas as pd
import re


df = pd.read_excel("data/timecost.xlsx")
times = df[r'2023 一月份']
tFormat = re.compile(r'(\d+) hr (\d+) min')
hours = 0
mins = 0
for item in times:
    if item != item:
        continue
    r = tFormat.search(item)
    print(f"{r.group(1)}:{r.group(2)}")
    hours += int(r.group(1))
    mins += int(r.group(2))


print(f"Total Time: {hours + (mins // 60)} hr {mins % 60} min")

