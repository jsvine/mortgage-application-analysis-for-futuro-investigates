import io
import pathlib
import zipfile

import requests

BASE_URL = "https://s3.amazonaws.com/cfpb-hmda-public/prod/"

SPECS = [
    (2022, "snapshot"),
    (2021, "one-year"),
    (2020, "one-year"),
    (2019, "three-year"),
    (2018, "three-year"),
]


def get_url(year: int, kind: str, data: str):
    assert data in ["panel", "lar"]
    assert kind in ["snapshot", "one-year", "three-year"]

    name_part = {
        "snapshot": "",
        "one-year": "one_year_",
        "three-year": "three_year_",
    }[kind]

    path = f"{kind}-data/{year}/{year}_public_{data}_{name_part}csv.zip"

    url = BASE_URL + path

    return url


def fetch_institutions(year: int, kind: str, overwrite=False) -> None:
    dest = pathlib.Path(f"data/raw/institutions/{year}-{kind}.csv")

    if dest.exists() and not overwrite:
        print("↳ Institution data already exists.")
        return
    else:
        print("↳ Fetching institution data ...")

    url = get_url(year, kind, "panel")
    res = requests.get(url, stream=True)

    print("↳ Extracting institution data ...")
    with zipfile.ZipFile(io.BytesIO(res.content)) as z:
        with z.open(z.namelist()[0]) as member:
            with open(dest, "wb") as f:
                f.write(member.read())


def fetch_lar(year: int, kind: str, overwrite=False) -> None:
    dest = pathlib.Path(f"data/raw/mortgage-records/{year}-{kind}.csv")

    if dest.exists() and not overwrite:
        print("↳ LAR already exists.")
        return
    else:
        print("↳ Fetching LAR ...")

    url = get_url(year, kind, "lar")
    res = requests.get(url, stream=True)

    print("↳ Extracting LAR ...")
    with zipfile.ZipFile(io.BytesIO(res.content)) as z:
        assert len(z.namelist()) == 1
        with z.open(z.namelist()[0]) as member:
            with open(dest, "wb") as f:
                f.write(member.read())


def main():
    for spec in SPECS:
        print(*spec)
        fetch_institutions(*spec)
        fetch_lar(*spec)


if __name__ == "__main__":
    main()
