import pandas as pd

import morph
from morph import MorphGlobalContext


@morph.config(
    name="example_python_cell",
    description="Example Python cell",
    output_paths=["_public/{name}/{now()}{ext()}", "_private/{name}/{now()}{ext()}"],
    output_type="dataframe",
)
@morph.load_data("example_sql_cell")
def main(context: MorphGlobalContext) -> pd.DataFrame:
    # Load data from the previous cell
    sql_result_df = context.data["example_sql_cell"]
    return sql_result_df
