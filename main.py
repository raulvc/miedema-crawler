import argparse
import concurrent.futures as cf
import os
from multiprocessing import cpu_count

from src.crawler.pairs import PairsCrawler
from src.crawler.values import ValuesCrawler
from src.writer import Writer

MIEDEMA_URL = "http://www.entall.imim.pl/calculator/"
NUM_CORES = cpu_count()


def parse_args():
    parser = argparse.ArgumentParser()
    default_out = os.path.join(os.getcwd(), 'output.csv')
    parser.add_argument('-o', '--out', type=str, help='Output filepath.', default=default_out)
    parser.add_argument('-u', '--url', type=str, help='Miedema calculator URL', default=MIEDEMA_URL)

    return parser.parse_args()


def crawl_values(u, p):
    vals = ValuesCrawler(url=u, pair=p).run()
    return p, vals


if __name__ == '__main__':
    args = parse_args()

    url = args.url
    pairs = PairsCrawler(url=url).run()

    with cf.ProcessPoolExecutor(NUM_CORES) as executor:
        writer = Writer(out_file=args.out)
        jobs = [executor.submit(crawl_values, url, pair) for pair in pairs]

        for complete_job in cf.as_completed(jobs):
            pair, values = complete_job.result()
            writer.write(pair, values)
            writer.flush()

    writer.close()
