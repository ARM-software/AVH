# FVP Audio

The **FVP Audio** project demonstrates the CMSIS-Driver vStream API for handling
audio input and output streams.

It shows how to capture audio samples from an input stream and output them through a audio output stream.

## Operation

The application initializes both audio input and output streams and then continuously
captures audio samples from the input stream and copies them directly to the output
stream.

The example uses CMSIS-RTOS2 for thread management and event-driven processing.

### Configuration

Default configuration expects the following input and output stream format:

- 16kHz, 16-bit, 2-channels (stereo)

To change default configuration use configuration defines:

- `AUDIO_CHANNELS`    - sets the number of channels in a stream
- `AUDIO_SAMPLE_BITS` - sets the number of bits per sample
- `AUDIO_SAMPLE_RATE` - sets the number of samples per second
