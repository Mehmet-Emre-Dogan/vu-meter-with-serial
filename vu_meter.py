#!/usr/bin/python3
import pyaudiowpatch as pyaudio
from amplitude import Amplitude
from vu_utilityFunctions import LoadConfig, Saturate
import serial
import sys
import os

if os.name == 'nt': # Only if we are running on Windows
    from ctypes import windll
    k = windll.kernel32
    k.SetConsoleMode(k.GetStdHandle(-11), 7)

def main(p_sConfigDictPath):
    dtConfig = LoadConfig(p_sConfigDictPath)
    # if dtConfig == {}

    with serial.Serial(
                        port=dtConfig["SerialDeviceSettings"]["COMPort"], 
                        baudrate=dtConfig["SerialDeviceSettings"]["Baudrate"], 
                        timeout=dtConfig["SerialDeviceSettings"]["TimeoutInSeconds"],
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS
                        ) as ser:

        with pyaudio.PyAudio() as p:
            try:
                # Get default WASAPI info
                wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
            except OSError:
                print("Looks like WASAPI is not available on the system. Exiting...")
                exit()
        
            if dtConfig["UseSpeakerOrMic"] == "Speaker":
                # Get default WASAPI speakers
                default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
                
                if not default_speakers["isLoopbackDevice"]:
                    for loopback in p.get_loopback_device_info_generator():
                        """
                        Try to find loopback device with same name(and [Loopback suffix]).
                        Unfortunately, this is the most adequate way at the moment.
                        """
                        if default_speakers["name"] in loopback["name"]:
                            default_speakers = loopback
                            break
                    else:
                        print("Default loopback output device not found.\n\nRun `python -m pyaudiowpatch` to check available devices.\nExiting...\n")
                        exit()

                NumberofChannels        = default_speakers["maxInputChannels"]
                iRate                   = int(default_speakers["defaultSampleRate"])
                iInputFramesPerBlock    = int(iRate * dtConfig["InputBlockTimeInSeconds"])
                iInputDeviceIndex       = default_speakers["index"]

            elif dtConfig["UseSpeakerOrMic"] == "Mic":
                # Get default WASAPI microphones
                default_microphones = p.get_device_info_by_index(wasapi_info["defaultInputDevice"])

                NumberofChannels        = default_microphones["maxInputChannels"]
                iRate                   = int(default_microphones["defaultSampleRate"])
                iInputFramesPerBlock    = int(iRate * dtConfig["InputBlockTimeInSeconds"])
                iInputDeviceIndex       = default_microphones["index"]
            else:
                raise Exception("Invalid <UseSpeakerOrMic> param. Use 'Speaker' or 'Mic'")

            with p.open(format=pyaudio.paInt16,
                        channels=NumberofChannels,
                        rate=iRate,
                        input=True,
                        frames_per_buffer=iInputFramesPerBlock,
                        input_device_index=iInputDeviceIndex
                        ) as stream:

                maximal = Amplitude()
                while True:
                    data = stream.read(iInputFramesPerBlock, exception_on_overflow=False)
                    amp = Amplitude.from_data(data, dtConfig["PrintConsequtively"])
                    if dtConfig["UseSpeakerOrMic"] == "Mic":
                        amp -= Amplitude(dtConfig["AmbientNoiseForMicInDB"])
                        # print(amp)
                        amp = Amplitude(Saturate(amp.value, 0, 40))
                    i8AmplitudeInBytes = amp.to_int(255)
                    ser.write(i8AmplitudeInBytes.to_bytes(1, "big"))
                    if amp > maximal:
                        maximal = amp
                    if(dtConfig["ConsoleDisplayEnabled"]):
                        amp.display(scale=100, mark=maximal)

if __name__ == "__main__":
    sConfigDictPath = sys.argv[1]
    main(sConfigDictPath)
