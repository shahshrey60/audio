from pipewire_python import Context, Node, Stream, MediaStreamFlags

def inject_audio_to_virtual_mic(audio_data, mic_name="VirtualMic"):
  """Injects audio data into the specified virtual microphone.

  Args:
    audio_data: The audio data to be injected (bytes).
    mic_name: Name of the virtual microphone (default: "VirtualMic").
  """

  # Initialize PipeWire context
  context = Context()

  # Configure virtual microphone format (adjust if needed)
  format = {
      "format": "s16le",
      "rate": 48000,
      "channels": 2,
  }

  # Create a node for the virtual microphone
  node = context.create_node(
      name=mic_name,
      properties={
          "media.class": "Audio/Source/Virtual",
      },
      # Specify format using MediaStreamInfo
      links=[
          Node.Link(
              name="source",
              info=MediaStreamInfo(format=format),
              flags=MediaStreamFlags.SHARED,
          )
      ],
  )

  # Open a stream to write data to the virtual microphone
  stream = context.create_stream(
      nodes=[node],
      flags=MediaStreamFlags.AUTOMATIC_BUFFERING,
  )

  # Write audio data to the stream
  stream.write(audio_data)

  # Close the stream and clean up
  stream.close()
  context.close()  # Close the context





import subprocess
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import BaseCase, SB

def AskToJoin(driver):
    try:
        join_now_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Ask to join']")))
        join_now_button.click()
    except Exception as e:
        join_now_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Join now']")))
        join_now_button.click()

# Create named pipes for virtual microphone and speaker
virtual_mic_pipe = "/tmp/virtual_mic"
virtual_speaker_pipe = "/tmp/virtual_speaker"

if not os.path.exists(virtual_mic_pipe):
        os.mkfifo(virtual_mic_pipe)

if not os.path.exists(virtual_speaker_pipe):
        os.mkfifo(virtual_speaker_pipe)

# Play audio into the virtual microphone
def play_audio(wav_file):
        import subprocess
        subprocess.Popen(["cat", wav_file, ">", virtual_mic_pipe], shell=True)

# Record audio from the virtual speaker
def record_audio(recording_file):
        import subprocess
        subprocess.Popen(["arecord", "-f", "S16_LE", "-r", "44100", "-c", "2", recording_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            
def main():
    with SB(uc=True, headless=True) as driver:
        driver.execute_cdp_cmd(
            "Browser.grantPermissions",
            {
                "origin": 'https://meet.google.com',
                "permissions": ["geolocation", "audioCapture", "displayCapture", "videoCapture", "videoCapturePanTiltZoom"]
            },
        )
        
        time.sleep(10)
        print("Done 1")
        driver.get("https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow")
        driver.type("#identifierId", 'compbadshah1408@gmail.com')
        driver.click("#identifierNext > div > button")
        print("Done 2")
        time.sleep(10)
        driver.type("#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input", 'Shrey@1408')
        driver.click("#passwordNext > div > button")
        time.sleep(10)
        print("Done 3")
        driver.get('https://meet.google.com/jyd-rvay-tot')
        time.sleep(10)
        time.sleep(10)
        print("Done 4")
        AskToJoin(driver)
        time.sleep(12)
        
        wav_file = "/home/ubuntu/interact/int/audio/speak_5.wav"
        sink_name = "Loopback,0,0"
        source_name = "Loopback,1,0"
        recording_file = "/home/ubuntu/interact/int/audio/recorded_audio.wav"
        channels = 2
        sample_format = "s16le"
        rate = 44100
        
        # route_audio_to_loopback_source(wav_file, source_name)
        import subprocess
        import os
        

        
        
        # record_audio_from_loopback_sink(channels, recording_file)
        # play_audio(wav_file)
        # record_audio(recording_file)
        # Replace with your method for obtaining audio data (e.g., reading from a file)
        inject_audio_to_virtual_mic(wav_file)


        time.sleep(25)
        print("Done 5")
        driver.save_screenshot("test.png")

if __name__ == "__main__":
    main()
