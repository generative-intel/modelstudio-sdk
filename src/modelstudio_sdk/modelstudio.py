"""
This is the interface script to call the modelstudio-api for:
- prediction of images through the api
  prediction is done with exponential backoff

The project specific api-url and api_key to make successful requests.
"""

import argparse
import logging
import sys
from urllib.parse import unquote


from modelstudio_sdk import __version__
from modelstudio_sdk.predictor import ModelStudioPredictor, read_images


__author__ = "nacho"
__copyright__ = "nacho"
__license__ = "MIT"

logger = logging.getLogger(__name__)


def positive_int(value):
    """Validator for positive integers"""
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"must be > 0, got {value}")
    return ivalue


def parse_args(args):
    """Parse command line parameters"""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
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

    subparsers = parser.add_subparsers(dest='subcommand', help='Available subcommands')

    # Predict subcommand
    predict_parser = subparsers.add_parser('predict', help='run a prediction')
    predict_parser.add_argument("--url", required=True, help="Project specific API URL")
    predict_parser.add_argument("--api_key", required=True, help="Project specific API key")
    predict_parser.add_argument("--images", nargs="+", required=True, help="List of images")
    predict_parser.add_argument("--timeout", type=float, default=10, help="timeout (in seconds)")
    predict_parser.add_argument("--max_retries", type=positive_int, default=3, help="max_retries (must be > 0)")
    predict_parser.add_argument("--base_delay", type=float, default=2, help="base_delay (seconds)")

    # Add other subcommands here in the future

    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging"""
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def predict_command(args):
    """Handle the predict subcommand"""
    logger.info("Executing predict command")

    predictor = ModelStudioPredictor(
        unquote(args.url),
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


def main(args):
    """Main entry point handling different subcommands"""
    args = parse_args(args)
    setup_logging(args.loglevel)

    # Handle subcommands
    if args.subcommand == 'predict':
        predict_command(args)

    elif args.subcommand is None:
        logger.error("No subcommand specified. Use --help for available commands.")
        sys.exit(1)

    else:
        logger.error(f"Unknown subcommand: {args.subcommand}")
        sys.exit(1)


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
