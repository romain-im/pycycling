import yaml

class Configuration:
    def __init__(self):
        hr_conf, ht_conf = self.load_conf_file("./conf.yml")
        self.hr_address = hr_conf["address"]
        self.ht_address = ht_conf["address"]

    @staticmethod
    def load_conf_file(config_file) -> (dict):
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
        return config["hr"], config["ht"]