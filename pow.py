#!/usr/bin/env python3 -u
"""
Usage:
    pow all
    pow add <entry> <label>...
    pow paste <label>...
    pow label <entry> <label>...
    pow relabel <entry> <label>...
    pow unlabel <entry> <label>...
    pow remove <entry>
    pow echo <label>...
    pow open <label>...
    pow edit
    pow <label>...
    pow -h | --help
Options:
    -q, --quiet
    -m, --multi
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

    def __init__(self, rows):
        self.rows = rows

    @classmethod
    def load(cls):
        with open(cls.path) as f:
            return cls(json.load(f)['entries'])

    def success(self, *args, **kwargs):
        print(green('POW!'), *args, **kwargs)

    def failure(self, *args, **kwargs):
        print(red('Nertz!'), *args, **kwargs)

    def info(self, *args, **kwargs):
        print(*args, **kwargs)

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
        self.success('Added {} with labels {}'.format(entry, labels))

    def remove(self, entry):
        pass  # TODO

    def label(self, entry, labels):
        pass  # TODO

    def relabel(self, entry, labels):
        pass  # TODO

    def unlabel(self, entry, labels):
        pass  # TODO

    def print(self, labels=()):
        rows = self.select(labels)
        self.success('Found {} entries:'.format(len(rows)))
        for row in rows:
            self.info(row['entry'], row['labels'])

    def default(self, labels):
        rows = self.select(labels)
        if not rows:
            if len(labels) == 1:
                self.failure('Nothing matched that label.')
            else:
                self.failure('Nothing matched those labels.')
        elif len(rows) == 1:
            entry = rows[0]['entry']
            set_clipboard(entry)
            self.success('Copied {} to the clipboard.'.format(cyan(entry)))
        else:
            self.success('Found {} matches:'.format(len(rows)))
            self.info()
            for row in rows:
                self.info(cyan(row['entry']), row['labels'])
            self.info()
            self.info('(add -m to copy them all)')

    def open(self, labels):
        rows = self.select(labels)
        if not rows:
            if len(labels) == 1:
                self.failure('Nothing matched that label.')
            else:
                self.failure('Nothing matched those labels.')
        elif len(rows) == 1:
            entry = rows[0]['entry']
            result = webbrowser.open_new(entry)
            self.info(type(result), result)
            self.success('Opening {} in a browser.'.format(cyan(entry)))
        else:
            self.success('Found {} matches:'.format(len(rows)))
            self.info()
            for row in rows:
                self.info(cyan(row['entry']), row['labels'])
            self.info()
            self.info('(add -m to open them all)')


if __name__ == '__main__':
    args = docopt(__doc__)
    print(args)

    if args['edit']:
        pass  # TODO

    entry = args.get('<entry>')
    labels = args.get('<label>')

    pow = Pow.load()

    if args['all']:
        pow.print()
    elif args['add']:
        pow.add(entry, labels)
    elif args['paste']:
        pow.paste(labels)
    elif args['label']:
        pow.label(entry, labels)
    elif args['relabel']:
        pow.relabel(entry, labels)
    elif args['unlabel']:
        pow.unlabel(entry, labels)
    elif args['remove']:
        pow.remove(entry)
    elif args['echo']:
        pow.echo(labels)
    elif args['open']:
        pow.open(labels)
    else:
        pow.default(labels)
