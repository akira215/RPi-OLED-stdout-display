# Raspberry Pi OLED stdout logger

This Python script shall be started at the boot of the RPI. It will monitor 2 RAM files (`/dev/shm/line1` & `/dev/shm/line2`) and display their content @ $pollinterval.

If either of 1 line content is `cls`, screen will be cleared.

A screensaver is triggered if $screensaver_delay is overpasss without any changes in `line1` and `line2` files

## Wiring

|OLED | RPi   | Pin |
|:---:|:-----:|:---:|
|Vcc  | 3.3V  | 1   |
|SDA  | GPIO2 | 3   |
|SCK  | GPIO3 | 5   |
|GND  | GND   | 6   |

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

4. Test

    Check that `countdown.sh` has exe permission `chmod 777 countdown.sh`
    Run `python oled.py`. 
    In a separate terminal, run `./countdown.sh`
    
    You should see the countdown on the OLED screen connected to RPi

## Install a service to start up at boot

Create a symlink to the service file so that systemd will know about it

```
sudo ln -sv /home/akira/docker/display/oled-display.service /etc/systemd/system/oled-display.service
```

Reload and enable systemd service (enable mean it will start at boot)

```
sudo systemctl daemon-reload
sudo systemctl enable oled-display.service
```

To disable start at boot

```
sudo systemctl disable oled-display.service
```

Then reboot or trigger with classical commands:

```
sudo systemctl start oled-display.service
sudo systemctl stop oled-display.service
sudo systemctl reload oled-display.service
```


## Usage

The usage of this script is fairly simple: the stdout that shall be displayed shall be piped to the RAM files that are read by the script `/dev/shm/line1` & `/dev/shm/line2` (`line1` is upper line)

If any of this file contains `cls` screen will be cleared

If one file doesn't exist, corresponding line will be empty

In the script 2 vars could be adjusted:
 - `pollinterval` is the delay in seconds for the script to poll the files (and display them)
 - `screensaver_delay` is the delay in seconds for which screen will be cleared if the content of the line don't change

As an example:

```
echo "cls" > /dev/shm/line1 # will clear the screen
ls -a /etc/ > /dev/shm/line1 # will display only the first line !
```
