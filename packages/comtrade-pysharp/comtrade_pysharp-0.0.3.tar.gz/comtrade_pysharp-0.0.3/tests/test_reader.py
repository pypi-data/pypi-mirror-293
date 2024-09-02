import os
from datetime import datetime
from pathlib import Path

import numpy as np

from comtrade_pysharp import read_comtrade

here = Path(os.path.dirname(__file__))
data_folder = here / ".." / "data"
simple = data_folder / "data.cfg"


def test_data_types():
    data = read_comtrade(simple)

    assert len(list(data.analog.keys())) == 130
    assert list(data.analog.keys())[0] == "UR1_ARU_uGSync_A"
    assert len(list(data.digital.keys())) == 45
    assert list(data.digital.keys())[0] == "UR1_50Hz LS Q1 geschlossen"

    for key, value in data.analog.items():
        assert isinstance(key, str)
        assert isinstance(value, np.ndarray)
        for data_point in value:
            assert isinstance(data_point, np.float32)

    for key, value in data.digital.items():
        assert isinstance(key, str)
        assert isinstance(value, np.ndarray)
        for data_point in value:
            assert isinstance(data_point, np.intc)

    assert isinstance(data.timestamps, list)
    for item in data.timestamps:
        assert isinstance(item, datetime)


def test_sparse():
    data = read_comtrade(simple, analog_channels=["UR1_ARU_uG_C__U_DS_L3_t"])
    assert list(data.analog.keys()) == ["UR1_ARU_uG_C__U_DS_L3_t"]
    assert len(data.digital.keys()) == 45

    data = read_comtrade(simple, digital_channels=["UR1_50Hz LS Q1 geschlossen"])
    assert list(data.digital.keys()) == ["UR1_50Hz LS Q1 geschlossen"]
    assert len(data.analog.keys()) == 130

    data = read_comtrade(
        simple,
        analog_channels=["UR1_ARU_uGSync_A"],
        digital_channels=["UR1_50Hz LS Q1 geschlossen"],
    )
    assert list(data.analog.keys()) == ["UR1_ARU_uGSync_A"]
    assert list(data.digital.keys()) == ["UR1_50Hz LS Q1 geschlossen"]

    data = read_comtrade(simple, analog_channels=["UR1_ARU_uG_B__U_DS_L2_t"])
    assert list(data.analog.keys()) == ["UR1_ARU_uG_B__U_DS_L2_t"]
    assert len(data.digital.keys()) == 45


def test_subsampling():
    """
    Full file has 173 000 samples. Divided by 3 gives 57666.6666667. So we should have 57667 in the subsampled.
    additionally, the timestamps should match.

    Also try with subsampling of 2. Subsampling of 2 should give 86500 samples.
    """
    full = read_comtrade(simple)
    subsampled_3 = read_comtrade(simple, subsampling=3)

    assert subsampled_3.analog["UR1_ARU_uGSync_A"].shape[0] == 57667
    assert full.analog["UR1_ARU_uGSync_A"].shape[0] == 173000
    assert full.timestamps[57666*3] == subsampled_3.timestamps[-1]

    subsampled_2 = read_comtrade(simple, subsampling=2)

    assert subsampled_2.analog["UR1_ARU_uGSync_A"].shape[0] == 86500
    assert full.analog["UR1_ARU_uGSync_A"].shape[0] == 173000
    assert full.timestamps[0] == subsampled_2.timestamps[0]
    assert full.timestamps[-2] == subsampled_2.timestamps[-1]  # -2 because there's an even number of samples total.


if __name__ == "__main__":
    test_data_types()
    test_sparse()
    test_subsampling()
