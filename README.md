# python-arkiver
Export.py can be used to export arbitrary entities from Arkiver into a pandas Dataframe and then saved in CSV file format. 
### Requirements
---
* Running Arkiver instance
* export.py requires pandas. To install pandas you can use pip with the following command.
> pip install pandas

### Usage
---
Ensure that your Arkiver instance is up and running. 
> python export.py {entity} {output} {optional: address} {optional: limit} {optional: skip}

entity: one object in the Arkive you wish to export. Example: Balance

output file: this file will be used to output the CSV data from Arkiver. example: output.csv

endpoint: Full web address of the graphql instance you wish to connect to. example: http://0.0.0.0:4000/graphql

limit: used to determine how many entities to request from the database per request. example: 1000

skip: used to determine how many entries will be excluded from the final output example: 100

