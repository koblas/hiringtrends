#!/usr/bin/env python

import os
import sys
import json
import functools
from hiring import submission

def main(dirname, dstr):
    posts = submission.load(dirname, submission.WHO_IS_HIRING)

    def order(a, b):
        if a.year != b.year:
            return a.year - b.year
        return a.month_num - b.month_num

    for post in posts:
        if post.short_time() != dstr:
            continue
        print(json.dumps(post.term_stats(), indent=2))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: %s DIRNAME" % sys.argv[0])
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
