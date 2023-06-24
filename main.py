from machine import Pin,SPI
from PiicoDev_TMP117 import PiicoDev_TMP117
import framebuf
import time
import utime
import math
from pitches import *

DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9
width = 128
height = 64
tempSensor = PiicoDev_TMP117()
i = 0

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

class OLED_1inch3(framebuf.FrameBuffer):
    
    def __init__(self):
        self.width = 128
        self.height = 64
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,2000_000)
        self.spi = SPI(1,20000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width // 8)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_HMSB)
        self.init_display()
        
        self.white =   0xffff
        self.balck =   0x0000
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize display"""  
        self.rst(1)
        time.sleep(0.001)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)
        
        self.write_cmd(0xAE)   #turn off OLED display

        self.write_cmd(0x00)   #set lower column address
        self.write_cmd(0x10)   #set higher column address 

        self.write_cmd(0xB0)   #set page address 
      
        self.write_cmd(0xdc)    #et display start line 
        self.write_cmd(0x00) 
        self.write_cmd(0x81)    #contract control 
        self.write_cmd(0x6f)    #128
        self.write_cmd(0x21)    # Set Memory addressing mode (0x20/0x21) #
    
        self.write_cmd(0xa0)    #set segment remap 
        self.write_cmd(0xc0)    #Com scan direction
        self.write_cmd(0xa4)   #Disable Entire Display On (0xA4/0xA5) 

        self.write_cmd(0xa6)    #normal / reverse
        self.write_cmd(0xa8)    #multiplex ratio 
        self.write_cmd(0x3f)    #duty = 1/64
  
        self.write_cmd(0xd3)    #set display offset 
        self.write_cmd(0x60)

        self.write_cmd(0xd5)    #set osc division 
        self.write_cmd(0x41)
    
        self.write_cmd(0xd9)    #set pre-charge period
        self.write_cmd(0x22)   

        self.write_cmd(0xdb)    #set vcomh 
        self.write_cmd(0x35)  
    
        self.write_cmd(0xad)    #set charge pump enable 
        self.write_cmd(0x8a)    #Set DC-DC enable (a=0:disable; a=1:enable)
        self.write_cmd(0XAF)

    def show(self):
        self.write_cmd(0xb0)
        for page in range(0,64):
            self.column = 63 - page              
            self.write_cmd(0x00 + (self.column & 0x0f))
            self.write_cmd(0x10 + (self.column >> 4))
            for num in range(0,16):
                self.write_data(self.buffer[page*16+num])

    class graph2D:
        def __init__(self, originX = 0, originY = height-1, width = width, height = height, minValue=0, maxValue=255, c = 1, bars = False):
            self.minValue = minValue
            self.maxValue = maxValue
            self.originX = originX
            self.originY = originY
            self.width = width
            self.height = height
            self.c = c
            self.m = (1-height)/(maxValue-minValue)
            self.offset = originY-self.m*minValue
            self.bars = bars
            self.data = []

    def updateGraph2D(self, graph, value):
        graph.data.insert(0,value)
        if len(graph.data) > graph.width:
            graph.data.pop()
        x = graph.originX+graph.width-1
        m = graph.c
        for value in graph.data:
            y = round(graph.m*value + graph.offset)
            if graph.bars == True:
                for idx in range(y, graph.originY+1):
                    if x >= graph.originX and x < graph.originX+graph.width and idx <= graph.originY and idx > graph.originY-graph.height:
                        self.pixel(x,idx, m)
            else:
                if x >= graph.originX and x < graph.originX+graph.width and y <= graph.originY and y > graph.originY-graph.height:
                    self.pixel(x,y, m)
            x -= 1

tempC = tempSensor.readTempC() # Celsius
initTemp = tempC
tempC1 = initTemp
OLED = OLED_1inch3()
graph1 = OLED.graph2D(height=44, minValue=18, maxValue=22) # create graph2D objects
xfactor = initTemp -20
buzzer = machine.PWM(machine.Pin(18))
tempUp = 0
tempDn = 0

while (True):
    #OLED = OLED_1inch3()
    OLED.fill(0x0000) 
    OLED.text("Wazza's Thermal",3,10,OLED.white)
    OLED.text("BUSTER Version 2",1,27,OLED.white)
    OLED.text("~ V1.0 15/6/23 ~",1,44,OLED.white)  
    OLED.show()
    time.sleep(2)
        
    OLED.fill(0x0000) 
    keyA = Pin(15,Pin.IN,Pin.PULL_UP)
    keyB = Pin(17,Pin.IN,Pin.PULL_UP)
    
    # Plot
    while(1):
        tempC = tempSensor.readTempC() # Celsius
        newtemp = str(truncate(tempC, 2))+" deg C"
        OLED.fill(0)
        OLED.rect(0,0,128,20,OLED.white)
        OLED.text(newtemp, 25, 6, OLED.white)
        print(str(tempC) + " °C")
        
        # OLED Graph display  
        y = tempC - xfactor
    
        #print(tempC, xfactor, initTemp, y)
    
        if y > 22:
            OLED.text("Temp > 2", 60, 40, 1)
            initTemp = tempC
            tempC1 = initTemp
            xfactor = initTemp -20
            
        elif y < 18:
            OLED.text("Temp < 2", 60, 40, 1)
            initTemp = tempC
            tempC1 = initTemp
            xfactor = initTemp -20
        
        OLED.updateGraph2D(graph1, y)
        OLED.line(0,63,127,63,OLED.white)
        OLED.show()
            
        if tempC1 > tempC:
            tempUp = 0
            tempDn = tempDn + 1
            #print("Temp Lower")
            if tempDn > 3 and i == 19660: # if temp decreases 5 times in a row sound buzzer
                #print("Sound Buzzer")
                buzzer.freq(C4)
                buzzer.duty_u16(3000)  
        elif tempC1 == tempC:
            tempDn = 0
            tempUp = 0
        else:
            tempDn = 0
            tempUp = tempUp + 1
            #print("Temp Higher")
            if tempUp > 3 and i == 19660: # if temp increases 5 times in a row sound buzzer
                #print("Sound Buzzer")
                buzzer.freq(A7)
                buzzer.duty_u16(3000)  
                 
        tempC1 = tempC
        
        if keyA.value() == 0:
                #print("A press - Buzz On")
                i = 19660
                buzzer.freq(A5)
                buzzer.duty_u16(3000)
        if(keyB.value() == 0):
                #print("B press - Buzz Off")
                i = 0
                buzzer.freq(C3)
                buzzer.duty_u16(3000) 
        
        if i > 0:
            OLED.fill_rect(0,20,10,10,OLED.white)
            OLED.show()
                
        time.sleep(0.5)
        buzzer.duty_u16(0)
        time.sleep(0.5)
      
    OLED.fill(0xFFFF)





