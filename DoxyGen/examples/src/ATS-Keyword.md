# ATS-Keyword Example {#ATS-Keyword}

The Arm Total Solution keyword detection application (ATS-Keyword) detects keywords in the audio input using Machine-Learning model DS-CNN and publishes recognized keywords to [AWS IoT Service](https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html) in the cloud.

The audio data to process are injected at run time from using the [virtual audio streaming interface](../../simulation/html/group__arm__vsi__audio.html). Additionally the AWS IoT service is used for OTA firmware updates. These firmware updates are securely applied using [Trusted Firmware-M](https://tf-m-user-guide.trustedfirmware.org/).

For more information, refer to the example descriptions in the [ATS-Keyword GitHub repository] (https://github.com/ARM-software/open-iot-sdk/tree/main/examples/ats-keyword).

