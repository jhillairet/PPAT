# -*- coding: utf-8 -*-
"""
Testing DCS setting module
"""
import pytest
from pppat.libpulse.DCS_setting import DCSSettings

sup_filename = '../resources/pulse_setup_examples/52865/Sup.xml'


def test_wrong_filename():
    with pytest.raises(FileNotFoundError):
        DCSSettings(sup_filename+'_')
