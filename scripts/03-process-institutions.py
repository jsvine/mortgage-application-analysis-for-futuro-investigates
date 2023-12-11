import pathlib

import polars as pl


def load_csv(path: pathlib.Path) -> pl.DataFrame:
    df = pl.read_csv(path, infer_schema_length=0)
    renames = {"upper": "lei"} if "upper" in df.columns else {}
    return df.rename(renames)


def main() -> None:
    paths = sorted(pathlib.Path("data/raw/institutions/").glob("*.csv"))

    df = (
        pl.concat(map(load_csv, paths))
        .sort("activity_year")
        .unique(subset=["lei"], keep="last", maintain_order=True)
        .select(
            "lei",
            pl.col("respondent_name").alias("lender_name"),
            pl.col("parent_name").alias("lender_parent"),
            pl.col("topholder_name").alias("lender_topholder"),
            pl.col("agency_code").alias("lender_agency"),
            pl.col("other_lender_code").alias("other_lender_code"),
            pl.col("respondent_state").alias("lender_state"),
            pl.col("assets").alias("lender_assets"),
            pl.col("activity_year").alias("lender_year_max"),
        )
    )

    df.write_csv("data/processed/institutions.csv")


if __name__ == "__main__":
    main()
