from .quick_curate import run_curation
import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "report", 
        type=str, 
        help="The path to your spikeinterface generated report"
    )

    parser.add_argument(
        "output",
        type=str,
        help="Where to save the curated labels. By default, these are saved in the report folder as 'curated_labels.json'"
    )


    args = parser.parse_args()

    label_list = ["sua", "mua", "bad"]
#    report_path = "/Users/chris/Work/Edinburgh/Projects/Harry_Comparison/kilosort4_report/units/"
#    output_file = "curated_labels.json"

    run_curation(label_list, args.report, args.output)
