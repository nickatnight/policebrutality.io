class CORSMiddleware(object):
    def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header("Access-Control-Allow-Origin", "*")

        if (
            req_succeeded
            and req.method == "OPTIONS"
            and req.get_header("Access-Control-Request-Method")
        ):
            allow = resp.get_header("Allow")
            resp.delete_header("Allow")

            allow_headers = req.get_header(
                "Access-Control-Request-Headers", default="*"
            )

            resp.set_headers(
                (
                    ("Access-Control-Allow-Methods", allow),
                    ("Access-Control-Allow-Headers", allow_headers),
                    ("Access-Control-Max-Age", "86400"),  # 24 hours
                )
            )
