import string
import secrets
import argparse

from my_scripts.logger import setup_logger
from my_scripts.secrets_manager import my_secrets


def generate_password(length=8, use_special_chars=True):
    alphabet = string.hexdigits + "~!@#$%^&*"
    password = "".join(secrets.choice(alphabet) for i in range(length))
    return password


if __name__ == "__main__":
    logger = setup_logger(name="password_generator", log_file=my_secrets["logfile"])
    parser = argparse.ArgumentParser(prog="myprogram")
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        help="the length of the password string that you want to generate",
    )
    parser.add_argument(
        "-ds",
        "--disable-special-characters",
        type=str,
        help="do you want to disable special-characters",
    )  # on/off flag
    # option that takes a value
    args = parser.parse_args()
    if args.length <= 1:
        parser.print_help()
    else:
        logger.info(f"Genearting a password of length: {args.length}")
        logger.info(generate_password(length=args.length))
