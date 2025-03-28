class Constant:
    """
    Constant ground temperature model.
    """

    def __init__(self, inputs):
        self.temperature = inputs['temperature']

    def get_temp(self, time: int = None, depth: float = None) -> float:
        return self.temperature
