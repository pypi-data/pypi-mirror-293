from argparse import ArgumentParser
from os import getenv
from asyncio import to_thread, gather, run
from taxi_data_advanced.gather_bwc_data import gather_bwc_data
from taxi_data_advanced.gather_gps_data import gather_gps_data

async def async_gather_bwc_data(start_date: str, finish_date: str, destination: str) -> None:
    await to_thread(gather_bwc_data, start_date, finish_date, destination)

async def async_gather_gps_data(start_date: str, finish_date: str, destination: str) -> None:
    await to_thread(gather_gps_data, start_date, finish_date, destination)

async def gather_all_data(start_date: str, finish_date: str, destination: str) -> None:
    await gather(async_gather_bwc_data(start_date, finish_date, destination),
                 async_gather_gps_data(start_date, finish_date, destination))

def main() -> None:
    parser = ArgumentParser(description='Gathers data all sources and stores in database')
    parser.add_argument('--start_date',type=str,required=False,help="start date to get shifts and jobs from",default="18/08/2024")
    parser.add_argument('--finish_date',type=str,required=False,help="finish date to get shifts and jobs from",default="20/08/2024")
    parser.add_argument('--destination',type=str,required=False,help="destination folder for downloaded data",default=f"{getenv('HOME')}/taxi_data")
    args, unknown = parser.parse_known_args()

    run(gather_all_data(args.start_date, args.finish_date, args.destination))

if __name__ == '__main__':
    main()