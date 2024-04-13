from pipewire_python.controller import Controller

def play_wav_to_virtual_mic(filename, mic_name="VirtualMic"):
  """Plays a WAV file through the specified virtual microphone.

  Args:
    filename: Path to the WAV file.
    mic_name: Name of the virtual microphone (default: "VirtualMic").
  """

  # Initialize PipeWire controller
  controller = Controller()

  # Read WAV file data (replace with your method)
  with open(filename, "rb") as f:
    wav_data = f.read()

  # Configure virtual microphone format (adjust if needed)
  format = {
      "format": "s16le",
      "rate": 48000,
      "channels": 2,
  }

  # Create virtual microphone
  try:
    controller.device_create_source(
        name=mic_name, format=format, media_class="Audio/Source/Virtual"
    )
  except Exception as e:
    print(f"Error creating virtual microphone: {e}")
    return

  # Open a stream to the virtual microphone
  stream = controller.stream_create(source=f"{mic_name}.monitor.0")

  # Write WAV data to the stream in chunks
  chunk_size = 1024
  for i in range(0, len(wav_data), chunk_size):
    chunk = wav_data[i:i + chunk_size]
    stream.write(chunk)

  # Close the stream and clean up
  stream.close()

# Replace with your WAV file path
filename = "/home/ubuntu/interact/audio/speak_5.wav"
play_wav_to_virtual_mic(filename)

