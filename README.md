# POW!
### Command line text snippets, inspired by Zach Holman's **boom**

OS X only for now. Sorry.

"Installation": `alias pow='/path/to/pow.py`

Example usage:

```
$ pow ls
Nertz! Nothing here!

$ pow add '¯\_(ツ)_/¯' shrug
POW! Added ¯\_(ツ)_/¯ with label ['shrug']

$ pow shrug
POW! Copied ¯\_(ツ)_/¯ to the clipboard.

$ pow label - shruggie guy face  # '-' pastes from clipboard
POW! Labeled ¯\_(ツ)_/¯ with ['shruggie', 'guy', 'face']

$ pow add '(╯°□°）╯︵ ┻━┻' table flip face
POW! Added (╯°□°）╯︵ ┻━┻ with labels ['table', 'flip', 'face']

$ pow add '┬─┬ノ(º_ºノ)' calm face table put down
POW! Added ┬─┬ノ(º_ºノ) with labels ['calm', 'face', 'table', 'put', 'down']

$ pow ls
POW! 3 entries:

¯\_(ツ)_/¯ ['shrug', 'shruggie', 'guy', 'face']
(╯°□°）╯︵ ┻━┻ ['table', 'flip', 'face']
┬─┬ノ(º_ºノ) ['calm', 'face', 'table', 'put', 'down']

$ pow table
POW! Found 2 matches:

(╯°□°）╯︵ ┻━┻ ['table', 'flip', 'face']
┬─┬ノ(º_ºノ) ['calm', 'face', 'table', 'put', 'down']

$ pow -m face
POW! Copied 2 entries to the clipboard:

(╯°□°）╯︵ ┻━┻
┬─┬ノ(º_ºノ)
```

My current entries:
```
$pow ls
POW! 11 entries:

(J °O°)J ['yelling', 'yell', 'holler', 'face']
(•_•)
( •_•)>⌐■-■
(⌐■_■) ['sunglasses', 'csi', 'horatio', 'caine', 'face']
(╯°□°）╯︵ ┻━┻ ['table', 'flip', 'tableflip', 'face']
https://www.youtube.com/watch?v=4F4qzPbcFiA ['its', 'a', 'trap', 'admiral', 'ackbar', 'star', 'wars']
https://youtu.be/RqIArE4Iw4U?t=2m31s ['turn', 'it', 'off', 'han', 'chewie', 'star', 'wars']
¯\_(ツ)_/¯ ['shrug', 'face', 'shruggie', 'guy', 'whatever']
ಠ_ಠ ['disapprove', 'face']
ಥ_ಥ ['crying', 'face']
⊙﹏⊙ ['waaa', 'face']
┬─┬ノ(º_ºノ) ['calm', 'face', 'table', 'put', 'down']
┻━┻ ︵ヽ(`Д´)ﾉ︵ ┻━┻ ['face', 'double', 'table', 'flip']

```

Work in progress, more refinements and features to come. Enjoy!
