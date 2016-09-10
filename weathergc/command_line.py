from forecast import Forecast
import sys

def main():
    print(Forecast(sys.argv[1]).as_json())
