import time
from tm1638 import TM1638

# Define GPIO pins
STB = 5
CLK = 6
DIO = 13

# Create a TM1638 instance
tm = TM1638(stb=STB, clk=CLK, dio=DIO)

# Clear the display
tm.clear()

# Counter loop
counter = 0
try:
    while True:
        tm.display_number(counter)
        counter += 1
        if counter > 99999999:  # Reset counter after 8 digits
            counter = 0
except KeyboardInterrupt:
    pass

# Clear the display before exiting
tm.clear()

# Cleanup GPIO
tm.cleanup()
