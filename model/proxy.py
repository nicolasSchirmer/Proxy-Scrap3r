from model.base_model import BaseModelObject


class Proxy(BaseModelObject):
    def __init__(self,
                 ip: str,
                 port: str,
                 type: str or None = None,
                 country: str or None = None,
                 google_able: bool or None = None):
        self.ip: str = ip
        self.port: str = port
        self.type: str or None = type
        self.country: str or None = country
        self.google_able: bool or None = google_able

    def __repr__(self):
        return "ip: " + str(self.ip) + "\n" \
               "port: " + str(self.port) + "\n" \
               "type: " + str(self.type) + "\n" \
               "country: " + str(self.country) + "\n" \
               "google_able: " + str(self.google_able) + "\n"
