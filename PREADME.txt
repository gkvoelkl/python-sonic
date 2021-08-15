== python-sonic - Programming Music with Python, Sonic Pi or Supercollider

Python-Sonic is a simple Python interface for Sonic Pi, which is a real
great music software created by Sam Aaron (http://sonic-pi.net).

At the moment Python-Sonic works with Sonic Pi. It is planned, that it
will work with Supercollider, too.

If you like it, use it. If you have some suggestions, tell me
(gkvoelkl@nelson-games.de).

== Installation

* First you need Python 3 (https://www.python.org, ) - Python 3.5 should
work, because it’s the development environment
* Then Sonic Pi (https://sonic-pi.net) - That makes the sound
* Modul python-osc (https://pypi.python.org/pypi/python-osc) -
Connection between Python and Sonic Pi Server
* And this modul python-sonic - simply copy the source

Or try
$ pip install python-sonic
That should work.

== Limitations

* You have to start _Sonic Pi_ first before you can use it with
python-sonic
* Only the notes from C2 to C6

== Changelog

[width="100%",cols="14%,86%",options="header",]
|===
|Version |
|0.2.0 |Some changes for Sonic Pi 2.11. Simpler multi-threading with
decorator _@in_thread_. Messaging with _cue_ and _sync_.

|0.3.0 |OSC Communication

|0.3.1. |Update, sort and duration of samples

|0.3.2. |Restructured

|0.4.0 |Changes communication ports and recording
|===

== Communication

The API _python-sonic_ communications with _Sonic Pi_ over UDP and two
ports. One port is an internal _Sonic Pi_ port and could be changed. +
For older _Sonic Pi_ Version you have to set the ports explicitly
from psonic import *
set_server_parameters('127.0.0.1',4557,4559)
== Examples

Many of the examples are inspired from the help menu in _Sonic Pi_.


+*In[1]:*+
[source, ipython3]
----
from psonic import *
----

The first sound


+*In[2]:*+
[source, ipython3]
----
play(70) #play MIDI note 70
----

Some more notes


+*In[3]:*+
[source, ipython3]
----
play(72)
sleep(1)
play(75)
sleep(1)
play(79) 
----

In more tratitional music notation


+*In[4]:*+
[source, ipython3]
----
play(C5)
sleep(0.5)
play(D5)
sleep(0.5)
play(G5) 
----

Play sharp notes like _F#_ or dimished ones like _Eb_


+*In[5]:*+
[source, ipython3]
----
play(Fs5)
sleep(0.5)
play(Eb5)
----

Play louder (parameter amp) or from a different direction (parameter
pan)


+*In[6]:*+
[source, ipython3]
----
play(72,amp=2)
sleep(0.5)
play(74,pan=-1) #left
----

Different synthesizer sounds


+*In[7]:*+
[source, ipython3]
----
use_synth(SAW)
play(38)
sleep(0.25)
play(50)
sleep(0.5)
use_synth(PROPHET)
play(57)
sleep(0.25)
----

ADSR _(Attack, Decay, Sustain and Release)_ Envelope


+*In[8]:*+
[source, ipython3]
----
play (60, attack=0.5, decay=1, sustain_level=0.4, sustain=2, release=0.5) 
sleep(4)
----

Play some samples


+*In[9]:*+
[source, ipython3]
----
sample(AMBI_LUNAR_LAND, amp=0.5)
----


+*In[10]:*+
[source, ipython3]
----
sample(LOOP_AMEN,pan=-1)
sleep(0.877)
sample(LOOP_AMEN,pan=1)
----


+*In[11]:*+
[source, ipython3]
----
sample(LOOP_AMEN,rate=0.5)
----


+*In[12]:*+
[source, ipython3]
----
sample(LOOP_AMEN,rate=1.5)
----


+*In[13]:*+
[source, ipython3]
----
sample(LOOP_AMEN,rate=-1)#back
----


+*In[14]:*+
[source, ipython3]
----
sample(DRUM_CYMBAL_OPEN,attack=0.01,sustain=0.3,release=0.1)
----


+*In[15]:*+
[source, ipython3]
----
sample(LOOP_AMEN,start=0.5,finish=0.8,rate=-0.2,attack=0.3,release=1)
----

Play some random notes


+*In[16]:*+
[source, ipython3]
----
import random

for i in range(5):
    play(random.randrange(50, 100))
    sleep(0.5)
----


+*In[17]:*+
[source, ipython3]
----
for i in range(3):
    play(random.choice([C5,E5,G5]))
    sleep(1)
----

Sample slicing


+*In[18]:*+
[source, ipython3]
----
from psonic import *

number_of_pieces = 8

for i in range(16):
    s = random.randrange(0,number_of_pieces)/number_of_pieces #sample starts at 0.0 and finishes at 1.0
    f = s + (1.0/number_of_pieces)
    sample(LOOP_AMEN,beat_stretch=2,start=s,finish=f)
    sleep(2.0/number_of_pieces)
----

An infinite loop and if


+*In[18]:*+
[source, ipython3]
----
while True:
  if one_in(2):
    sample(DRUM_HEAVY_KICK)
    sleep(0.5)
  else:
    sample(DRUM_CYMBAL_CLOSED)
    sleep(0.25)
----


+*Out[18]:*+
----

    ---------------------------------------------------------------------------

    KeyboardInterrupt                         Traceback (most recent call last)

    <ipython-input-18-d8759ac2d27e> in <module>()
          5   else:
          6     sample(DRUM_CYMBAL_CLOSED)
    ----> 7     sleep(0.25)
    

    /mnt/jupyter/python-sonic/psonic.py in sleep(duration)
        587     :return:
        588     """
    --> 589     time.sleep(duration)
        590     _debug('sleep', duration)
        591 


    KeyboardInterrupt: 

----

If you want to hear more than one sound at a time, use Threads.


+*In[19]:*+
[source, ipython3]
----
import random
from psonic import *
from threading import Thread

def bass_sound():
    c = chord(E3, MAJOR7)
    while True:
        use_synth(PROPHET)
        play(random.choice(c), release=0.6)
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
----


+*Out[19]:*+
----

    ---------------------------------------------------------------------------

    KeyboardInterrupt                         Traceback (most recent call last)

    <ipython-input-19-5b8671a783d6> in <module>
         22 
         23 while True:
    ---> 24     pass
    

    KeyboardInterrupt: 

----

Every function _bass_sound_ and _snare_sound_ have its own thread. Your
can hear them running.


+*In[1]:*+
[source, ipython3]
----
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
----


+*Out[1]:*+
----
Press Enter to continue... 
''----

To synchronize the thread, so that they play a note at the same time,
you can use _Condition_. One function sends a message with
_condition.notifyAll_ the other waits until the message comes
_condition.wait_.

More simple with decorator __@in_thread__


+*In[ ]:*+
[source, ipython3]
----
from psonic import *
from random import choice

tick = Message()

@in_thread
def random_riff():
    use_synth(PROPHET)
    sc = scale(E3, MINOR)
    while True:
        s = random.choice([0.125,0.25,0.5])
        tick.sync()
        for i in range(8):
            r = random.choice([0.125, 0.25, 1, 2])
            n = random.choice(sc)
            co = random.randint(30,100)
            play(n, release = r, cutoff = co)
            sleep(s)
            
@in_thread
def drums():
    while True:
        tick.cue()
        for i in range(16):
            r = random.randrange(1,10)
            sample(DRUM_BASS_HARD, rate=r)
            sleep(0.125)

random_riff()
drums()

input("Press Enter to continue...")
----


+*Out[ ]:*+
----
Press Enter to continue... 
----


+*In[ ]:*+
[source, ipython3]
----
from psonic import *

tick = Message()

@in_thread
def metronom():
    while True:
        tick.cue()
        sleep(1)
        
@in_thread
def instrument():
    while True:
        tick.sync()
        sample(DRUM_HEAVY_KICK)

metronom()
instrument()

while True:
    pass
----

Play a list of notes


+*In[2]:*+
[source, ipython3]
----
from psonic import *

play ([64, 67, 71], amp = 0.3) 
sleep(1)
play ([E4, G4, B4])
sleep(1)
----

Play chords


+*In[2]:*+
[source, ipython3]
----
play(chord(E4, MINOR)) 
sleep(1)
play(chord(E4, MAJOR))
sleep(1)
play(chord(E4, MINOR7))
sleep(1)
play(chord(E4, DOM7))
sleep(1)
----

Play arpeggios


+*In[3]:*+
[source, ipython3]
----
play_pattern( chord(E4, 'm7')) 
play_pattern_timed( chord(E4, 'm7'), 0.25) 
play_pattern_timed(chord(E4, 'dim'), [0.25, 0.5]) 
----

Play scales


+*In[4]:*+
[source, ipython3]
----
play_pattern_timed(scale(C3, MAJOR), 0.125, release = 0.1) 
play_pattern_timed(scale(C3, MAJOR, num_octaves = 2), 0.125, release = 0.1) 
play_pattern_timed(scale(C3, MAJOR_PENTATONIC, num_octaves = 2), 0.125, release = 0.1)
----

The function _scale_ returns a list with all notes of a scale. So you
can use list methodes or functions. For example to play arpeggios
descending or shuffeld.


+*In[5]:*+
[source, ipython3]
----
import random
from psonic import *

s = scale(C3, MAJOR)
s
----


+*Out[5]:*+
----[48, 50, 52, 53, 55, 57, 59, 60]----


+*In[6]:*+
[source, ipython3]
----
s.reverse()
----


+*In[7]:*+
[source, ipython3]
----

play_pattern_timed(s, 0.125, release = 0.1)
random.shuffle(s)
play_pattern_timed(s, 0.125, release = 0.1)
----

== Live Loop

One of the best in SONIC PI is the _Live Loop_. While a loop is playing
music you can change it and hear the change. Let’s try it in Python,
too.


+*In[5]:*+
[source, ipython3]
----
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
----


+*Out[5]:*+
----
Press Enter to continue...Y
'Y'----

Now change the function _my_loop_ und you can hear it.


+*In[6]:*+
[source, ipython3]
----
def my_loop():
  use_synth(TB303)
  play (60, release= 0.3)
  sleep (0.25)
----


+*In[7]:*+
[source, ipython3]
----
def my_loop():
  use_synth(TB303)
  play (chord(E3, MINOR), release= 0.3)
  sleep(0.5)
----


+*In[8]:*+
[source, ipython3]
----
def my_loop():
    use_synth(TB303)
    sample(DRUM_BASS_HARD, rate = random.uniform(0.5, 2))
    play(random.choice(chord(E3, MINOR)), release= 0.2, cutoff=random.randrange(60, 130))
    sleep(0.25)
----

To stop the sound you have to end the kernel. In IPython with Kernel –>
Restart

Now with two live loops which are synch.


+*In[10]:*+
[source, ipython3]
----
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
----


+*Out[10]:*+
----
Press Enter to continue...y
'y'----


+*In[11]:*+
[source, ipython3]
----
def loop_foo():
  play (A4, release = 0.5)
  sleep (0.5)
----


+*In[14]:*+
[source, ipython3]
----
def loop_bar():
  sample (DRUM_HEAVY_KICK)
  sleep (0.125)
----

If would be nice if we can stop the loop with a simple command. With
stop event it works.


+*In[1]:*+
[source, ipython3]
----
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
----


+*Out[1]:*+
----
Press Enter to continue...y
'y'----


+*In[3]:*+
[source, ipython3]
----
stop_event.set()
----

More complex live loops


+*In[4]:*+
[source, ipython3]
----
sc = Ring(scale(E3, MINOR_PENTATONIC))

def loop_foo():
  play (next(sc), release= 0.1)
  sleep (0.125)

sc2 = Ring(scale(E3,MINOR_PENTATONIC,num_octaves=2))
           
def loop_bar():
  use_synth(DSAW)
  play (next(sc2), release= 0.25)
  sleep (0.25)
----

Now a simple structure with four live loops


+*In[11]:*+
[source, ipython3]
----
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
----


+*Out[11]:*+
----
Press Enter to continue...y
'y'----

After starting the loops you can change them


+*In[12]:*+
[source, ipython3]
----
def live_1():
    sample(BD_HAUS,amp=2)
    sleep(0.5)
    pass
----


+*In[7]:*+
[source, ipython3]
----
def live_2():
    #sample(AMBI_CHOIR, rate=0.4)
    #sleep(1)
    pass
----


+*In[14]:*+
[source, ipython3]
----
def live_3():
    use_synth(TB303)
    play(E2, release=4,cutoff=120,cutoff_attack=1)
    sleep(4)
----


+*In[13]:*+
[source, ipython3]
----
def live_4():
    notes = scale(E3, MINOR_PENTATONIC, num_octaves=2)
    for i in range(8):
        play(random.choice(notes),release=0.1,amp=1.5)
        sleep(0.125)
----

And stop.


+*In[15]:*+
[source, ipython3]
----
stop_event.set()
----

== Creating Sound


+*In[4]:*+
[source, ipython3]
----
from psonic import *

synth(SINE, note=D4)
synth(SQUARE, note=D4)
synth(TRI, note=D4, amp=0.4)
----


+*In[5]:*+
[source, ipython3]
----
detune = 0.7
synth(SQUARE, note = E4)
synth(SQUARE, note = E4+detune)
----


+*In[12]:*+
[source, ipython3]
----
detune=0.1 # Amplitude shaping
synth(SQUARE, note = E2, release = 2)
synth(SQUARE, note = E2+detune, amp =  2, release = 2)
synth(GNOISE, release = 2, amp = 1, cutoff = 60)
synth(GNOISE, release = 0.5, amp = 1, cutoff = 100)
synth(NOISE, release = 0.2, amp = 1, cutoff = 90)
----

== Next Step

Using FX _Not implemented yet_


+*In[2]:*+
[source, ipython3]
----
from psonic import *

with Fx(SLICER):
    synth(PROPHET,note=E2,release=8,cutoff=80)
    synth(PROPHET,note=E2+4,release=8,cutoff=80)
----


+*In[3]:*+
[source, ipython3]
----
with Fx(SLICER, phase=0.125, probability=0.6,prob_pos=1):
    synth(TB303, note=E2, cutoff_attack=8, release=8)
    synth(TB303, note=E3, cutoff_attack=4, release=8)
    synth(TB303, note=E4, cutoff_attack=2, release=8)
----

== OSC Communication (Sonic Pi Ver. 3.x or better)

In Sonic Pi version 3 or better you can work with messages.


+*In[1]:*+
[source, ipython3]
----
from psonic import *
----

First you need a programm in the Sonic Pi server that receives messages.
You can write it in th GUI or send one with Python.


+*In[2]:*+
[source, ipython3]
----
run("""live_loop :foo do
  use_real_time
  a, b, c = sync "/osc*/trigger/prophet"
  synth :prophet, note: a, cutoff: b, sustain: c
end """)
----

Now send a message to Sonic Pi.


+*In[3]:*+
[source, ipython3]
----
send_message('/trigger/prophet', 70, 100, 8)
----


+*In[4]:*+
[source, ipython3]
----
stop()
----

== Recording

With python-sonic you can record wave files.


+*In[1]:*+
[source, ipython3]
----
from psonic import *
----


+*In[5]:*+
[source, ipython3]
----
# start recording
start_recording()

play(chord(E4, MINOR)) 
sleep(1)
play(chord(E4, MAJOR))
sleep(1)
play(chord(E4, MINOR7))
sleep(1)
play(chord(E4, DOM7))
sleep(1)
----


+*In[6]:*+
[source, ipython3]
----
# stop recording
stop_recording
----


+*Out[6]:*+
----<function psonic.psonic.stop_recording()>----


+*In[7]:*+
[source, ipython3]
----
# save file
save_recording('/Volumes/jupyter/python-sonic/test.wav')
----

== More Examples


+*In[1]:*+
[source, ipython3]
----
from psonic import *
----


+*In[ ]:*+
[source, ipython3]
----
#Inspired by Steve Reich Clapping Music

clapping = [1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0]

for i in range(13):
    for j in range(4):
        for k in range(12): 
          if clapping[k] ==1 : sample(DRUM_SNARE_SOFT,pan=-0.5)
          if clapping[(i+k)%12] == 1: sample(DRUM_HEAVY_KICK,pan=0.5)
          sleep (0.25)
----

== Projects that use Python-Sonic

Raspberry Pi sonic-track.py a Sonic-pi Motion Track Demo
https://github.com/pageauc/sonic-track

== Sources

Joe Armstrong: Connecting Erlang to the Sonic Pi
http://joearms.github.io/2015/01/05/Connecting-Erlang-to-Sonic-Pi.html

Joe Armstrong: Controlling Sound with OSC Messages
http://joearms.github.io/2016/01/29/Controlling-Sound-with-OSC-Messages.html

..
