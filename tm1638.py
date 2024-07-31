import RPi.GPIO as GPIO
import time

class TM1638:
    def __init__(self, stb, clk, dio):
        self.stb = stb
        self.clk = clk
        self.dio = dio

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.stb, GPIO.OUT)
        GPIO.setup(self.clk, GPIO.OUT)
        GPIO.setup(self.dio, GPIO.OUT)

        self.send_command(0x8F)  # Activate and set brightness

    def send_command(self, cmd):
        GPIO.output(self.stb, GPIO.LOW)
        self.send(cmd)
        GPIO.output(self.stb, GPIO.HIGH)

    def send(self, data):
        for _ in range(8):
            GPIO.output(self.clk, GPIO.LOW)
            GPIO.output(self.dio, GPIO.HIGH if data & 0x01 else GPIO.LOW)
            data >>= 1
            GPIO.output(self.clk, GPIO.HIGH)

    def write(self, data):
        self.send_command(0x40)  # Set auto-increment mode
        GPIO.output(self.stb, GPIO.LOW)
        self.send(0xC0)  # Set starting address to 0xC0
        for byte in data:
            self.send(byte)
        GPIO.output(self.stb, GPIO.HIGH)

    def clear(self):
        self.write([0x00] * 16)

    def display_number(self, number, zero_pad=True):
        # Convert number to a string
        str_number = str(number)
        # Pad with zeros or spaces
        if zero_pad:
            str_number = str_number.zfill(8)
        else:
            str_number = str_number.rjust(8)
        # Create segment data for each digit
        segments = [digit_to_segment[int(digit)] if digit.isdigit() else 0x00 for digit in str_number]
        # Interleave segments with 0x00 for dots
        interleaved_segments = []
        for segment in segments:
            interleaved_segments.append(segment)
            interleaved_segments.append(0x00)  # Assuming no dots, we append 0x00 for the dot control
        # Write to display
        self.write(interleaved_segments)

    def cleanup(self):
        GPIO.cleanup()

# Define digit to segment mapping
digit_to_segment = {
    0: 0x3F,  # 0
    1: 0x06,  # 1
    2: 0x5B,  # 2
    3: 0x4F,  # 3
    4: 0x66,  # 4
    5: 0x6D,  # 5
    6: 0x7D,  # 6
    7: 0x07,  # 7
    8: 0x7F,  # 8
    9: 0x6F,  # 9
}