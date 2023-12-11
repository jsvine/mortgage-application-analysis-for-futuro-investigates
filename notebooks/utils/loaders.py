import pathlib

import polars as pl


def load_lenders():
    return pl.read_csv("../data/processed/institutions.csv").with_columns(
        pl.when(
            pl.col("lender_agency").eq(5)
            |
            # Case-insensitive, and skipping entries, such as
            # "Credit Union Lending Source, LLC", that begin with the phrase.
            pl.col("lender_name").str.contains(r"(?i)^.+credit +union")
        )
        .then(pl.lit("cu"))
        .when(pl.col("other_lender_code").eq(3))
        .then(pl.lit("ind"))
        .otherwise(pl.lit("bank_or_other"))
        .alias("lender_type")
    )


def load_county_meta():
    return pl.read_csv("../data/manual/county-names.csv").select(
        pl.col("county_code").cast(str), "county_name"
    )


def get_type(type_str):
    if type_str == "str":
        return str
    else:
        return getattr(pl, type_str)


def load_hmda():
    paths = sorted(
        pathlib.Path("../data/processed/mortgage-records/filtered/").glob("*.csv")
    )

    column_types_df = pl.read_csv("../data/manual/column-types.csv")
    column_types = dict(
        zip(column_types_df["name"], column_types_df["type"].map_elements(get_type))
    )

    def load_csv(path):
        return pl.read_csv(path, dtypes=column_types)

    return pl.concat(map(load_csv, paths))
