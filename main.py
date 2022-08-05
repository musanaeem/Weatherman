# Import Weatherman class and argument library
import argparse
from weather import Weatherman


# Arguments that are acceptable in the command line
parser = argparse.ArgumentParser(description="A weather reporting application")
parser.add_argument('path',
                    help="Path to file Extraction")
parser.add_argument('-e', '--Temp_Humidity', nargs='+',
                    help="Report Highest and Lowest Temp and Humidity")
parser.add_argument('-a', '--Avg_TH', nargs='+',
                    help="Report Average Temp and Humidity")
parser.add_argument('-c', '--chart_TH', nargs='+',
                    help="Report Highest and Lowest Temp and Humidity in chart form")
parser.add_argument('-b', '--chart_TH_bonus', type=bool, default=False,  # Bonus task to print Temp together
                    help="Report Highest and Lowest Temp together chart form")
args = parser.parse_args()


# main function to run the code
if __name__ == '__main__':

    w = Weatherman(args.path, args.Temp_Humidity, args.Avg_TH, args.chart_TH, args.chart_TH_bonus)
    w.run()

    # Extract("/Users/musanaeem/Documents/temp")

