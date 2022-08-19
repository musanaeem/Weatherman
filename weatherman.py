# Import Weatherman class and argument library
import argparse
from weather import Weatherman


# Arguments that are acceptable in the command line
parser = argparse.ArgumentParser(description="A weather reporting application")
parser.add_argument('path',
                    help="Path to file Extraction")
parser.add_argument('-e', '--max_results', nargs='+',
                    help="Report Highest/Lowest Temperature and Highest Humidity")
parser.add_argument('-a', '--avg_results', nargs='+',
                    help="Report Average Temperature and Humidity")
parser.add_argument('-c', '--chart_form', nargs='+',
                    help="Report Highest/Lowest Temperature and Humidity, separately, in chart form")
parser.add_argument('-b', '--chart_form_max_min', type=bool, default=False,  # Bonus task to print Temp together
                    help="Report Highest/Lowest Temperature together in chart form")
args = parser.parse_args()


# main function to run the code
if __name__ == '__main__':

    w = Weatherman(args.path, args.max_results, args.avg_results, args.chart_form, args.chart_form_max_min)
    w.run()

    # Extract("/Users/musanaeem/Documents/temp")

