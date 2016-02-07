
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
* Only the notes from C3 to C6

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

ADSR *(Attack, Decay, Sustain and Release)* Envelope


```python
play (60, attack=0.5, decay=1, sustain_level=0.4, sustain=2, release=0.5) 
sleep(4)
```

Play some samples


```python
sample(AMBI_LUNAR_LAND, amp=0.5)
```


```python
sample(LOOP_AMEN,pan=-1)
sleep(0.877)
sample(LOOP_AMEN,pan=1)
```


```python
sample(LOOP_AMEN,rate=0.5)
```


```python
sample(LOOP_AMEN,rate=1.5)
```


```python
sample(LOOP_AMEN,rate=-1)#back
```


```python
sample(DRUM_CYMBAL_OPEN,attack=0.01,sustain=0.3,release=0.1)
```


```python
sample(LOOP_AMEN,start=0.5,finish=0.8,rate=-0.2,attack=0.3,release=1)
```

Play some random notes


```python
import random

for i in range(5):
    play(random.randrange(50, 100))
    sleep(0.5)
```


```python
for i in range(3):
    play(random.choice([C5,E5,G5]))
    sleep(1)
```

An infinite loop and if


```python
while True:
  if one_in(2):
    sample(DRUM_HEAVY_KICK)
    sleep(0.5)
  else:
    sample(DRUM_CYMBAL_CLOSED)
    sleep(0.25)
```

More than one sound - threading


```python
from psonic import *
from threading import Thread

def bass_sound():
    c = Chord(E3, M7)
    while True:
        use_synth(PROPHET)
        play(c.choose(), release=0.6)
        sleep(0.5)

def snare_sound():
    while True:
        sample(ELEC_SNARE)
        sleep(1)

bass_thread = Thread(target=bass_sound)
snare_thread = Thread(target=snare_sound)

bass_thread.start()
snare_thread.start()

while True:
    pass
```

## More Informations

### Sonic Pi

..

### OSC

..

### MIDI

..

## Sources

Joe Armstrong: Connecting Erlang to the Sonic Pi http://joearms.github.io/2015/01/05/Connecting-Erlang-to-Sonic-Pi.html

Joe Armstrong: Controlling Sound with OSC Messages http://joearms.github.io/2016/01/29/Controlling-Sound-with-OSC-Messages.html

..
