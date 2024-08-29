# pylint: disable=missing-function-docstring, missing-module-docstring, unused-import
from unittest import mock

import numpy as np
import pytest
from bec_lib import messages
from qtpy.QtGui import QFontInfo

from bec_widgets.widgets.figure import BECFigure

from .client_mocks import mocked_client
from .conftest import create_widget


@pytest.fixture
def bec_image_show(bec_figure):
    yield bec_figure.image("eiger")


def test_on_image_update(qtbot, mocked_client):
    bec_image_show = create_widget(qtbot, BECFigure, client=mocked_client).image("eiger")
    data = np.random.rand(100, 100)
    msg = messages.DeviceMonitor2DMessage(device="eiger", data=data, metadata={"scan_id": "12345"})
    bec_image_show.on_image_update(msg.content, msg.metadata)
    img = bec_image_show.images[0]
    assert np.array_equal(img.get_data(), data)


def test_autorange_on_image_update(qtbot, mocked_client):
    bec_image_show = create_widget(qtbot, BECFigure, client=mocked_client).image("eiger")
    # Check if autorange mode "mean" works, should be default
    data = np.random.rand(100, 100)
    msg = messages.DeviceMonitor2DMessage(device="eiger", data=data, metadata={"scan_id": "12345"})
    bec_image_show.on_image_update(msg.content, msg.metadata)
    img = bec_image_show.images[0]
    assert np.array_equal(img.get_data(), data)
    vmin = max(np.mean(data) - 2 * np.std(data), 0)
    vmax = np.mean(data) + 2 * np.std(data)
    assert np.isclose(img.color_bar.getLevels(), (vmin, vmax), rtol=(1e-5, 1e-5)).all()
    # Test general update with autorange True, mode "max"
    bec_image_show.set_autorange_mode("max")
    bec_image_show.on_image_update(msg.content, msg.metadata)
    img = bec_image_show.images[0]
    vmin = np.min(data)
    vmax = np.max(data)
    assert np.array_equal(img.get_data(), data)
    assert np.isclose(img.color_bar.getLevels(), (vmin, vmax), rtol=(1e-5, 1e-5)).all()
    # Change the input data, and switch to autorange False, colormap levels should stay untouched
    data *= 100
    msg = messages.DeviceMonitor2DMessage(device="eiger", data=data, metadata={"scan_id": "12345"})
    bec_image_show.set_autorange(False)
    bec_image_show.on_image_update(msg.content, msg.metadata)
    img = bec_image_show.images[0]
    assert np.array_equal(img.get_data(), data)
    assert np.isclose(img.color_bar.getLevels(), (vmin, vmax), rtol=(1e-3, 1e-3)).all()
    # Reactivate autorange, should now scale the new data
    bec_image_show.set_autorange(True)
    bec_image_show.set_autorange_mode("mean")
    bec_image_show.on_image_update(msg.content, msg.metadata)
    img = bec_image_show.images[0]
    vmin = max(np.mean(data) - 2 * np.std(data), 0)
    vmax = np.mean(data) + 2 * np.std(data)
    assert np.isclose(img.color_bar.getLevels(), (vmin, vmax), rtol=(1e-5, 1e-5)).all()
