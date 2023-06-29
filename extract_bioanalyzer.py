""" This script will take a list of bioanalyzer xml files 
    and extract some parameters of interest from the region Information 
	from a bioanalyzer .xml output file 
"""


import argparse
import pandas as pd
from bs4 import BeautifulSoup
import pdb


parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+')
parser.add_argument('-o')
args = parser.parse_args()

d={}

to_get = ["RegionConcentration", "PercentTotal", "StartBasePair", "EndBasePair", "RegionConcentration", "RegionMolarity"]

for file in args.files:
	with(open(file) as test):
		data = BeautifulSoup(test, "xml")
		for samples in data.find_all("Sample"):	
			
			sample_name = samples.find("Name").string
	
			if samples.find("Category").text != "Ladder":
				sample_data =  samples.find("DAResultStructures").find("DARSmearAnalysis").find("RegionsMolecularResults")
				sample_vals = [sample_data.find(item).string for item in to_get]

				d[sample_name] = sample_vals
				
out = pd.DataFrame.from_dict(d, orient='index')
out.columns = to_get
out.index.name = "Sample_ID"


out.to_csv(args.o)
