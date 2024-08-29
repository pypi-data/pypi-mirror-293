# pylint: disable=missing-function-docstring, missing-module-docstring, unused-import

import numpy as np
import pytest

from bec_widgets.widgets.figure import BECFigure
from bec_widgets.widgets.figure.plots.image.image import BECImageShow
from bec_widgets.widgets.figure.plots.motor_map.motor_map import BECMotorMap
from bec_widgets.widgets.figure.plots.waveform.waveform import BECWaveform

from .client_mocks import mocked_client
from .conftest import create_widget


def test_bec_figure_init(qtbot, mocked_client):
    bec_figure = create_widget(qtbot, BECFigure, client=mocked_client)
    assert bec_figure is not None
    assert bec_figure.client is not None
    assert isinstance(bec_figure, BECFigure)
    assert bec_figure.config.widget_class == "BECFigure"


def test_bec_figure_init_with_config(mocked_client):
    config = {"widget_class": "BECFigure", "gui_id": "test_gui_id", "theme": "dark"}
    widget = BECFigure(client=mocked_client, config=config)
    assert widget.config.gui_id == "test_gui_id"
    assert widget.config.theme == "dark"


def test_bec_figure_add_remove_plot(qtbot, mocked_client):
    bec_figure = create_widget(qtbot, BECFigure, client=mocked_client)
    initial_count = len(bec_figure._widgets)

    # Adding 3 widgets -  2 WaveformBase and 1 PlotBase
    w0 = bec_figure.plot(new=True)
    w1 = bec_figure.plot(new=True)
    w2 = bec_figure.add_widget(widget_type="BECPlotBase")

    # Check if the widgets were added
    assert len(bec_figure._widgets) == initial_count + 3
    assert w0.gui_id in bec_figure._widgets
    assert w1.gui_id in bec_figure._widgets
    assert w2.gui_id in bec_figure._widgets
    assert bec_figure._widgets[w0.gui_id].config.widget_class == "BECWaveform"
    assert bec_figure._widgets[w1.gui_id].config.widget_class == "BECWaveform"
    assert bec_figure._widgets[w2.gui_id].config.widget_class == "BECPlotBase"

    # Check accessing positions by the grid in figure
    assert bec_figure[0, 0] == w0
    assert bec_figure[1, 0] == w1
    assert bec_figure[2, 0] == w2

    # Removing 1 widget
    bec_figure.remove(widget_id=w0.gui_id)
    assert len(bec_figure._widgets) == initial_count + 2
    assert w0.gui_id not in bec_figure._widgets
    assert w2.gui_id in bec_figure._widgets
    assert bec_figure._widgets[w1.gui_id].config.widget_class == "BECWaveform"


def test_add_different_types_of_widgets(qtbot, mocked_client):
    bec_figure = create_widget(qtbot, BECFigure, client=mocked_client)
    plt = bec_figure.plot(x_name="samx", y_name="bpm4i")
    im = bec_figure.image("eiger")
    motor_map = bec_figure.motor_map("samx", "samy")

    assert plt.__class__ == BECWaveform
    assert im.__class__ == BECImageShow
    assert motor_map.__class__ == BECMotorMap


def test_access_widgets_access_errors(qtbot, mocked_client):
    bec_figure = create_widget(qtbot, BECFigure, client=mocked_client)
    bec_figure.plot(row=0, col=0)

    # access widget by non-existent coordinates
    with pytest.raises(ValueError) as excinfo:
        bec_figure[0, 2]
        assert "No widget at coordinates (0, 2)" in str(excinfo.value)

    # access widget by non-existent widget_id
    with pytest.raises(KeyError) as excinfo:
        bec_figure["non_existent_widget"]
        assert "Widget with id 'non_existent_widget' not found" in str(excinfo.value)

    # access widget by wrong type
    with pytest.raises(TypeError) as excinfo:
        bec_figure[1.2]
        assert (
            "Key must be a string (widget id) or a tuple of two integers (grid coordinates)"
            in str(excinfo.value)
        )


def test_add_plot_to_occupied_position(qtbot, mocked_client):
    bec_figure = create_widget(qtbot, BECFigure, client=mocked_client)
    bec_figure.plot(row=0, col=0)

    with pytest.raises(ValueError) as excinfo:
        bec_figure.plot(row=0, col=0, new=True)
        assert "Position at row 0 and column 0 is already occupied." in str(excinfo.value)


def test_remove_plots(qtbot, mocked_client):
    bec_figure = create_widget(qtbot, BECFigure, client=mocked_client)
    w1 = bec_figure.plot(row=0, col=0)
    w2 = bec_figure.plot(row=0, col=1)
    w3 = bec_figure.plot(row=1, col=0)
    w4 = bec_figure.plot(row=1, col=1)

    assert bec_figure[0, 0] == w1
    assert bec_figure[0, 1] == w2
    assert bec_figure[1, 0] == w3
    assert bec_figure[1, 1] == w4

    # remove by coordinates
    bec_figure[0, 0].remove()
    assert w1.gui_id not in bec_figure._widgets

    # remove by widget_id
    bec_figure.remove(widget_id=w2.gui_id)
    assert w2.gui_id not in bec_figure._widgets

    # remove by widget object
    w3.remove()
    assert w3.gui_id not in bec_figure._widgets

    # check the remaining widget 4
    assert bec_figure[0, 0] == w4
    assert bec_figure[w4.gui_id] == w4
    assert w4.gui_id in bec_figure._widgets
    assert len(bec_figure._widgets) == 1


def test_remove_plots_by_coordinates_ints(qtbot, mocked_client):
    bec_figure = create_widget(qtbot, BECFigure, client=mocked_client)
    w1 = bec_figure.plot(row=0, col=0)
    w2 = bec_figure.plot(row=0, col=1)

    bec_figure.remove(row=0, col=0)
    assert w1.gui_id not in bec_figure._widgets
    assert w2.gui_id in bec_figure._widgets
    assert bec_figure[0, 0] == w2
    assert len(bec_figure._widgets) == 1


def test_remove_plots_by_coordinates_tuple(qtbot, mocked_client):
    bec_figure = create_widget(qtbot, BECFigure, client=mocked_client)
    w1 = bec_figure.plot(row=0, col=0)
    w2 = bec_figure.plot(row=0, col=1)

    bec_figure.remove(coordinates=(0, 0))
    assert w1.gui_id not in bec_figure._widgets
    assert w2.gui_id in bec_figure._widgets
    assert bec_figure[0, 0] == w2
    assert len(bec_figure._widgets) == 1


def test_remove_plot_by_id_error(qtbot, mocked_client):
    bec_figure = create_widget(qtbot, BECFigure, client=mocked_client)
    bec_figure.plot()

    with pytest.raises(ValueError) as excinfo:
        bec_figure.remove(widget_id="non_existent_widget")
        assert "Widget with ID 'non_existent_widget' does not exist." in str(excinfo.value)


def test_remove_plot_by_coordinates_error(qtbot, mocked_client):
    bec_figure = create_widget(qtbot, BECFigure, client=mocked_client)
    bec_figure.plot(row=0, col=0)

    with pytest.raises(ValueError) as excinfo:
        bec_figure.remove(0, 1)
        assert "No widget at coordinates (0, 1)" in str(excinfo.value)


def test_remove_plot_by_providing_nothing(qtbot, mocked_client):
    bec_figure = create_widget(qtbot, BECFigure, client=mocked_client)
    bec_figure.plot(row=0, col=0)

    with pytest.raises(ValueError) as excinfo:
        bec_figure.remove()
        assert "Must provide either widget_id or coordinates for removal." in str(excinfo.value)


# def test_change_theme(bec_figure): #TODO do no work at python 3.12
#     bec_figure.change_theme("dark")
#     assert bec_figure.config.theme == "dark"
#     assert bec_figure.backgroundBrush().color().name() == "#000000"
#     bec_figure.change_theme("light")
#     assert bec_figure.config.theme == "light"
#     assert bec_figure.backgroundBrush().color().name() == "#ffffff"
#     bec_figure.change_theme("dark")
#     assert bec_figure.config.theme == "dark"
#     assert bec_figure.backgroundBrush().color().name() == "#000000"


def test_change_layout(qtbot, mocked_client):
    bec_figure = create_widget(qtbot, BECFigure, client=mocked_client)
    w1 = bec_figure.plot(row=0, col=0)
    w2 = bec_figure.plot(row=0, col=1)
    w3 = bec_figure.plot(row=1, col=0)
    w4 = bec_figure.plot(row=1, col=1)

    bec_figure.change_layout(max_columns=1)

    assert np.shape(bec_figure.grid) == (4, 1)
    assert bec_figure[0, 0] == w1
    assert bec_figure[1, 0] == w2
    assert bec_figure[2, 0] == w3
    assert bec_figure[3, 0] == w4

    bec_figure.change_layout(max_rows=1)

    assert np.shape(bec_figure.grid) == (1, 4)
    assert bec_figure[0, 0] == w1
    assert bec_figure[0, 1] == w2
    assert bec_figure[0, 2] == w3
    assert bec_figure[0, 3] == w4


def test_clear_all(qtbot, mocked_client):
    bec_figure = create_widget(qtbot, BECFigure, client=mocked_client)
    bec_figure.plot(row=0, col=0)
    bec_figure.plot(row=0, col=1)
    bec_figure.plot(row=1, col=0)
    bec_figure.plot(row=1, col=1)

    bec_figure.clear_all()

    assert len(bec_figure._widgets) == 0
    assert np.shape(bec_figure.grid) == (0,)


def test_shortcuts(qtbot, mocked_client):
    bec_figure = create_widget(qtbot, BECFigure, client=mocked_client)
    plt = bec_figure.plot(x_name="samx", y_name="bpm4i")
    im = bec_figure.image("eiger")
    motor_map = bec_figure.motor_map("samx", "samy")

    assert plt.config.widget_class == "BECWaveform"
    assert plt.__class__ == BECWaveform
    assert im.config.widget_class == "BECImageShow"
    assert im.__class__ == BECImageShow
    assert motor_map.config.widget_class == "BECMotorMap"
    assert motor_map.__class__ == BECMotorMap


def test_plot_access_factory(qtbot, mocked_client):
    bec_figure = create_widget(qtbot, BECFigure, client=mocked_client)
    plt_00 = bec_figure.plot(x_name="samx", y_name="bpm4i")
    plt_01 = bec_figure.plot(x_name="samx", y_name="bpm4i", row=0, col=1)
    plt_10 = bec_figure.plot(new=True)

    assert bec_figure.widget_list[0] == plt_00
    assert bec_figure.widget_list[1] == plt_01
    assert bec_figure.widget_list[2] == plt_10
    assert bec_figure.axes(row=0, col=0) == plt_00
    assert bec_figure.axes(row=0, col=1) == plt_01
    assert bec_figure.axes(row=1, col=0) == plt_10

    assert len(plt_00.curves) == 1
    assert len(plt_01.curves) == 1
    assert len(plt_10.curves) == 0

    # update plt_00
    bec_figure.plot(x_name="samx", y_name="bpm3a")
    bec_figure.plot(x=[1, 2, 3], y=[1, 2, 3], row=0, col=0)

    assert len(plt_00.curves) == 3
