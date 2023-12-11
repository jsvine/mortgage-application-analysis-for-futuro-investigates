import pathlib

import polars as pl


def load_lar_csv(path: pathlib.Path, lazy: bool = False) -> pl.DataFrame:
    method = pl.scan_csv if lazy else pl.read_csv
    return method(
        path,
        null_values=[
            "NA",
            "Na",
            "nA",
            "na",
            "N/AN/",
            "Exempt",
        ],
        dtypes={"total_units": str},
    )
