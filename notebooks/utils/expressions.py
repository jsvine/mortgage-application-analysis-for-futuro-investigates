import polars as pl


def make_expr_ethn_simple(ethn_variable: str, alias: str) -> pl.Expr:
    return pl.col(ethn_variable).replace({11: 1, 12: 1, 13: 1, 14: 1}).alias(alias)


EXPR_ETHN_SIMPLE = make_expr_ethn_simple("applicant_ethnicity_1", "ethn_simple")


def make_expr_race_simple(race_variable: str, alias: str) -> pl.Expr:
    return (
        # AIAN
        pl.when(pl.col(race_variable).eq(1))
        .then(pl.lit("native"))
        # NHPI
        .when(pl.col(race_variable).cast(str).str.slice(0, 1).eq("4"))
        .then(pl.lit("pacific_islander"))
        # Asian
        .when(pl.col(race_variable).cast(str).str.slice(0, 1).eq("2"))
        .then(pl.lit("asian"))
        # Black
        .when(pl.col(race_variable).eq(3))
        .then(pl.lit("black"))
        # White
        .when(pl.col(race_variable).eq(5))
        .then(pl.lit("white"))
        # Missing
        .when(pl.col(race_variable).gt(5))
        .then(pl.lit("missing"))
        .when(pl.col(race_variable).is_null())
        .then(pl.lit("missing"))
        .otherwise(pl.lit("UNPROCESSED"))
        .alias(alias)
    )


EXPR_RACE_SIMPLE = make_expr_race_simple("applicant_race_1", "race_simple")


def make_expr_race_ethn(race_var: str, ethn_var: str, alias: str) -> pl.Expr:
    # When the applicant's ethnicity is Hispanic/Latino,
    # set `race_ethn` to Hispanic/Latino (`hl`).
    # Otherwise, set `race_ethn` to the applicant's race
    return (
        pl.when(pl.col(ethn_var).eq(1))
        .then(pl.lit("hl"))
        .otherwise(pl.col(race_var))
        .alias(alias)
    )


EXPR_RACE_ETHN = make_expr_race_ethn("race_simple", "ethn_simple", "race_ethn")

EXPR_IS_CREDIT_DENIAL = pl.any_horizontal(
    pl.col("denial_reason_1").is_in([3, 7]).fill_null(False),
    pl.col("denial_reason_2").is_in([3, 7]).fill_null(False),
    pl.col("denial_reason_3").is_in([3, 7]).fill_null(False),
    pl.col("denial_reason_4").is_in([3, 7]).fill_null(False),
)
