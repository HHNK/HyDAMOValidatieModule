"""
Test voor datamodel.py
"""

from hydamo_validation.datamodel import HyDAMO
from pathlib import Path
import geopandas as gpd
from shapely.geometry import Point

try:
    from .config import DATA_DIR
except ImportError:
    from config import DATA_DIR

hydamo_version = "2.2"
object_layers = ['admingrenswaterschap',
                 'afsluitmiddel',
                 'afvoergebiedaanvoergebied',
                 'aquaduct',
                 'beheergrenswaterschap',
                 'bijzonderhydraulischobject',
                 'bodemval',
                 'brug',
                 'doorstroomopening',
                 'duikersifonhevel',
                 'gemaal',
                 'grondwaterinfolijn',
                 'grondwaterinfopunt',
                 'grondwaterkoppellijn',
                 'grondwaterkoppelpunt',
                 'hydroobject',
                 'hydroobject_normgp',
                 'kunstwerkopening',
                 'lateraleknoop',
                 'normgeparamprofiel',
                 'normgeparamprofielwaarde',
                 'peilafwijkinggebied',
                 'peilbesluitgebied',
                 'peilgebiedpraktijk',
                 'peilgebiedvigerend',
                 'pomp',
                 'regelmiddel',
                 'reglementgrenswaterschap',
                 'streefpeil',
                 'stuw',
                 'vispassage',
                 'vispassagevlak',
                 'zandvang']

ignored_layers = ['afvoeraanvoergebied',
                  'imwa_geoobject',
                  'leggerwatersysteem',
                  'leggerwaterveiligheid',
                  'waterbeheergebied']

dataset_gpkg = DATA_DIR / "tasks" / "test_wrij" / "datasets" / "HyDAMO.gpkg"
hydroobject_gdf = gpd.read_file(dataset_gpkg, layer="Hydroobject")
stuw_gdf = gpd.read_file(dataset_gpkg, layer="Stuw")

exports_dir = Path(__file__).parent / "exports"
exports_dir.mkdir(exist_ok=True)

datamodel = HyDAMO(version=hydamo_version)


def test_version():
    assert datamodel.version == hydamo_version


def test_layers():
    assert datamodel.layers == object_layers


def test_ignored_layers():
    assert datamodel.ignored_layers == ignored_layers


def test_setting_data():
    datamodel.set_data(hydroobject_gdf, "hydroobject")
    assert not datamodel.hydroobject.empty


def test_typeerror_data():
    gdf = hydroobject_gdf.copy()
    gdf.loc[0, "geometry"] = Point(0, 0)
    try:
        datamodel.set_data(gdf, "hydroobject")
        assert False
    except TypeError:
        assert True


def test_keyerror_missing_column():
    gdf = hydroobject_gdf.copy()
    gdf.drop("categorieoppwaterlichaam", axis=1, inplace=True)
    try:
        datamodel.hydroobject._check_columns(gdf)
        assert False
    except KeyError:
        assert True


def test_snapping_data():
    datamodel.set_data(hydroobject_gdf, "hydroobject", index_col="nen3610id")
    datamodel.set_data(stuw_gdf, "stuw", index_col="nen3610id")
    datamodel.stuw.snap_to_branch(datamodel.hydroobject, snap_method="overall")
    assert "branch_id" in datamodel.stuw.columns


def test_exporting_data():
    datamodel.set_data(hydroobject_gdf, "hydroobject", index_col="nen3610id")
    result = exports_dir / "result.gpkg"
    if result.exists():
        result.unlink()
    datamodel.to_geopackage(result)
    assert result.exists()
    if result.exists():
        result.unlink()
    datamodel.to_geopackage(result, use_schema=False)
    assert result.exists()
    if result.exists():
        result.unlink()

