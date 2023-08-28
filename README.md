# XDM1041-Python
A python driver for the XDM1041 Multimeter instrument

The XDM1041 is a capable, "lower cost" benchtop DMM (~$150 USD)

One reviewer compared it to a $1000 Fluke instrument with very good results.

That video here: https://pallavaggarwal.in/owon-xdm1041-programmable-multimeter/

One of the key features is high precision DC voltage measurement at 50mV range. 
There is also a fine-grained 500uA current measurement range for AC and DC. 

The meter can be controlled via RS232 port and the readings can be sent over the port.

## Interfacing

You'll need an available RS232 port, or an RS232 to USB converter. We used the 
"UGREEN USB to RS232 Serial Cable DB9 9 Pin USB 2.0 Male A Converter Adapter with Prolific PL2303 Chipset" 
with good success. 

## API / Using the module

Check ```test_general.py``` for usage information. The API has support for all mode switching, range selection,
as well as some other features, but support is limited for advanced Math and Datalogging modes. 


## Sample Rate

The manual claims the sample rate is 4 samples per second for Low, 16 samples per second for Medium and 
65 samples per second for High, meaning we should be able to get about 1 sample per 15ms in "High". Accordingly, 
the baud rate for the serial port is 115,200 which gives us an actual bytes per second of approximately 11000.
If the represented float has an average of 10 bytes in length, and the command is 10 bytes, we should
be able to get at least 550 samples per second (11000 bytes per second / 20). 

However, in looking at the actual received data, the sample rate seems to be closer to 2-3Hz or
one sample every 300-400ms

The actual meter may therefor sample at a higher rate but only update the data over the serial port every 300-400ms

For an example, look in ```misc/test_sample_rate.txt```

More thorough testing will be required, but since our application doesn't need higher rate sampling, we'll leave that 
as a future exercise. 