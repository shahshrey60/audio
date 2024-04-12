import gi

gi.require_version('pulseaudio', '1.0')
from gi.repository import PulseAudio

def play_wav_to_virtual_mic(wav_file, loopback_source):
  """Plays a WAV file to the specified PulseAudio loopback source (virtual mic)"""
  try:
    # Open the WAV file
    with open(wav_file, "rb") as f:
      wav_data = f.read()

    # Initialize PulseAudio
    pa = PulseAudio.init(application_name="WAV to Virtual Mic")

    # Get the loopback source stream
    stream = pa.stream_new(name="WAV Player", stream_direction=PulseAudio.StreamDirection.OUTPUT)
    stream.set_state(PulseAudio.StreamState.RUNNING)

    # Configure stream format based on WAV file (modify if needed)
    sample_spec = PulseAudio.SampleSpec(format=PulseAudio.SampleFormat.S16LE, channels=2, rate=44100)
    stream.set_sample_spec(sample_spec)

    # Write WAV data to the stream (play to virtual mic)
    sink = stream.get_sink()
    sink.cork()
    sink.write(wav_data, len(wav_data), PulseAudio.SinkFlags.LATENCY)
    sink.uncork()

    print(f"Playing WAV file: {wav_file} to {loopback_source}")
  except Exception as e:
    print(f"Error playing WAV: {e}")

def record_from_virtual_speaker(recording_file, loopback_sink, channels=2, sample_rate=44100):
  """Records audio from the specified PulseAudio loopback sink (virtual speaker)"""
  try:
    # Initialize PulseAudio
    pa = PulseAudio.init(application_name="Virtual Speaker Recorder")

    # Get the loopback sink stream
    stream = pa.stream_new(name="Virtual Speaker Recorder", stream_direction=PulseAudio.StreamDirection.INPUT)
    stream.set_state(PulseAudio.StreamState.RUNNING)

    # Configure stream format based on desired recording parameters
    sample_spec = PulseAudio.SampleSpec(format=PulseAudio.SampleFormat.S16LE, channels=channels, rate=sample_rate)
    stream.set_sample_spec(sample_spec)

    # Open the recording file
    with open(recording_file, "wb") as f:
      # Callback function to receive and write recorded audio data
      def callback(stream, data, length, userdata):
        f.write(data)
      stream.set_read_callback(callback, None)

      # Start recording
      stream.start()

      print(f"Recording audio from: {loopback_sink} to {recording_file}")

      # Wait until the user interrupts (Ctrl+C)
      while True:
        pass

  except Exception as e:
    print(f"Error recording audio: {e}")


import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up loopback device
# subprocess.run(["pactl", "load-module", "module-null-sink", "sink_name=my_sink"])
# subprocess.run(["pactl", "load-module", "module-loopback", "source=my_sink.monitor"])

from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def AskToJoin(driver):
    # Ask to Join meet
    # time.sleep(5)
    # Wait for the 'Join now' button to be clickable
    try:
        join_now_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Ask to join']")))
        # Click the 'Join now' button
        join_now_button.click()
        # Accept any alert that might appear
    except Exception as e:
        join_now_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Join now']")))
        # Click the 'Join now' button
        join_now_button.click()
        # Accept any alert that might appear
    

from seleniumbase import SB

def meet_main():
    # permissions = [
    # {
    #     "name": "geolocation",
    #     "grant": "granted"
    # },
    # {
    #     "name": "audioCapture",
    #     "grant": "granted"
    # },
    # {
    #     "name": "videoCapture",
    #     "grant": "denied"
    # }
    # ]
    with SB(uc=True, headless=True) as driver:
        subprocess.run(["pacmd", "set-default-sink", 'my_sink'])
        driver.execute_cdp_cmd(
            "Browser.grantPermissions",
            {
                "origin": 'https://meet.google.com',
                "permissions": ["geolocation", "audioCapture", "displayCapture", "videoCapture",
                    "videoCapturePanTiltZoom"]
                # "permissions":permissions,
            },
        )
        # driver.execute_script("navigator.permissions.query({name:'geolocation'}).then(permission => { permission.state = 'denied'; });")
        # driver.execute_script("navigator.permissions.query({name:'microphone'}).then(permission => { permission.state = 'granted'; });")
        # driver.execute_script("navigator.permissions.query({name:'camera'}).then(permission => { permission.state = 'denied'; });")

        time.sleep(10)
        print("Done 1")
        driver.get("https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow")
        driver.type("#identifierId",'compbadshah1408@gmail.com')
        driver.click("#identifierNext > div > button")
        print("Done 2")
        time.sleep(10)
        driver.type("#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input", 'Shrey@1408')
        driver.click("#passwordNext > div > button")
        time.sleep(10)
        print("Done 3")
        driver.get('https://meet.google.com/ozg-cnsp-zii')
        time.sleep(10)
        time.sleep(10)
        print("Done 4")
        AskToJoin(driver)
        time.sleep(12)
        # audio_file_path = "/home/ubuntu/interact/int/audio/speak_5.wav"
        # recorded_audio_file_path = "/home/ubuntu/interact/int/audio/recorded_audio.wav"
    
        # # Set the sink and source names
        # sink_name = "my_sink"
        # source_name = "my_sink.monitor"
        # subprocess.Popen(["paplay", "--device=" + sink_name, audio_file_path])

    
        # subprocess.Popen(["parec", "--device=" + source_name, recorded_audio_file_path])

        # subprocess.Popen(["paplay", "/home/ubuntu/interact/int/audio/speak_5.wav"])

        ##New Part

        wav_file = "/home/ubuntu/interact/int/audio/speak_5.wav"
        loopback_source = "my_sink.monitor"  # Replace with your loopback source name
        recording_file = "/home/ubuntu/interact/int/audio/recording.wav"
      
        # Create the loopback using pactl (outside of Python for now)
        # ... (refer to previous instructions for creating the loopback)
      
        # Play WAV to virtual mic
        play_wav_to_virtual_mic(wav_file, loopback_source)
      
        # Record from virtual speaker
        record_from_virtual_speaker(recording_file, loopback_sink=loopback_source)  # Use loopback source name as sink
        ##New Part
        time.sleep(25)
        print("Done 5")
        driver.save_screenshot("test.png")

if __name__ == "__main__":
  # Modify these variables as needed
  meet_main()
  
