import spidev
import RPi.GPIO as GPIO
import time
from scipy.stats import zscore

class TemperatureSensor:
    # Constants for the voltage divider
    V_SUPPLY = 5  # Supply Voltage
    R_DIVIDER = 10000.0  # Resistance of the fixed resistor in ohms (10 kOhms)

    # NTC voltage table (for temperatures 0 to 100)
    ntc_voltage_table = {
    0: 1.148, 1: 1.134, 2: 1.120, 3: 1.106, 4: 1.091, 5: 1.076, 6: 1.061, 7: 1.046, 8: 1.030, 9: 1.014,
    10: 0.998, 11: 0.982, 12: 0.966, 13: 0.950, 14: 0.933, 15: 0.917, 16: 0.900, 17: 0.883, 18: 0.867, 19: 0.850,
    20: 0.833, 21: 0.816, 22: 0.800, 23: 0.783, 24: 0.767, 25: 0.750, 26: 0.734, 27: 0.717, 28: 0.701, 29: 0.685,
    30: 0.669, 31: 0.654, 32: 0.638, 33: 0.623, 34: 0.608, 35: 0.593, 36: 0.578, 37: 0.563, 38: 0.549, 39: 0.535,
    40: 0.521, 41: 0.508, 42: 0.494, 43: 0.481, 44: 0.469, 45: 0.456, 46: 0.444, 47: 0.432, 48: 0.420, 49: 0.408,
    50: 0.397, 51: 0.386, 52: 0.376, 53: 0.365, 54: 0.355, 55: 0.345, 56: 0.335, 57: 0.326, 58: 0.317, 59: 0.308,
    60: 0.299, 61: 0.290, 62: 0.282, 63: 0.274, 64: 0.266, 65: 0.259, 66: 0.251, 67: 0.244, 68: 0.237, 69: 0.230,
    70: 0.224, 71: 0.217, 72: 0.211, 73: 0.205, 74: 0.199, 75: 0.193, 76: 0.188, 77: 0.182, 78: 0.177, 79: 0.172,
    80: 0.167, 81: 0.163, 82: 0.158, 83: 0.154, 84: 0.149, 85: 0.145, 86: 0.141, 87: 0.137, 88: 0.133, 89: 0.129,
    90: 0.126, 91: 0.122, 92: 0.119, 93: 0.116, 94: 0.112, 95: 0.109, 96: 0.106, 97: 0.104, 98: 0.101, 99: 0.098,
    100: 0.095
    }

    def __init__(self):
        # Setup SPI
        self.spi = spidev.SpiDev()
        self.spi.open(5, 0)  # Use SPI port 1, device 0 (CE0)
        self.spi.max_speed_hz = 500000  # 1 MHz 
        self.spi.mode = 0b01

        # Define the chip select pin in BCM numbering system
        self.CS_PIN = 12  # BCM GPIO16
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.CS_PIN, GPIO.OUT)
        GPIO.output(self.CS_PIN, GPIO.HIGH)

        # AD7928 configuration
        self.AD7928_WRITE_CR = 0x0800  # Write to control register command
        self.AD7928_CODING = 0x0001    # Straight binary coding
        self.AD7928_PM_MODE_OPS = 0x0030  # Normal operation mode
        self.AD7928_SEQUENCE_OFF = 0x0000  # Sequence function off
        self.CHANNEL = 6  # Select channel 4

        # Initialize AD7928
        command = self.AD7928_WRITE_CR | (self.CHANNEL << 6) | self.AD7928_CODING | self.AD7928_PM_MODE_OPS | self.AD7928_SEQUENCE_OFF
        command <<= 4  # Shift to fit AD7928 format
        tx_buf = [command >> 8, command & 0xFF]

        # Send configuration command to AD7928
        GPIO.output(self.CS_PIN, GPIO.LOW)  # Select device
        self.spi.xfer2(tx_buf)
        GPIO.output(self.CS_PIN, GPIO.HIGH)  # Deselect device

        # Wait for AD7928 to stabilize
        time.sleep(0.01)

    def read_adc(self, channel):
        # Ensure the channel is within the valid range
        assert 0 <= channel <= 7, "Channel must be 0-7."

        # Build command for the ADC
        command = (self.AD7928_WRITE_CR | (channel << 6) | self.AD7928_SEQUENCE_OFF | self.AD7928_CODING | self.AD7928_PM_MODE_OPS) << 4
        tx_buf = [command >> 8, command & 0xFF]

        # Select device
        GPIO.output(self.CS_PIN, GPIO.LOW)

        # Send command and receive data
        rx_buf = self.spi.xfer2(tx_buf + [0x00, 0x00])

        # Deselect device
        GPIO.output(self.CS_PIN, GPIO.HIGH)

        # Combine received bytes to get the result
        result = ((rx_buf[0] & 0x0F) << 8) | rx_buf[1]
        return result

    def adc_value_to_voltage(self, adc_value):
        v_thermistor = (adc_value * self.V_SUPPLY) / 4095.0
        return v_thermistor

    def get_temperature_from_voltage(self, voltage):
        closest_voltage = min(self.ntc_voltage_table.keys(), key=lambda k: abs(self.ntc_voltage_table[k] - voltage))
        return closest_voltage

    def read_temperature(self):
        # 收集多个温度读取值样本
        num_samples = 100   #!!!!!!!改这里！！！！！！
        samples = [self.read_adc(6) for _ in range(num_samples)]

        # 计算z-score
        z_scores = zscore(samples) if len(samples) > 1 else [0] * len(samples)

        # 过滤掉异常值
        filtered_samples = [val for val, z in zip(samples, z_scores) if abs(z) < 3]

        # 计算过滤后的平均值
        if filtered_samples:
            filtered_mean = sum(filtered_samples) / len(filtered_samples)
        else:
            filtered_mean = sum(samples) / len(samples)  # 如果所有样本都被过滤掉，则使用原始平均值

        # 将过滤后的平均值转换为温度
        temperature = self.adc_value_to_voltage(filtered_mean)
        temperature = self.get_temperature_from_voltage(temperature)

        return temperature

    def cleanup(self):
        self.spi.close()  # Close the SPI connection
        GPIO.cleanup()  # Clean up GPIO

# Main loop to read the ADC value, calculate resistance, and estimate temperature
if __name__ == "__main__":
    try:
        sensor = TemperatureSensor()
        while True:
            temperature = sensor.read_temperature()
            print(f"Estimated Temperature: {temperature}°C")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exiting the program.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sensor.cleanup()
