# VHT


## Directory Structure

Directory      | Description
:--------------|:--------------------------------------------------
interface      | Interface (APIs with drivers and Pyhton scripts)
Doxygen        | Doxygen documentation of Orta
Documentation  | Output directory for the documentation


## Interface

### Virtual Streaming Interface (VSI)

Virtual Streaming Interface is a peripheral simulated in Fast Models with running user Python scripts.

It contains:
 - `./interface/include/`[arm_vsi.h](./interface/include/arm_vsi.h): VSI API header
 - `./interface/python/`[arm_vsi0.py](./interface/python/arm_vsi0.py): VSI Python script template (instance 0)
 - `./interface/python/`[arm_vsi1.py](./interface/python/arm_vsi1.py): VSI Python script template (instance 1)
 - `./interface/python/`[arm_vsi2.py](./interface/python/arm_vsi2.py): VSI Python script template (instance 2)
 - `./interface/python/`[arm_vsi3.py](./interface/python/arm_vsi3.py): VSI Python script template (instance 3)
 - `./interface/python/`[arm_vsi4.py](./interface/python/arm_vsi4.py): VSI Python script template (instance 4)
 - `./interface/python/`[arm_vsi5.py](./interface/python/arm_vsi5.py): VSI Python script template (instance 5)
 - `./interface/python/`[arm_vsi6.py](./interface/python/arm_vsi6.py): VSI Python script template (instance 6)
 - `./interface/python/`[arm_vsi7.py](./interface/python/arm_vsi7.py): VSI Python script template (instance 7)

### Audio as Virtual Streaming Interface (VSI)

Audio driver implementing the VSI API. Peripheral is defined as a Virtual Streaming Interface (VSI) simulated in Fast Models with Audio specific Python scripts.

It contains:
 - `./interface/audio/include/audio_drv.h`: Audio API header
 - `./interface/audio/driver/audio_drv.c`: Audio driver for VSI
 - `./interface/audio/python/arm_vsi0.py`: Python script for Audio Input (instance 0)
 - `./interface/audio/python/arm_vsi1.py`: Python script for Audio Output (instance 1)

