import simplejson as json


class BaseModelObject:
    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, indent=4, use_decimal=True), use_decimal=True)
