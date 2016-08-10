from collections import defaultdict
from functools import lru_cache
import os
import re
import json
from . import terms
from . import util

WHO_IS_HIRING = 1

def load(dirname, group):
    isint = re.compile(r'^[0-9]+$')

    title_re = Submissions.HIRING_TITLE

    submissions = []

    for filename in os.listdir(dirname):
        if not isint.match(filename):
            continue

        with open(os.path.join(dirname, filename, filename + '.json')) as fd:
            data = json.load(fd)
            if title_re.match(data.get('title', '')):
                submissions.append(Submissions(dirname, filename))

    return submissions


class Submissions(object):
    HIRING_TITLE = re.compile(r'ask hn: who is hiring\? \((?P<month>.*) (?P<year>\d{4})\)', re.I)

    def __init__(self, dirname, id, title=None):
        if title is None:
            with open(os.path.join(dirname, id, id + '.json')) as fd:
                data = json.load(fd)
                title = data.get('title', '')

        m = self.HIRING_TITLE.match(title)
        self.month = m.group('month')
        self.year  = int(m.group('year'))

        self.month_num = util.MONTHS[self.month.lower()]

        self.title = title

        # Now load the comments
        self.comments = []

        dir2 = os.path.join(dirname, id)
        skip = ['.','..', id + '.json']

        for filename in os.listdir(dir2):
            if filename in skip:
                continue

            with open(os.path.join(dir2, filename)) as fd:
                c = Comment(json.load(fd))
                if not c.deleted:
                    self.comments.append(c)

    @lru_cache()
    def term_stats(self):
        counts = defaultdict(int)
        for c in self.comments:
            for term in c.terms():
                counts[term] += 1

        terms = {}
        c_count = len(self.comments)
        for rank, (term, count) in enumerate(sorted(counts.items(), key=lambda x: x[1], reverse=True)):
            terms[term] = {
                'full_term' : term,
                'count' : count,
                'percentage': round(100.0 * float(count) / float(c_count), 2),
                'mavg3': 0,
                'rank': rank,
            }

        return terms

    def short_time(self):
        """Return the short time version - e.g. Apr15"""
        return "%s%02d" % (util.SHORT_MONTH[self.month_num], self.year - 2000)
            

class Comment(object):
    """Wrapper for the HackerNews comment object, we have the following fields:

        id - Comment ID
        parent - parent post ID
        time - epoch timestamp
        text - the comment text
        score - score for this comment
        deleted - flag if it's deleted
        by - post author
        descendants - children of this comment -- NOT LOADED
    """

    def __init__(self, data):
        keys = ['id', 'parent', 'time', 'score', 'text', 'deleted', 'by', 'descendants']
        for k in keys:
            setattr(self, k, data.get(k))

    def terms(self):
        return terms.match_terms(self.text)
