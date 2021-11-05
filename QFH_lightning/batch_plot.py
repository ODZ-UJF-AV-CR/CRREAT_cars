import argparse
import datetime
from readrec import *
import os.path

def dateparse(time_in_secs):    
    return datetime.datetime.utcfromtimestamp(float(time_in_secs))

def main():

    parser = argparse.ArgumentParser(
        description='')
    parser.add_argument('recs', nargs='+', type=str)
    parser.add_argument('--pre', type=int, default=50)
    parser.add_argument('--post', type=int, default=50)
    parser.add_argument('--timemarks')
    args = parser.parse_args()
    
    marktimes = []
    if args.timemarks is not None:
        triggers = pd.read_csv(args.timemarks, delimiter=',',
                           parse_dates=True, date_parser=dateparse, index_col='DateTime',
                           usecols = [0], names=['DateTime'], header=None, squeeze = True)
        marktimes = triggers.index

    for fn in args.recs:
        with open(fn, 'rb') as f:
            try:
                print("reading %s..." % fn)
                h, samples, synclog = loadrec(f)
                fig = plotrec(h, samples, synclog, os.path.basename(fn),
                        title=os.path.basename(fn),
                        pre_trigger_blocks=args.pre,
                        post_trigger_blocks=args.post,
                        marktimes=marktimes)
                fig.savefig(os.path.basename(fn) + '.png', bbox_inches='tight')
                fig.clear()
                plt.close(fig)
            except:
                print(traceback.format_exc())
                continue

if __name__ == "__main__":
    main()
