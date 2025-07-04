import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--interval",
        "-int",
        type= int,
        default = 15,
        help = "interval for how often queries should be done"
    )
    parser.add_argument(
        "--port",
        type = int,
        default = 8000,
        help = "port for server to be hosted on, defaults to 8000"
    )
    parser.add_argument(
        "--json",
        type = str,
        required = True,
        help = "argument to a json file, where the json file specifies what services we need to query"
    )
    parser.add_argument(
        "--promurl",
        type = str,
        default= "http://prometheus:9090",
        help = "the url for the promtheus container thats running that has to be scraped"
    )

    return parser.parse_args()