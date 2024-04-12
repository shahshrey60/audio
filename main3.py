import subprocess
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

def play_audio_in_loopback_source(wav_file, source_name):
    try:
        subprocess.Popen(["pacat", wav_file, "<", source_name], shell=True)
        print("Audio playing in loopback source.")
    except Exception as e:
        print(f"Error playing audio in loopback source: {e}")

def record_audio_from_loopback_sink(channels, recording_file, sink_name):
    try:
        subprocess.Popen(["parecord", "--channels=" + str(channels), "-d", recording_file, sink_name])
        print("Recording audio from loopback sink.")
    except Exception as e:
        print(f"Error recording audio from loopback sink: {e}")

def main():
    with SB(uc=True, headless=True) as driver:
        subprocess.run(["pacmd", "set-default-sink", "my_sink"])

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
        driver.get('https://meet.google.com/ozg-cnsp-zii')
        time.sleep(10)
        time.sleep(10)
        print("Done 4")
        AskToJoin(driver)
        time.sleep(12)
        
        wav_file = "/home/ubuntu/interact/int/audio/speak_5.wav"
        sink_name = "my_sink"
        source_name = "my_sink.monitor"
        recording_file = "/home/ubuntu/interact/int/audio/recorded_audio.wav"
        channels = 2
        
        play_audio_in_loopback_source(wav_file, source_name)
        record_audio_from_loopback_sink(channels, recording_file, sink_name)
        
        time.sleep(25)
        print("Done 5")
        driver.save_screenshot("test.png")

if __name__ == "__main__":
    main()
