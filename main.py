import argparse
from weather import Weatherman


parser = argparse.ArgumentParser(description="A weather reporting application")
parser.add_argument('path',
                    help="Path to file Extraction")
parser.add_argument('-e','--Temp_Humidity',
                    help="Report Highest and Lowest Temp and Humidity")
parser.add_argument('-a','--Avg_TH',
                    help="Report Average Temp and Humidity")
parser.add_argument('-c','--chart_TH',
                    help="Report Highest and Lowest Temp and Humidity in chart form")
args = parser.parse_args()


if __name__ == '__main__':
    w = Weatherman(args.path,args.Temp_Humidity,args.Avg_TH,args.chart_TH)
    w.run()

    # Extract("/Users/musanaeem/Documents/temp")

