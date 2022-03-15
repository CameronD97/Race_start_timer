from machine import Pin, Timer
import _thread
import time
import gc #garbage collector

#define variables
elapsed = int(-330) #the elapsed time from the start of the race. It starts at -5minutes and 30seconds
display_time = str(1531) #the time to write to the display. This must be a 4 character string. This is using a global variable which is a slightly messy way of doing it
restart_thread_counter = int(1000)

#define pins
led = Pin(25, Pin.OUT) #the LED on the board is on pin 25. Needs to be changed to the relay pin
relay = Pin(0, Pin.OUT) #the GPIO pin to connect the relay for the hooter to
#defining the pins used for the display
display_1 = Pin(1, Pin.OUT)
display_2 = Pin(2, Pin.OUT)
display_3 = Pin(3, Pin.OUT)
display_4 = Pin(4, Pin.OUT)
display_5 = Pin(5, Pin.OUT)
display_7 = Pin(6, Pin.OUT)
display_10 = Pin(7, Pin.OUT)
display_11 = Pin(8, Pin.OUT)

segments = [display_1 , display_2 , display_3 , display_4 , display_5 , display_7 , display_10 , display_11]

display_12 = Pin(9, Pin.OUT)
display_9 = Pin(10, Pin.OUT)
display_8 = Pin(11, Pin.OUT)
display_6 = Pin(13, Pin.OUT)

digits = [display_12 , display_9 , display_8 , display_6]
for k in range (0,3):
    digits[k].value(1) #set all the multiplexer pins to be high. They are pulled low to address the digit

sLock = _thread.allocate_lock() #a thread lock to stop issues where both threads try to access the same variable at once

#define functions

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
    
def display_write():
    global display_time
    global segments
    global digits
    truths = [[1,1,0,1,0,1,1,1],[0,0,0,1,0,1,0,0],[1,1,0,0,1,1,0,1],[0,1,0,1,1,1,0,1],[0,0,0,1,1,1,1,0],[0,1,0,1,1,0,1,1],[1,1,0,1,1,0,1,1],[0,0,0,1,0,1,0,1],[1,1,0,1,1,1,1,1],[0,0,0,1,1,1,1,1]]  #the truth table for  all the pin values to give each digit
    
    while True:
        #sLock.acquire()
        #global display_time
        for i in range (0,4):
            digits[i].value(0)
            sLock.acquire()
            digit = int(display_time[i])
            #print(display_time)
            sLock.release()
            #print(i)
            #print(digit)
            for j in range (0,8):
                segments[j].value((truths[digit][j]))
            time.sleep(0.0015)
            for j in range (0,8):
                segments[j].value(0)
            digits[i].value(1)
            gc.collect()
        #sLock.release()
            
        #print(display_time)

        
    

tim = Timer()#the timer for the main clock
tom = Timer()#the timer for the toot length

def tick(timer):#the periodic timer that increments the elapsed time by 1 second, prints the time, and checks whether a sound signal is needed
    #sLock.acquire()
    global elapsed
    global display_time
    elapsed += 1
    
    #micropython has no zfill(). This ensures the minutes ad seconds are not one digits by adding preceding 0s. This programm isn't designed to work after 99 minutes
    mint = str(abs(elapsed)//60) #mint is minutes because min is already a function
    if len(mint) == 1:
        mint = "0" + mint
        
    sec = str(abs(elapsed)%60)
    if len(sec) == 1:
        sec = "0" + sec
    
    sLock.acquire()
    display_time = mint + sec
    sLock.release()
    
    print(mint, ':' , sec)
    #print(display_time)
    print(gc.mem_free())
    gc.collect()
    print(gc.mem_free())
      
    if elapsed == -300:
        toot_short()
    elif elapsed == -240:
        toot_short()
    elif elapsed == -60:
        toot_long()
    elif elapsed == 0:
        toot_short()
    #sLock.release()

#a separate thread on the other core to run the 7 seg display. 
_thread.start_new_thread(display_write, ())

tim.init(freq=1, mode=Timer.PERIODIC, callback=tick) #calls the periodic timer with a frequency of 1Hz

#hardware interrupt(rising edge on a pin) to end the timer Timer.deinit(tim)
#hardware interrupt to take you back to the beginning of a while loop, reset elapsed, and start again

