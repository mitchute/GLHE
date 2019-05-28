from glhe.properties.base_properties import PropertiesBase


class SoilProperties(PropertiesBase):

    def __init__(self, inputs):
        PropertiesBase.__init__(self, inputs)

    def get_temp(self, time: int = None, depth: float = None) -> float:
        pass  # pragma: no cover
