import SorterLook.lib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--type', required=True, type=str)
args = parser.parse_args()

SorterLook.lib.Start(
    type=args.type
)
