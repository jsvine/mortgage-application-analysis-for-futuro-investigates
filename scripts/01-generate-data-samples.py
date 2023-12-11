import pathlib

import polars as pl
from utils.load import load_lar_csv


def process_file(path: pathlib.Path) -> None:
    df = load_lar_csv(path)
    stats = pl.DataFrame(
        (
            {
                "column_ix": ix,
                "column_name": name,
            }
            for ix, name in enumerate(df.columns)
        )
    )

    stats.write_csv("data/processed/mortgage-records/columns/" + path.name)

    sample = df.sample(10000)
    sample.write_csv("data/processed/mortgage-records/raw-samples/" + path.name)


def main() -> None:
    paths = pathlib.Path("data/raw/mortgage-records/").glob("*.csv")
    for path in sorted(paths):
        print(path)
        process_file(path)


if __name__ == "__main__":
    main()
