# Stresses a website
# Pass a list of urls with [--url] parameter
# Can pass more than one parameter
# Pass the maxout number of outstanding requests as --max
# Pass the testsecs for how long the test must last; blank for continuous

import aiohttp
from argparse import ArgumentParser
import time
import asyncio
import random
from colorama import Fore, Style, init as colinit
colinit()

async def getreq(session, url, ts):
    """ sends out a request and returns its response code when
    complete with its timestamp, as at tuple """

    response = await session.get(url)
    return (ts, response)

async def main():
    parser = ArgumentParser()
    parser.add_argument("--url", dest = "urls", nargs = "+", default = [], 
                        help = "url to test. Can accept this parameter more than once")
    parser.add_argument("--maxout", dest = "maxout", default = 1000, type = int,
                        help = "maximum number of outstanding requests")
    args = parser.parse_args()
    if len(args.urls) < 1:
        raise Exception("Need at least one URL. Please pass using --url parameter for each url required")
    tasks = {}
    nanotimes = []
    status_codes = []
    response_codes = []
    async with aiohttp.ClientSession() as session:
        while True:
            timer = time.perf_counter_ns()
            done_count = 0
            if len(tasks) < args.maxout:
                # add two tasks
                for _ in range(200):
                    ts = time.perf_counter_ns()
                    url = random.sample(args.urls, 1)[0]
                    tasks[ts] = asyncio.create_task(getreq(session, url, ts))
            done, pending = await asyncio.wait(list(tasks.values()), 
                            return_when = asyncio.FIRST_COMPLETED)
            for task in done:
                stamp = task.result()[0]
                status_code = task.result()[1].status
                response_codes.append(status_code)
                if len(response_codes) > 10:
                    response_codes.pop(0)
                ns = time.perf_counter_ns() - stamp
                nanotimes.append(round(ns / 1e9, 4))
                if len(nanotimes) > 10:
                    nanotimes.pop(0) # remove first item
                print("last 10 queue_times, seconds", nanotimes, "response_codes", response_codes)
                del tasks[stamp]
                done_count = done_count + 1
            print("pending requests",  len(pending))
            time_taken = round((time.perf_counter_ns() - timer) / 1e9, 4)

            print((f"took {time_taken} seconds to do {done_count} requests, "
                   f"at {Fore.RED}{Style.BRIGHT}rate {round(1 / (time_taken / done_count), 2)} "
                   f"{Style.RESET_ALL} per request."))


if __name__ == "__main__":
    asyncio.run(main())











    







