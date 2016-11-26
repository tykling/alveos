from channels.routing import route
channel_routing = [
    route("http.request", "alveos.consumers.http_consumer"),
]

