"""
XBarcodeCamera
============

Defines the Kivy garden :class:`XBarcodeCamera` class which is the widget provided
by the xbarcodecamera flower.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.utils import _get_platform

__all__ = ("XBarcodeCamera",)

from ._version import __version__


class XBarcodeCamera(BoxLayout):
    """A :class:`~kivy.uix.boxlayout.BoxLayout` based class that shows
    a camera widget with superpowers based on the current platform.
    """

    def __init__(self, **kwargs):
        super(XBarcodeCamera, self).__init__(**kwargs)
        self.register_event_type("on_barcode")
        if _get_platform() == "ios":
            """
            iOS doesn't need pyzbar or anything similar, cause natively
            supports it, so We can use the kivy's Camera widget and configure it.
            """
            from kivy.uix.camera import Camera
            self._barcodewidget = Camera()
            self._barcodewidget._camera.start_metadata_analysis(
                callback=lambda t, code: self.dispatch("on_barcode", t, code)
            )
        else:
            try:
                from kivy_garden.zbarcam import ZBarCam
            except ImportError:
                print("kivy-garden/zbarcam is a requirement for non-iOS platforms")
                return
            self._barcodewidget = ZBarCam()
            self._barcodewidget.on_symbols = self.zbar_have_new_symbols
        self.add_widget(self._barcodewidget)

    def zbar_have_new_symbols(self):
        for x in self._barcodewidget.symbols:
            self.dispatch("on_barcode", "not_known", x.data.decode())

    def on_barcode(self, *args):
        pass
