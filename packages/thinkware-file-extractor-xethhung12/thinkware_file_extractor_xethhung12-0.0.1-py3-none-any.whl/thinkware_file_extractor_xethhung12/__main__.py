import argparse
import sys

import thinkware_file_extractor_xethhung12 as thinkwareExtractor

def main():
    parser = argparse.ArgumentParser(
        prog='thinkware_file_extractor_xethhung12',
        description='extract thinkware data',
    )

    subparser=parser.add_subparsers(help="utils", dest="level1")
    utils_parser = subparser.add_parser(
        "utils", description="ratio"
    )

    utils_parser_level_2=utils_parser.add_subparsers(help="when-x", dest="level2")

    utils_parser_level_2_when_x=utils_parser_level_2.add_parser("when-x")
    utils_parser_level_2_when_x.add_argument(
        "--value", type=str, help="x value"
    )

    utils_parser_level_2_when_x=utils_parser_level_2.add_parser("when-y")
    utils_parser_level_2_when_x.add_argument(
        "--value", type=str, help="y value"
    )

    utils_parser_level_2_scale=utils_parser_level_2.add_parser("scale")
    utils_parser_level_2_scale.add_argument(
        "--value", type=str, help="scale value"
    )

    x = parser.parse_args(sys.argv[1:])
    if(x.level1 == "utils"):
        if(x.level2 == "when-x"):
            val = x.value
            return print(thinkwareExtractor.utils.get_x(val))
        elif x.level2 == "when-y":
            val = x.value
            return print(thinkwareExtractor.utils.get_y(val))
        elif x.level2 == "scale":
            val = x.value
            return print(thinkwareExtractor.utils.get_scale(val))
        else:
            print(x)
    else:
        print(x)


if __name__ == '__main__':
    main()
