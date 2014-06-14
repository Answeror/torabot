import json


class RequestMethodMixin(object):

    def make_requests_from_query(self, query):
        query = json.loads(query)
        for req in self.request_method_mapping[query['method']](query):
            yield req
