#!/usr/bin/env python3 -u
"""
Usage:
    pow all
    pow add <entry> <label>...
    pow paste <label>...
    pow remove <label>...
    pow echo <label>...
    pow open <label>...
    pow edit
    pow <label>...
    pow -h | --help
Options:
    -q, --quiet
"""
import json
import webbrowser
import subprocess
import sys
from collections import Counter
from functools import partial

from docopt import docopt
import colorama
# TODO: from fuzzywuzzy import fuzz

# TODO: transition formats:
# {'entry': '¯\\_(ツ)_/¯', 'labels': ['shrug']}
# {'¯\\_(ツ)_/¯': ['shrug']}

# TODO: initialize ~/.config/pow


def colored(color, s):
    return color + s + colorama.Fore.RESET


cyan = partial(colored, colorama.Fore.CYAN)
green = partial(colored, colorama.Fore.GREEN)
red = partial(colored, colorama.Fore.RED)


def set_clipboard(contents):
    # TODO: linux, win32, cygwin
    if sys.platform.startswith('darwin'):
        subprocess.run('pbcopy', input=contents.encode('utf-8'))
    else:
        raise NotImplementedError('unsupported platform')


class Pow:

    # TODO: LOL FIXME
    path = '/Users/frederick/.config/pow/pow.json'
    success = green('POW!')
    failure = red('Nertz!')

    def __init__(self, rows):
        self.rows = rows

    @classmethod
    def load(cls):
        with open(cls.path) as f:
            return cls(json.load(f)['entries'])

    def save(self):
        with open(self.path, 'w') as f:
            json.dump({'entries': self.rows}, f, ensure_ascii=False, indent=2)

    def select(self, labels):
        labels = Counter(labels)

        def all_labels_match(row):
            return not labels - Counter(row['labels'])

        return [row for row in self.rows if all_labels_match(row)]

    def add(self, entry, labels):
        self.rows.append({'entry': entry, 'labels': labels})
        self.save()
        print('{} added {} with labels {}'.format(self.success, entry, labels))

    def delete(self, entry):
        pass  # TODO

    def set(self, entry, labels):
        pass  # TODO

    def label(self, entry, labels):
        pass  # TODO

    def print(self, labels=()):
        rows = self.select(labels)
        print('{} Found {} entries:'.format(self.success, len(rows)))
        for row in rows:
            print(row['entry'], row['labels'])

    def default(self, labels):
        rows = self.select(labels)
        if not rows:
            if len(labels) == 1:
                print('{} Nothing matched that label.'.format(self.failure))
            else:
                print('{} Nothing matched those labels.'.format(self.failure))
        elif len(rows) == 1:
            entry = rows[0]['entry']
            set_clipboard(entry)
            print('{} Copied {} to the clipboard.'.format(self.success, cyan(entry)))
        else:
            print('{} Found {} matches:'.format(self.success, len(rows)))
            print()
            for row in rows:
                print(cyan(row['entry']), row['labels'])
            print()
            print('(add -f to copy them all)')

    def open(self, labels):
        rows = self.select(labels)
        if not rows:
            if len(labels) == 1:
                print('{} Nothing matched that label.'.format(self.failure))
            else:
                print('Nertz! Nothing matched those labels.')
        elif len(rows) == 1:
            entry = rows[0]['entry']
            result = webbrowser.open_new(entry)
            print(type(result), result)
            print('{} Opening {} in a browser.'.format(self.success, cyan(entry)))
        else:
            print('{} Found {} matches:'.format(self.success, len(rows)))
            print()
            for row in rows:
                print(cyan(row['entry']), row['labels'])
            print()
            print('(add -f to open them all)')


if __name__ == '__main__':
    args = docopt(__doc__)
    # print(args)

    entry = args.get('<entry>')
    labels = args.get('<label>')

    pow = Pow.load()

    if args['all']:
        pow.print()
    elif args['add']:
        pow.add(entry, labels)
    elif args['open']:
        pow.open(labels)
    else:
        pow.default(labels)
