import os
import unittest
import warnings
from pathlib import Path
from pymatgen.ext.matproj import MPRester
from pymatgen.core import SETTINGS
from _pytest.monkeypatch import MonkeyPatch
from monty.serialization import loadfn, dumpfn
from piro.route import SynthesisRoutes

TEST_FILES = Path(__file__).absolute().parent / "test_files"


class RoutesTest(unittest.TestCase):
    def setUp(self):
        # Monkeypatch if MAPI key not detected
        if not SETTINGS.get("PMG_MAPI_KEY"):
            warnings.warn("Using mock MPRester response")
            self.monkeypatch = MonkeyPatch()

            def get(*args, **kwargs):
                return loadfn(TEST_FILES / "ba-o-ti.json")
            self.monkeypatch.setattr(MPRester, "get_entries_in_chemsys", get)

    def test_basic_route(self):
        # BaTiO3 example
        route = SynthesisRoutes("mp-5020")
        route.recommend_routes(temperature=298)


def dump_tdata():
    """Quick helper function to dump data for future reference"""
    with MPRester() as mpr:
        data = mpr.get_entries_in_chemsys(
            ["Ba", "Ti", "O"], inc_structure="final",
            property_data=["icsd_ids", "formation_energy_per_atom"])
    dumpfn(data, TEST_FILES / "ba-o-ti.json")
    return data


if __name__ == '__main__':
    unittest.main()
