# 2020_10_02

Most recent data pulled from [Trellis](https://trellis.sinopia.io/repository/washington). Has been run through `fix_URIs.py` and `fix_copyright_dates.py`.

# list_namespaces.py

Python script that takes in a directory of RDA data and outputs a text file listing all namespaces used throughout the RDA data and all properties used belonging to those namespaces. The script takes a file path to the RDA data as an argument. Currently, this script will only work with XML files.

Example:
`$ python3.6 list_namespaces.py 2020_8_24`

# namespaces.txt

Output of `list_namespaces.py`.
