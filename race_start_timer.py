from machine import Pin, Timer
#import time

#some definitions
elapsed = int(-330) #the elapsed time from the start of the race. It starts at -5minutes and 30seconds
led = Pin(25, Pin.OUT) #the LED on the board is on pin 25. Needs to be changed to the relay pin

#a function to take in the time and display it on the 7 seg display

def stop(timer):
    led.value(0)
    pass
    #Timer.deinit(t)

def toot_long():
    print('Toooooot')
    led.value(1)
    #time.sleep(1.5)
    #led.value(0)
    tom.init(mode=Timer.ONE_SHOT, period=1500, callback=stop) #this is better than using time.sleep because it means other stuff can carry on while the hooter is on
    
def toot_short():
    print('toot')
    led.value(1)
    #time.sleep(0.5)
    #led.value(0)
    tom.init(mode=Timer.ONE_SHOT, period=500, callback=stop)
    

tim = Timer()#the timer for the main clock
tom = Timer()#the timer for the toot length

def tick(timer):#the periodic timer that increments the elapsed time by 1 second, prints the time, and checks whether a sound signal is needed
    global elapsed
    elapsed += 1
    print(abs(elapsed)//60, ':', abs(elapsed)%60) #Prints the absolute elapsed time in minuets and seconds. Needs to be changed to pass this to the display function
    if elapsed == -300:
        toot_short()
    elif elapsed == -240:
        toot_short()
    elif elapsed == -60:
        toot_long()
    elif elapsed == 0:
        toot_short()
    
#a separate thread on the other core to run the 7 seg display. 

tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)
 #calls the periodic timer with a frequency of 1Hz

#hardware interrupt(rising edge on a pin) to end the timer Timer.deinit(tim)
#hardware interrupt to take you back to the beginning of a while loop, reset elapsed, and start again

