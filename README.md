# vu-meter-with-serial
*Measure volumes and send to an LED device via serial port with Python!*

## Requirements
* [PyAudioWPatch ](https://pypi.org/project/PyAudioWPatch/)
* [pyserial ](https://pypi.org/project/pyserial/)

## Usage

- Configure `vu_config.json` as your needs
    - `"ConsoleDisplayEnabled"`     :  enables console graphics (needs to be disabled to be run in background)
    - `"PrintConsequtively"`        :  `false` -> single line graphics; `true` -> multi-line consequtive graphics (keeps old samples) 
    - `"UseSpeakerOrMic"`           :  `"Speaker"` or `"Mic"`
    - `"AmbientNoiseForMicInDB"`    :  Ambient noise cancellation for `Mic`
    - `"InputBlockTimeInSeconds"`   :  Chunk size in seconds to be sampled
    - `"SerialDeviceSettings"`      :  Parameters for the external hardware connected via the serial port
- Prepare your hardware ( example: https://github.com/Mehmet-Emre-Dogan/wirelessMusicVisualizer )
- Find your COM port using Device Manager and enter it to `vu_config.json`
- Use `run.bat` to run application in foreground. You may exit program using `X` button on the console.
- Use `run_backgnd.bat` to run application in background. To exit program, use `kill_backgnd.ps1`.


## Credits
https://github.com/s0d3s/PyAudioWPatch/blob/master/examples/pawp_record_wasapi_loopback.py