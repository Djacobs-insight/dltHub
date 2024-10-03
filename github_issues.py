import dlt
from dlt.sources.helpers import requests

# Specify the URL of the API endpoint
url = "https://api.github.com/repos/dlt-hub/dlt/issues"
# Make a request and check if it was successful
response = requests.get(url)
response.raise_for_status()

pipeline = dlt.pipeline(
    pipeline_name='github_issues',
    destination='duckdb',
    dataset_name='github_data',
)
# The response contains a list of issues
load_info = pipeline.run(
    response.json(),
    table_name="issues",
    write_disposition="replace"  # <-- Add this line
)
print(load_info)
