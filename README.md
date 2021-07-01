# PYLON_EMU
Python script to emulate the outgoing CAN bus traffic from a Pylontech LFP battery pack (48V)

Useful script to make a hybrid inverter think that your self made battery pack is a Pylontech one. This should allow you to use any battery pack that you have designed with many hybrid inverters which support pylontech LFP batteries.

It has not been tested with an inverter but the information send should be correct.

Modify it at your own needs. I no longer support this since I do not require it any more and can not test it on real hardware.

Of course it requires a raspberry pi (or a linux machine) plus extra hardware to communicate via CAN.

See a short screen capture video showing the function of it. Currently only the keep alive message is being modified every second (incremented by one). The rest of the values are static (but can be modified in the script to be set on-the-fly) https://www.youtube.com/watch?v=CiFts8KZV6k
