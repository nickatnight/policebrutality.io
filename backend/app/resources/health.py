import falcon


class Ping(object):
    """
    Is our service alive?

    Return 200 if OK, fail or not respond otherwise
    """

    def on_get(self, req: falcon.Request, resp: falcon.Response):
        resp.status = falcon.HTTP_200
        resp.media = {"pong": "OK"}
