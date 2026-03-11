import argparse
import sys

from pvactools.lib.aggregate_report_filter import AggregateReportFilter

def define_parser():
    return AggregateReportFilter.parser('pvacbind')

def main(args_input = sys.argv[1:]):
    parser = define_parser()
    args = parser.parse_args(args_input)

    AggregateReportFilter(
        args.input_file,
        args.output_file,
        include_tiers=args.include_tiers
    ).execute()

if __name__ == "__main__":
    main()
