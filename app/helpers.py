"""Helpers."""
import yaml
import logging
import polars as pl



def load_yaml_file(file_path):
    """Load a yaml file.

    :param file_path: String
    :return: dict
    """
    with open(
        file=file_path,
        mode="r",
        encoding="utf-8",
    ) as ymlfile:
        return yaml.load(
            ymlfile,
            Loader=yaml.FullLoader,
        )


def load_csv_file(file_path):
    """read csv file
    """

    return pl.read_csv(file_path, separator=";")


def start_logger(config):
    """Starts recording.

    """
    extra = {'app_name': config.get("log").get("app_name"), 'environment': config.get("log").get("environment")}

    logger = logging.getLogger(__name__)
    syslog = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(app_name)s %(environment)s : %(message)s')
    syslog.setFormatter(formatter)
    logger.setLevel(config.get("log").get("level"))
    logger.addHandler(syslog)

    logger = logging.LoggerAdapter(logger, extra)
    return logger 

