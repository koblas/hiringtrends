#!/usr/bin/env python

import os
import sys
import json
import functools
from hiring import submission

def main(dirname, outdir):
    posts = submission.load(dirname, submission.WHO_IS_HIRING)

    def order(a, b):
        if a.year != b.year:
            return a.year - b.year
        return a.month_num - b.month_num

    spost = sorted(posts, key=functools.cmp_to_key(order), reverse=True)

    while spost:
        post = spost[0]
        if post.year == 2011:
            break
        file = '%d/data-%d%02d01.js' % (post.year, post.year, post.month_num)
        data = []
        for p in spost:
            print("Building", p.short_time())
            data.append({
                'month' : p.short_time(),
                'num_comments' : len(p.comments),
                'terms' : p.term_stats(),
            })

        with open(os.path.join(outdir, file), 'w') as fd:
            json.dump(data, fd)

        spost.pop(0)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: %s DIRNAME" % sys.argv[0])
        sys.exit(1)
    main(sys.argv[1], 'static')
