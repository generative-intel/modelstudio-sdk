"""
This is a simple script to call the modelstudio-api for:

- prediction of images through the api
"""

import argparse
import logging
import sys

from modelstudio_sdk import __version__
from modelstudio_sdk.predictor import ModelStudioPredictor, read_images


__author__ = "nacho"
__copyright__ = "nacho"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--version",
        action="version",
        version=f"modelstudio-sdk {__version__}",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    parser.add_argument("--url", required=True, help="API URL")
    parser.add_argument("--api_key", required=True, help="API key")
    parser.add_argument("--images", nargs="+", required=True, help="Paths to images")
    parser.add_argument("--timeout", type=float, default=10, help="timeout (seconds)")
    parser.add_argument("--max_retries", type=int, default=3, help="max_retries")
    parser.add_argument("--base_delay", type=float, default=2, help="base_delay (seconds)")
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging"""
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """ run the api on a set of images """
    args = parse_args(args)
    setup_logging(args.loglevel)

    predictor = ModelStudioPredictor(
        args.url,
        args.api_key,
        timeout=args.timeout,
        max_retries=args.max_retries,
        base_delay=args.base_delay,
    )

    for name, img_path in read_images(args.images):
        prediction = predictor.predict(img_path)
        print(name, prediction)
        if 'error' in prediction:
            break


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
