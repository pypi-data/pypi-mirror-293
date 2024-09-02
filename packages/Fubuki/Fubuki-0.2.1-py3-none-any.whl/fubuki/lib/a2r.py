class RSC:
    pass

    def scope(scope: dict):
        if scope["type"] == "ws":
            asgi_type = "websocket"
        elif scope["type"] == "http":
            asgi_type = "http"
        asgi_scope = {
            "type": asgi_type,
            "http_version": scope["http_version"],
            "server": tuple(scope['server'].split(':')),
            "client": tuple(scope['server'].split(':')),
            "scheme": scope["scheme"],
            "method": scope["method"],
            "path": scope["path"],
            "query_string": scope['query_string'].encode('utf-8'),
            "headers": [(key.encode('utf-8'), value.encode('utf-8')) for key, value in scope['headers'].items()],
            "__rsgi__": {
                "version": scope["rsgi_version"],
                "authority": scope["authority"]
            }
        }
        return asgi_scope