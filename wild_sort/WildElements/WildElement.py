import ImageSorting.CallsToUI as ui



class WildElement():
    _code: str

    def __init__(self, code):
        self._code = code

    def show(self):
        ui.show(self._code)

    def hide(self):
        ui.hide(self._code)

    def focus(self):
        ui.focus(self._code)

    def set(self, value):
        ui.set(self._code, value)