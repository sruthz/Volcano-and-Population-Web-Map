import pandas
import json

df = pandas.read_json("states.json")
df.to_csv("states.csv")