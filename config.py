import yaml


class Config:
    def __init__(self):
        with open("config.yaml", "r") as file:
            config_data = yaml.safe_load(file)

        db_config = config_data["database"]

        self.DEBUG = config_data.get("flask", {}).get("debug", True)

        self.SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{db_config['user']}:"
            f"{db_config['password']}@"
            f"{db_config['host']}/"
            f"{db_config['name']}"
        )

        self.SQLALCHEMY_TRACK_MODIFICATIONS = False