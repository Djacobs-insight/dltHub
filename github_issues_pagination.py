import dlt
from dlt.sources.helpers.rest_client import paginate

@dlt.resource(
    table_name="issues",
    write_disposition="merge",
    primary_key="id",
)
def get_issues(
    updated_at=dlt.sources.incremental("updated_at", initial_value="1970-01-01T00:00:00Z")
):
    for page in paginate(
        "https://api.github.com/repos/dlt-hub/dlt/issues",
        params={
            "since": updated_at.last_value,
            "per_page": 100,
            "sort": "updated",
            "direction": "desc",
            "state": "open",
        },
    ):
        yield page

pipeline = dlt.pipeline(
    pipeline_name="github_issues_merge",
    destination="duckdb",
    dataset_name="github_data_merge",
)
load_info = pipeline.run(get_issues)
row_counts = pipeline.last_trace.last_normalize_info

print(row_counts)
print("------")
print(load_info)