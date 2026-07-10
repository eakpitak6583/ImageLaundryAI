from parsers.part_parser import extract_parts

sample = """
Item
Part No.
Qty.

1
A0-A026-021
1
Steam Coil 1/2"

2
A0-A004-013
1
Y-Bearing

3
A0-E027-100
1
RTD Sensor

4
A0-E008-126
1
Motor 25HP. /2P. /380V
"""

parts = extract_parts(sample)

for p in parts:

    print(p)