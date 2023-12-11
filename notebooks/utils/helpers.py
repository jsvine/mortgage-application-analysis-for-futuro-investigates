import io
import os
import re

import polars as pl
import pyperclip
import statsmodels.api as sm


# Set NOTEBOOK_CLIPBOARD=1 to use this functionality.
# Otherwise, a no-op.
def clip(obj):
    if not int(os.environ.get("NOTEBOOK_CLIPBOARD", 0)):
        return obj
    x = io.BytesIO()
    if isinstance(obj, pl.DataFrame):
        obj.write_csv(x, separator="\t")
    else:
        x.write(str(obj).encode("utf-8"))
    x.seek(0)
    pyperclip.copy(x.read().decode("utf-8"))
    return obj


def make_logger(log_path, clear=True, width=100):
    if clear:
        with open(log_path, "w"):
            pass

    def log(obj, description):
        print(description + ":")
        clip(obj)

        if isinstance(obj, sm.iolib.summary.Summary):

            def replace_chars(match):
                return match.group(1) + "*" * len(match.group(2)) + "  "

            to_write = re.sub(
                r"(\n(?:Time|Date):\s+)([^\s]+.*?)  ",
                replace_chars,
                obj.as_text(),
            )
        else:
            to_write = obj

        with open(log_path, "a") as f:
            with pl.Config(tbl_rows=-1, tbl_cols=-1, tbl_width_chars=width):
                f.write(f"{description}:\n\n{to_write}\n\n---\n")
        return obj

    return log


# via https://github.com/pola-rs/polars/issues/10394#issuecomment-1671761323
def shift_columns_left(df: pl.DataFrame, columns: list[str]) -> pl.DataFrame:
    "Reorders the columns in df so that the specified columns appear first."
    return df.select([pl.col(columns), pl.all().exclude(columns)])


def count_with_pct(df, *cols):
    return (
        df.group_by(*cols)
        .count()
        .sort(*cols, nulls_last=True)
        .with_columns(
            (100 * pl.col("count") / pl.col("count").sum()).alias("pct").round(1)
        )
    )
