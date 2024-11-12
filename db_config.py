from dotenv import load_dotenv

import os


load_dotenv()



TORTOISE_ORM = {
    "connections": {
         "default": os.getenv("DB_URL")
    },
    "apps": {
        "models": {
            "models": [
                "aerich.models",
                
                # Call models file
                "app.models.user"
                ],
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": "UTC"
}
