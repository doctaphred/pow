#!/usr/bin/env python3 -u
"""
POW! Command line text snippets, inspired by Zach Holman's **boom**.

# TODO: why won't docopt allow in-line descriptions?
# (Switch to click/argparse?)

  pow (list|ls)                         List all entries
  pow (add|new|set) <entry> <label>...  Add a new entry
  pow label <entry> <label>...          Add labels to an existing entry
  pow relabel <entry> <label>...        Replace the labels of an existing entry
  pow unlabel <entry> <label>...        Remove labels from an existing entry
  pow (remove|rm|delete) <entry>        Remove an existing entry
  pow echo [options] <label>...         Echo without copying
  pow open [options] <label>...         Open url in browser
  pow edit                              Open pow.json in editor
  pow (view|cat)                        Dump pow.json on the screen
  pow [options] <label>...              Copy specified entry to the clipboard

Usage:
  pow (list|ls)
  pow (add|new|set) <entry> <label>...
  pow label <entry> <label>...
  pow relabel <entry> <label>...
  pow unlabel <entry> <label>...
  pow (remove|rm|delete) <entry>
  pow echo [options] <label>...
  pow open [options] <label>...
  pow edit
  pow (view|cat)
  pow [options] <label>...
  pow -h | --help

Options:
  -q, --quiet   Only print the requested entry
  -m, --multi   Operate on multiple entries
"""
import json
import subprocess
import sys
import webbrowser
from collections import Counter
from functools import partial, wraps
from pathlib import Path

import colorama
from docopt import docopt
# TODO: from fuzzywuzzy import fuzz


def colored(color, s):
    return getattr(colorama.Fore, color.upper()) + s + colorama.Fore.RESET


cyan = partial(colored, 'cyan')
green = partial(colored, 'green')
red = partial(colored, 'red')


def get_clipboard():
    # TODO: linux, win32, cygwin
    if sys.platform.startswith('darwin'):
        return subprocess.run(
            'pbpaste', universal_newlines=True, stdout=subprocess.PIPE).stdout
    else:
        raise NotImplementedError('unsupported platform')


def set_clipboard(contents):
    # TODO: linux, win32, cygwin
    if sys.platform.startswith('darwin'):
        subprocess.run('pbcopy', input=contents.encode('utf-8'))
    else:
        raise NotImplementedError('unsupported platform')


class Pow:

    pow_dir = Path('~/.config/pow/').expanduser()
    path = pow_dir / 'pow.json'

    exit_code = 0

    def __init__(self, rows, quiet=False, multi=False):
        self.rows = rows
        self.quiet = quiet
        self.multi = multi

    def success(self, *args, **kwargs):
        if not self.quiet:
            print(green('POW!'), *args, **kwargs)

    def failure(self, *args, **kwargs):
        if not self.quiet:
            print(red('Nertz!'), *args, **kwargs)
        self.exit_code = 1

    def info(self, *args, **kwargs):
        if not self.quiet:
            print(*args, **kwargs)

    @classmethod
    def load(cls, *args, **kwargs):
        cls.pow_dir.mkdir(parents=True, exist_ok=True)
        try:
            with cls.path.open() as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        return cls(rows=data, *args, **kwargs)

    def save(self):
        with self.path.open('w') as f:
            json.dump(self.rows, f, ensure_ascii=False, indent=2,
                      sort_keys=True)

    def select(self, labels):
        labels = Counter(labels)

        def all_labels_match(row):
            return not labels - Counter(self.rows[row])

        return [row for row in self.rows if all_labels_match(row)]

    def new_entry(func):
        @wraps(func)
        def wrapper(self, entry, *args, **kwargs):
            if entry in self.rows:
                self.failure(cyan(entry), 'already labeled', self.rows[entry])
            else:
                func(self, entry, *args, **kwargs)
        return wrapper

    def existing_entry(func):
        @wraps(func)
        def wrapper(self, entry, *args, **kwargs):
            if entry not in self.rows:
                self.failure('Did not find', cyan(entry))
            else:
                func(self, entry, *args, **kwargs)
        return wrapper

    @new_entry
    def add(self, entry, labels):
        self.rows[entry] = labels
        self.save()
        if len(labels) == 1:
            self.success('Added', cyan(entry), 'with label', labels)
        else:
            self.success('Added', cyan(entry), 'with labels', labels)

    @existing_entry
    def remove(self, entry):
        del self.rows[entry]
        self.save()
        self.success('Removed', cyan(entry))

    @existing_entry
    def label(self, entry, labels):
        self.rows[entry].extend(labels)
        self.save()
        self.success('Labeled', cyan(entry), 'with', labels)

    @existing_entry
    def relabel(self, entry, labels):
        self.rows[entry] = labels
        self.save()
        self.success('Relabeled', cyan(entry), 'as', labels)

    @existing_entry
    def unlabel(self, entry, labels):
        for label in labels:
            try:
                self.rows[entry].remove(label)
            except ValueError:
                pass
        self.save()
        self.success('Removed', labels, 'from', cyan(entry))

    def list(self):
        if not self.rows:
            self.failure('Nothing here!')
        else:
            if len(self.rows) == 1:
                self.success('1 entry:')
            else:
                self.success(len(self.rows), 'entries:')
            self.info()
            for entry in sorted(self.rows):
                self.info(cyan(entry), self.rows[entry])
            self.info()

    def default(self, labels):
        rows = self.select(labels)
        if not rows:
            if len(labels) == 1:
                message = 'Nothing matched that label.'
            else:
                message = 'Nothing matched those labels.'
            self.failure(message)
        elif len(rows) == 1:
            entry = next(iter(rows))
            set_clipboard(entry)
            self.success('Copied', cyan(entry), 'to the clipboard.')
        elif self.multi:
            set_clipboard('\n'.join(rows))
            self.success('Copied', len(rows), 'entries to the clipboard:')
            self.info()
            for entry in rows:
                self.info(cyan(entry))
            self.info()
        else:
            self.success('Found', len(rows), 'matches:')
            self.info()
            for entry in rows:
                self.info(cyan(entry), self.rows[entry])
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
            entry = next(iter(rows))
            result = webbrowser.open_new(entry)
            self.info(type(result), result)
            self.success('Opening {} in a browser.'.format(cyan(entry)))
        else:
            self.success('Found {} matches:'.format(len(rows)))
            self.info()
            for entry in rows:
                self.info(cyan(entry), self.rows[entry])
            self.info()
            self.info('(add -m to open them all)')


def main():
    args = docopt(__doc__)
    # print(args)

    if args['edit']:
        raise NotImplementedError  # TODO
    if args['view'] or args['cat']:
        raise NotImplementedError  # TODO

    entry = args.get('<entry>')
    labels = args.get('<label>')

    if entry == '-':
        entry = get_clipboard()

    pow = Pow.load(quiet=args['--quiet'], multi=args['--multi'])

    # # TODO:
    # if '--' in labels:
    #     index = labels.index('--')
    #     labels = labels[:index]
    #     new_labels = labels[index + 1:]

    # TODO: switch to click or argparse, this is gross
    if args['list'] or args['ls']:
        pow.list()
    elif args['add'] or args['new'] or args['set']:
        pow.add(entry, labels)
    elif args['label']:
        pow.label(entry, labels)
    elif args['relabel']:
        pow.relabel(entry, labels)
    elif args['unlabel']:
        pow.unlabel(entry, labels)
    elif args['remove'] or args['rm'] or args['delete']:
        pow.remove(entry)
    elif args['echo']:
        pow.echo(labels)
    elif args['open']:
        pow.open(labels)
    else:
        pow.default(labels)

    sys.exit(pow.exit_code)


if __name__ == '__main__':
    main()
