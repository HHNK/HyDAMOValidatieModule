# %%
import geopandas as gpd
import hhnk_research_tools as hrt
import numpy as np
import pytest
from pathlib import Path
from tests.config import DATA_DIR

# always_skip_for_now = True  # TODO remove later when test works


# %%
# TODO remove skip when py312 implemented.
# @pytest.mark.skipif(sys.version_info < (3, 12) or always_skip_for_now, reason="Requires Python 3.12 or higher")
def test_gemaal_custom_functions():
    from hydamo_validation.datamodel import HyDAMO
    from hydamo_validation.functions import custom

    """
    This function will test the customs function that where done for gemaal converter. Specifically it test to
    functions: intersected_pump_peilgebieden, gemaal_streefpeil_value
    """
    logger = hrt.logging.get_logger(__name__)

    # load data
    TEST_DIRECTORY = Path(r"D:\github\jacosta\hhnk-threedi-tools\tests\data")
    hydamo_file_path = TEST_DIRECTORY / "schematisation_builder" / "HyDAMO.gpkg"

    # select layer to do the test
    # gemaal = gpd.read_file(hydamo_file_path, layer="gemaal")
    # polder = gpd.read_file(hydamo_file_path, layer="polder")
    # combinatiepeilgebied_gdf = gpd.read_file(hydamo_file_path, layer="combinatiepeilgebied")


    # make a hydamo object out f the temp file
    hydamo = HyDAMO.from_geopackage(DATA_DIR, check_columns=False)

    # run functions
    results_intersected_pump_peilgebieden = custom.intersected_pump_peilgebieden(gpd.GeoDataFrame, hydamo)
    results_gemaal_streefpeil_value = custom.gemaal_streefpeil_value(gpd.GeoDataFrame, hydamo)

    # # assert intersected code peilgebied KMG-Q-25259
    # val_25259 = results_gemaal_streefpeil_value.loc[results_gemaal_streefpeil_value['code']=='KGM-Q-25259', 'pgd_codes'].values[0]
    # assert val_25259 == "CMB_2020-6, CMB_GPG-Q-140709"

    # # assert intersected code peilgebied KGM-Q-25263
    # val_25263 = results_gemaal_streefpeil_value.loc[results_gemaal_streefpeil_value["code"] == "KGM-Q-25263", "pgd_codes"].values[0]
    # assert val_25263 == "CMB_GPG-W-32, CMB_GPG-Q-140717"

    # #gemaal code KGM-Q-25259 in intersected with peilgebiedes CMB_2020-6, CMB_GPG-Q-140709
    # val_25263 = results_gemaal_streefpeil_value.loc[results_gemaal_streefpeil_value["code"] == "KGM-Q-25263", "pgd_codes"].values[0]
    # assert val_25263 == "CMB_GPG-W-32, CMB_GPG-Q-140717"

    # #gemaal code KGM-Q-25259 in intersected with peilgebiedes CMB_2020-6, CMB_GPG-Q-140709
    # val_25263 = results_gemaal_streefpeil_value.loc[results_gemaal_streefpeil_value["code"] == "KGM-Q-25265", "pgd_codes"].values[0]
    # assert val_25263 == "CMB_GPG-Q-140716, CMB_1000-01"

    # asset functions
    assert np.sum(results_intersected_pump_peilgebieden["distance_to_peilgebied"] == 0.0)
    assert np.average(results_gemaal_streefpeil_value["aantal_peilgebieden"] == 2.0)


# %%
if __name__ == "__main__":
    test_gemaal_custom_functions()
# %%
