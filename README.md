# python-sonic - Programming Music with Python, Sonic Pi or Supercollider

Python-Sonic is a simple Python interface for Sonic Pi, which is a real great music software created by Sam Aaron (http://sonic-pi.net). 

At the moment Python-Sonic is in __pre-pre-alpha__ status. It is planned, that it will work with Supercollider, too.

If you like it, use it. If you have some suggestions, tell me (gkvoelkl@nelson-games.de).

But no debugging now or help on how to install it on your system.  


## Installation

* First you need Python 3 (https://www.python.org, ) - Python 3.4 should work, because it's the development environment
* Then Sonic Pi (https://sonic-pi.net) - That makes the sound
* Modul python-osc (https://pypi.python.org/pypi/python-osc) - Connection between Python and Sonic Pi Server
* And this modul python-sonic - simply copy the source, no setup available at the moment

## Limitations

* You have to start _Sonic Pi_ first before you can use it with python-sonic
* Only the notes from C5 to C6

## Examples

Many of the examples are inspired from the help menu in *Sonic Pi*.


```python
from psonic import *
```

The first sound


```python
play(70) #play MIDI note 70
```

Some more notes


```python
play(72)
sleep(1)
play(75)
sleep(1)
play(79) 
```

In more tratitional music notation


```python
play(C5)
sleep(0.5)
play(D5)
sleep(0.5)
play(G5) 
```

Play sharp notes like *F#* or dimished ones like *Eb*


```python
play(Fs5)
sleep(0.5)
play(Eb5)
```

Play louder (parameter amp) or from a different direction (parameter pan)


```python
play(72,amp=2)
sleep(0.5)
play(74,pan=-1) #left
```

Different synthesizer sounds


```python
use_synth(SAW)
play(38)
sleep(0.25)
play(50)
sleep(0.5)
use_synth(PROPHET)
play(57)
sleep(0.25)
```

## More Informations

### Sonic Pi

..

### OSC

..

### MIDI

..


```python

```
