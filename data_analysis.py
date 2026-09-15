import csv

thumb_fsi = 0.0;
index_fsi = 0.0;
middle_fsi = 0.0;
ring_fsi = 0.0;
pinky_fsi = 0.0;
last_row = 0;

with open("EXTENDED_DATA.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)



    for row in reader:
        thumb_fsi += float(row["thumb_fsi"]) - 0.05
        index_fsi += float(row["index_fsi"])
        middle_fsi += float(row["middle_fsi"])
        ring_fsi += float(row["ring_fsi"])
        pinky_fsi += float(row["pinky_fsi"]) - 0.03
        last_row = row

index = int(last_row["index"])
print(f"thumb {thumb_fsi / index}")
print(f"index {index_fsi / index}")
print(f"middle {middle_fsi / index}")
print(f"ring {ring_fsi / index}")
print(f"pinky {pinky_fsi / index}")