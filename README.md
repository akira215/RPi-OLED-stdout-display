# Raspberry Pi OLED stdout logger

This Python script shall be started at the boot of the RPI. It will monitor 2 RAM files (`/dev/shm/line1` & `/dev/shm/line1`) and display their content @ $pollinterval.

If either of 1 line content is `cls`, screen will be cleared.

A screensaver is triggered if $screensaver_delay is overpasss without any changes in `line1` and `line2` files


## Installation

1. On RPi enable i2c

    In file `/boot/config.txt` add or modify the line

    ```
    dtparam=i2c_arm=on
    ```

    Reboot and check:

    ```
    echo 'i2c-dev' | sudo tee /etc/modules-load.d/i2c-dev.conf
    sudo i2cdetect -y 1
    ```

2. Install Python and tools

    Install Python and tools from raspbian repos
    ```
    sudo apt install -y python3-dev i2c-tools python3-pil python3-pip python3-setuptools \
    python3-rpi.gpio python3-ftdi rpi.gpio-common python3-luma.led-matrix python3-sysv-ipc \
    python3-usb python3-typing-extensions
    ```

    Install Adafruit_Python_SSD1306 library (driver for OLED)

    ```
    sudo pip3 install --break-system-packages adafruit-circuitpython-ssd1306
    ```

3. Python script

    put `oled.py` script wherever you want
