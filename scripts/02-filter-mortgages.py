import pathlib

import polars as pl
from utils.load import load_lar_csv


def filter_and_log(df, expression, notice):
    count_before = len(df)
    filtered = df.filter(expression)
    count_after = len(filtered)
    change = (count_after / count_before) - 1
    print(notice)
    print(f"↳ {count_before:,d} → {count_after:,d} ({100*change:.1f}%)")
    return filtered


def filter_mortgages(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df
        # Note: State codes are standardized in the data,
        #   there are no casing/etc. variations
        .pipe(
            filter_and_log,
            (pl.col("state_code") == "NJ"),
            "Limit to New Jersey",
        )
        # NOT `Purchased loan`
        .pipe(
            filter_and_log,
            (pl.col("action_taken") != 6),
            "Excluding 'Purchased loan' actions",
        )
        # NOT other non-determined applications
        # I.e., withdrawn, incomplete, preapproval
        .pipe(
            filter_and_log,
            (pl.col("action_taken") < 4),
            "Excluding withdrawn, incomplete applications and preapproval decisions",
        )
        # Only for `Home purchase`
        .pipe(
            filter_and_log,
            (pl.col("loan_purpose") == 1),
            "Home purchase only",
        )
        # Only `Conventional (not insured or guaranteed by FHA, VA, RHS, or FSA)`
        #   OR `Federal Housing Administration insured (FHA)
        # Note: We'll want to analyze these separately later.
        .pipe(
            filter_and_log,
            pl.col("loan_type").is_in([1, 2]),
            "Conventional/FHA only",
        )
        # Only `Secured by a first lien`
        .pipe(
            filter_and_log,
            (pl.col("lien_status") == 1),
            "Secured by a first lien only",
        )
        # NOT a reverse mortgage
        .pipe(
            filter_and_log,
            (pl.col("reverse_mortgage") == 2),
            "Not a reverse mortgage",
        )
        # NOT an open-end line of credit
        .pipe(
            filter_and_log,
            (pl.col("open_end_line_of_credit") == 2),
            "Not an open-end line of credit",
        )
        # Only 1-4 units
        # Note: This is a string, because larger values are ranges, e.g., "5-24"
        .pipe(
            filter_and_log,
            pl.col("total_units").is_in(["1", "2", "3", "4"]),
            "1-4 unit properties only",
        )
        # NOT `Primarily for a business or commercial purpose`
        .pipe(
            filter_and_log,
            (pl.col("business_or_commercial_purpose") == 2),
            "Not loans primarily for business/commercial purpose",
        )
        # Only `Site-built`
        .pipe(
            filter_and_log,
            (pl.col("construction_method") == 1),
            "Site-built only",
        )
        # Only `Principal residence`
        .pipe(
            filter_and_log, (pl.col("occupancy_type") == 1), "Principal residence only"
        )
    )


def filter_from_path(path: pathlib.Path) -> None:
    print(path.name)

    dest = pathlib.Path("data/processed/mortgage-records/filtered/" + path.name)

    if dest.exists():
        print("▹ Already filtered")
    else:
        df = load_lar_csv(path)
        filtered = filter_mortgages(df)
        filtered.write_csv(dest)


def main() -> None:
    paths = pathlib.Path("data/raw/mortgage-records/").glob("*.csv")
    for path in sorted(paths):
        filter_from_path(path)


if __name__ == "__main__":
    main()
