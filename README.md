
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
* Only the notes from C2 to C6

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

If you want to hear more than one sound at a time, use Threads.


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

Every function *bass_sound* and *snare_sound* have its own thread. Your can hear them running.


```python
from psonic import *
from threading import Thread, Condition
from random import choice

def random_riff(condition):
    use_synth(PROPHET)
    sc = scale(E3, MINOR)
    while True:
        s = random.choice([0.125,0.25,0.5])
        with condition:
            condition.wait() #Wait for message
        for i in range(8):
            r = random.choice([0.125, 0.25, 1, 2])
            n = random.choice(sc)
            co = random.randint(30,100)
            play(n, release = r, cutoff = co)
            sleep(s)

def drums(condition):
    while True:
        with condition:
            condition.notifyAll() #Message to threads
        for i in range(16):
            r = random.randrange(1,10)
            sample(DRUM_BASS_HARD, rate=r)
            sleep(0.125)

condition = Condition()
random_riff_thread = Thread(name='consumer1', target=random_riff, args=(condition,))
drums_thread = Thread(name='producer', target=drums, args=(condition,))

random_riff_thread.start()
drums_thread.start()

input("Press Enter to continue...")
```

To synchronize the thread, so that they play a note at the same time, you can use *Condition*. One function sends a message with *condition.notifyAll* the other waits until the message comes *condition.wait*.

Play a list of notes


```python
from psonic import *

play ([64, 67, 71], amp = 0.3) 
sleep(1)
play ([E4, G4, B4])
sleep(1)
```

Play chords


```python
play(chord(E4, MINOR)) 
sleep(1)
play(chord(E4, MAJOR))
sleep(1)
play(chord(E4, MINOR7))
sleep(1)
play(chord(E4, DOM7))
sleep(1)
```

Play arpeggios


```python
play_pattern( chord(E4, 'm7')) 
play_pattern_timed( chord(E4, 'm7'), 0.25) 
play_pattern_timed(chord(E4, 'dim'), [0.25, 0.5]) 
```

Play scales


```python
play_pattern_timed(scale(C3, MAJOR), 0.125, release = 0.1) 
play_pattern_timed(scale(C3, MAJOR, num_octaves = 2), 0.125, release = 0.1) 
play_pattern_timed(scale(C3, MAJOR_PENTATONIC, num_octaves = 2), 0.125, release = 0.1)
```

### Live Loop

One of the best in SONIC PI is the _Live Loop_. While a loop is playing music you can change it and hear the change. Let's try it in Python, too.


```python
from psonic import *
from threading import Thread

def my_loop():
  play(60)
  sleep(1)

def looper():
  while True:
    my_loop()

looper_thread = Thread(name='looper', target=looper)

looper_thread.start()

input("Press Enter to continue...")
```

    Press Enter to continue...y





    'y'



Now change the function *my_loop* und you can hear it.


```python
def my_loop():
  use_synth(TB303)
  play (60, release= 0.3)
  sleep (0.25)
```


```python
def my_loop():
  use_synth(TB303)
  play (chord(E3, MINOR), release= 0.3)
  sleep(0.5)
```


```python
def my_loop():
    use_synth(TB303)
    sample(DRUM_BASS_HARD, rate = random.uniform(0.5, 2))
    play(random.choice(chord(E3, MINOR)), release= 0.2, cutoff=random.randrange(60, 130))
    sleep(0.25)
```

To stop the sound you have to end the kernel. In IPython with Kernel --> Restart

Now with two live loops which are synch.


```python
from psonic import *
from threading import Thread, Condition
from random import choice

def loop_foo():
  play (E4, release = 0.5)
  sleep (0.5)


def loop_bar():
  sample (DRUM_SNARE_SOFT)
  sleep (1)
    

def live_loop_1(condition):
    while True:
        with condition:
            condition.notifyAll() #Message to threads
        loop_foo()
            
def live_loop_2(condition):
    while True:
        with condition:
            condition.wait() #Wait for message
        loop_bar()

condition = Condition()
live_thread_1 = Thread(name='producer', target=live_loop_1, args=(condition,))
live_thread_2 = Thread(name='consumer1', target=live_loop_2, args=(condition,))

live_thread_1.start()
live_thread_2.start()

input("Press Enter to continue...")
```

    Press Enter to continue...y





    'y'




```python
def loop_foo():
  play (A4, release = 0.5)
  sleep (0.5)
```


```python
def loop_bar():
  sample (DRUM_HEAVY_KICK)
  sleep (0.125)
```

If would be nice if we can stop the loop with a simple command. With stop event it works.


```python
from psonic import *
from threading import Thread, Condition, Event

def loop_foo():
  play (E4, release = 0.5)
  sleep (0.5)


def loop_bar():
  sample (DRUM_SNARE_SOFT)
  sleep (1)
    

def live_loop_1(condition,stop_event):
    while not stop_event.is_set():
        with condition:
            condition.notifyAll() #Message to threads
        loop_foo()
            
def live_loop_2(condition,stop_event):
    while not stop_event.is_set():
        with condition:
            condition.wait() #Wait for message
        loop_bar()



condition = Condition()
stop_event = Event()
live_thread_1 = Thread(name='producer', target=live_loop_1, args=(condition,stop_event))
live_thread_2 = Thread(name='consumer1', target=live_loop_2, args=(condition,stop_event))


live_thread_1.start()
live_thread_2.start()

input("Press Enter to continue...")
```

    Press Enter to continue...y





    'y'




```python
stop_event.set()
```

More complex live loops


```python
sc = Ring(scale(E3, MINOR_PENTATONIC))

def loop_foo():
  play (next(sc), release= 0.1)
  sleep (0.125)

sc2 = Ring(scale(E3,MINOR_PENTATONIC,num_octaves=2))
           
def loop_bar():
  use_synth(DSAW)
  play (next(sc2), release= 0.25)
  sleep (0.25)
```

Now a simple structure with four live loops


```python
import random
from psonic import *
from threading import Thread, Condition, Event

def live_1():
    pass

def live_2():
    pass
    
def live_3():
    pass

def live_4():
    pass

def live_loop_1(condition,stop_event):
    while not stop_event.is_set():
        with condition:
            condition.notifyAll() #Message to threads
        live_1()
            
def live_loop_2(condition,stop_event):
    while not stop_event.is_set():
        with condition:
            condition.wait() #Wait for message
        live_2()

def live_loop_3(condition,stop_event):
    while not stop_event.is_set():
        with condition:
            condition.wait() #Wait for message
        live_3()

def live_loop_4(condition,stop_event):
    while not stop_event.is_set():
        with condition:
            condition.wait() #Wait for message
        live_4()
        
condition = Condition()
stop_event = Event()
live_thread_1 = Thread(name='producer', target=live_loop_1, args=(condition,stop_event))
live_thread_2 = Thread(name='consumer1', target=live_loop_2, args=(condition,stop_event))
live_thread_3 = Thread(name='consumer2', target=live_loop_3, args=(condition,stop_event))
live_thread_4 = Thread(name='consumer3', target=live_loop_3, args=(condition,stop_event))

live_thread_1.start()
live_thread_2.start()
live_thread_3.start()
live_thread_4.start()

input("Press Enter to continue...")
```

    Press Enter to continue...y





    'y'



After starting the loops you can change them


```python
def live_1():
    sample(BD_HAUS,amp=2)
    sleep(0.5)
    pass
```


```python
def live_2():
    #sample(AMBI_CHOIR, rate=0.4)
    #sleep(1)
    pass
```


```python
def live_3():
    use_synth(TB303)
    play(E2, release=4,cutoff=120,cutoff_attack=1)
    sleep(4)
```


```python
def live_4():
    notes = scale(E3, MINOR_PENTATONIC, num_octaves=2)
    for i in range(8):
        play(random.choice(notes),release=0.1,amp=1.5)
        sleep(0.125)
```

And stop.


```python
stop_event.set()
```

## More Examples


```python
from psonic import *
```


```python
#Inspired by Steve Reich Clapping Music

clapping = [1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0]

for i in range(13):
    for j in range(4):
        for k in range(12): 
          if clapping[k] ==1 : sample(DRUM_SNARE_SOFT,pan=-0.5)
          if clapping[(i+k)%12] == 1: sample(DRUM_HEAVY_KICK,pan=0.5)
          sleep (0.25)
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
