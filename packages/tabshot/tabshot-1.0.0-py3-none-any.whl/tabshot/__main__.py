import argparse
from .func_save import execute_save_mode
from .func_load import execute_load_mode
from .func_print import execute_print_mode

def main():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="sub-command help", dest="command")

    # command print
    parser_print = subparsers.add_parser("print", aliases=["p"])

    # command save
    parser_save = subparsers.add_parser("save", aliases=["s"])
    parser_save.add_argument("outfile", type=str,
        help="output filename")
    parser_save.add_argument("-d", "--description", type=str,
        help="description of the saved browser tab URLs")

    # command load
    parser_load = subparsers.add_parser("load", aliases=["l"])
    parser_load.add_argument("infile", type=str,
        help="input filename")

    # execute functionality
    args = parser.parse_args()

    if args.command in {"print", "p"}:
        execute_print_mode()
    
    elif args.command in {"save", "s"}:
        execute_save_mode(args.outfile, args.description)
    
    elif args.command in {"load", "l"}:
        execute_load_mode(args.infile)
    
    return

if __name__ == "__main__":
    main()