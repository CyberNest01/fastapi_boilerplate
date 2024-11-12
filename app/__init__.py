

TORTOISE_ORM = {
    "connections": {
         "default": "mysql://azhide:1Y4cqu9xeJr8@192.168.130.29:3306/tests"
    },
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": "UTC"
}

class App:
    
    def ger_redis():
        pass
    
    def serialize():
        pass
    
    
__all__ = ["TORTOISE_ORM", "App"]
