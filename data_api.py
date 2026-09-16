
import xarray as xr
from pyproj import Transformer
from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError, URLError


def get_sea_ice_at_location(file_path, latitude, longitude):
    """
    Get real sea-ice concentration from NOAA/NSIDC NetCDF data
    for a given latitude and longitude.
    """

    ds = xr.open_dataset(file_path)

    transformer = Transformer.from_crs(
        "EPSG:4326",
        "EPSG:3412",
        always_xy=True
    )

    x, y = transformer.transform(longitude, latitude)

    value = ds["cdr_seaice_conc"].sel(
        x=x,
        y=y,
        method="nearest"
    ).values[0]

    if value != value:
        return None

    return float(value) * 100


def download_sea_ice_file(data_date, output_dir="data"):
    """
    Download an official NOAA/NSIDC Antarctic daily sea-ice NetCDF file.
    """

    filename = f"sic_pss25_{data_date:%Y%m%d}_am2_v06r00.nc"

    url = (
        "https://noaadata.apps.nsidc.org/NOAA/G02202_V6/"
        f"south/daily/{data_date.year}/{filename}"
    )

    output_path = Path(output_dir) / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with urlopen(url) as response, open(output_path, "wb") as file:
            file.write(response.read())

    except HTTPError as error:
        if error.code == 404:
            raise RuntimeError(
                f"NOAA sea-ice file is not available for "
                f"{data_date:%Y-%m-%d}"
            ) from error

        raise RuntimeError(
            f"NOAA download failed with HTTP error {error.code}"
        ) from error

    except URLError as error:
        raise RuntimeError(
            "Unable to connect to the NOAA data server."
        ) from error

    return str(output_path)


def get_sea_ice_for_date(data_date, latitude, longitude, output_dir="data"):
    """
    Download NOAA sea-ice data for a date and return
    sea-ice concentration for the given location.
    """

    file_path = download_sea_ice_file(data_date, output_dir)

    return get_sea_ice_at_location(
        file_path,
        latitude,
        longitude
    )

def classify_sea_ice(concentration):
    """
    Convert sea-ice concentration (%) into a simple map category.
    """
    if concentration is None:
        return "UNKNOWN"

    if concentration < 30:
        return "LOW"

    if concentration <= 70:
        return "MEDIUM"

    return "HIGH"
