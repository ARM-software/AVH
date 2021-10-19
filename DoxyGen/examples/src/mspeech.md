# Micro speech example {#mspeech}

The Micro speech program analyzes an audio input with a voice recognition model that can detect 2 keywords - **yes** and **no**. The recognized keywords are then printed into a serial interface. The voice recognition model is implemented using [TensorFlow Lite for Microcontrollers](https://www.tensorflow.org/lite/microcontrollers).

GitHub repository [**github.com/arm-software/VHT-TFLmicrospeech**](https://github.com/arm-software/VHT-TFLmicrospeech) contains an implementation supporting Arm Virtual Hardware Targets (VHT) as well as real hardware boards.
It demonstrates how to use the processor and peripheral abstraction layers for simpler software portability across different targets. The example repository contains documentation with running instructions.

Sections <a href="../../infrastructure/html/run_ami_local.html">**Run AMI with Local Host**</a> and <a href="../../infrastructure/html/run_ami_github.html">**Run AMI with GitHub Actions**</a> explain how to build and run an application project on Arm Virtual Hardware and use the Micro speech example as a reference.





