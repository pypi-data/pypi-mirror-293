{{
	config(
		name="example_sql_cell",
		description="Example SQL cell",
		output_paths=["_public/{name}/{now()}{ext()}", "_private/{name}/{now()}{ext()}"],
        output_type="dataframe",
	)
}}

select 1 as test;
