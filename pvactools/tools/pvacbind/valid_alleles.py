import sys

from pvactools.lib.valid_alleles import ValidAlleles

def define_parser():
    return ValidAlleles.parser('pvacbind')

def main(args_input = sys.argv[1:]):
    parser = define_parser()
    args = parser.parse_args(args_input)

    ValidAlleles(args.prediction_algorithm, args.species, args.length).print_valid_alleles()

if __name__ == "__main__":
    main()
