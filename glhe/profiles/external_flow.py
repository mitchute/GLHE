from glhe.profiles.external_base import ExternalBase


class ExternalFlow(ExternalBase):

    def __init__(self, path):
        ExternalBase.__init__(self, path=path, col_num=1)
