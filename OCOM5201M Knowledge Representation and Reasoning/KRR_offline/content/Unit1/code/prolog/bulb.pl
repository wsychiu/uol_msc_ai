

switchOn :- harryAlone, not(harrySwitchedOff).

powerOK :- tv.

bulbDead :- not(lampLit), switchOn, powerOK.

tv.

harrySwitchedOff :- fail.

harryAlone.

lampLit :- fail.
