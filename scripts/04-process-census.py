import polars as pl

PREFIX_COUNTIES = "data/raw/census/acs-2021-5y-nj-counties"
PREFIX_TRACTS_2021 = "data/raw/census/acs-2021-5y-nj-tracts"
PREFIX_TRACTS_2019 = "data/raw/census/acs-2019-5y-nj-tracts"


def load_census_income(path):
    return pl.read_csv(
        path,
        skip_rows_after_header=1,
        columns=[
            "GEO_ID",
            "S1903_C03_001E",
        ],
        dtypes={"S1903_C03_001E": str},
        null_values=["-"],
    )


def process_income(df, geo_col):
    return (
        df.rename(
            {
                "S1903_C03_001E": "median_income",
            }
        )
        .with_columns(pl.col("median_income").str.extract(r"(\d+)").cast(int))
        .select(geo_col, "median_income")
    )


def load_census_demog(path):
    return pl.read_csv(
        path,
        skip_rows_after_header=1,
        columns=[
            "GEO_ID",
            "DP05_0001E",
            "DP05_0071E",
            "DP05_0077E",
        ],
        null_values=["-"],
    )


def process_demog(df, geo_col):
    return (
        df.rename(
            {
                "DP05_0001E": "pop_total",
                "DP05_0071E": "pop_hl",
                "DP05_0077E": "pop_white_non_hl",
            }
        )
        .with_columns(
            (pl.col("pop_hl") / pl.col("pop_total")).alias("prop_hl"),
            (pl.col("pop_white_non_hl") / pl.col("pop_total")).alias(
                "prop_white_non_hl"
            ),
        )
        .select(
            geo_col,
            "pop_total",
            "pop_hl",
            "pop_white_non_hl",
            "prop_hl",
            "prop_white_non_hl",
        )
    )


def run_counties():
    income_counties = (
        load_census_income(f"{PREFIX_COUNTIES}-S1903/ACSST5Y2021.S1903-Data.csv")
        .with_columns(pl.col("GEO_ID").str.slice(-5, None).alias("county_code"))
        .pipe(process_income, "county_code")
    )
    return (
        load_census_demog(f"{PREFIX_COUNTIES}-DP05/ACSDP5Y2021.DP05-Data.csv")
        .with_columns(pl.col("GEO_ID").str.slice(-5, None).alias("county_code"))
        .pipe(process_demog, "county_code")
        .join(income_counties, on="county_code")
    )


def run_tracts():
    income_tracts = (
        pl.concat(
            [
                load_census_income(
                    f"{PREFIX_TRACTS_2021}-S1903/ACSST5Y2021.S1903-Data.csv"
                ),
                load_census_income(
                    f"{PREFIX_TRACTS_2019}-S1903/ACSST5Y2019.S1903-Data.csv"
                ),
            ]
        )
        .with_columns(pl.col("GEO_ID").str.slice(-11, None).alias("census_tract"))
        .unique(["census_tract"], keep="first", maintain_order=True)
        .pipe(process_income, "census_tract")
    )

    return (
        pl.concat(
            [
                load_census_demog(
                    f"{PREFIX_TRACTS_2021}-DP05/ACSDP5Y2021.DP05-Data.csv"
                ),
                load_census_demog(
                    f"{PREFIX_TRACTS_2019}-DP05/ACSDP5Y2019.DP05-Data.csv"
                ),
            ]
        )
        .with_columns(pl.col("GEO_ID").str.slice(-11, None).alias("census_tract"))
        .unique(["census_tract"], keep="first", maintain_order=True)
        .pipe(process_demog, "census_tract")
        .join(income_tracts, on="census_tract")
    )


def main():
    run_counties().write_csv("data/processed/census/county-demographics.csv")
    run_tracts().write_csv("data/processed/census/tract-demographics.csv")


if __name__ == "__main__":
    main()
