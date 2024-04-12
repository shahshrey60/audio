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

import subprocess

def route_audio_to_loopback_source(wav_file, source_name):
    try:
        subprocess.run(["pacat", wav_file, "<", source_name], check=True, shell=True)
        print("Audio routed to loopback source successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error routing audio to loopback source: {e}")

def record_from_loopback_sink(channels, recording_file, sink_name):
    try:
        subprocess.run(["parecord", "--channels=" + str(channels), "-d", recording_file, sink_name], check=True)
        print("Audio recorded from loopback sink successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error recording audio from loopback sink: {e}")


from seleniumbase import SB

def main():
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
        audio_file_path = "/home/ubuntu/interact/int/audio/speak_5.wav"
        recorded_audio_file_path = "/home/ubuntu/interact/int/audio/recorded_audio.wav"
    
        # Set the sink and source names
        sink_name = "my_sink"
        source_name = "my_sink.monitor"
        
        # subprocess.Popen(["paplay", "--device=" + source_name, audio_file_path])
        # subprocess.Popen(["parec", "--device=" + sink_name, recorded_audio_file_path])

        # subprocess.Popen(["paplay", "/home/ubuntu/interact/int/audio/speak_5.wav"])
        # Replace these variables with your actual WAV file path, loopback source name, and sink name
        wav_file = "/home/ubuntu/interact/int/audio/speak_5.wav"
        # source_name = "your_loopback_source_name"
        # sink_name = "your_loopback_sink_name"
        recording_file = "/home/ubuntu/interact/int/audio/recorded_audio.wav"
        channels = 2
        
        # Route audio to loopback source (virtual mic)
        route_audio_to_loopback_source(wav_file, source_name)
        
        # Record from loopback sink (virtual speaker)
        record_from_loopback_sink(channels, recording_file, sink_name)
        time.sleep(25)
        print("Done 5")
        driver.save_screenshot("test.png")

if __name__ == "__main__":
    main()








