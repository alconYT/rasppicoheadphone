import board
import audiobusio
import time

# Define the threshold for audio level detection
THRESHOLD = 5000

# Initialize the microphone
mic = audiobusio.PDMIn(board.GP26, board.GP27, sample_rate=16000, bit_depth=16)

# Main loop
while True:
    # Read audio data from the microphone
    raw_samples = mic.record(512)

    # Compute the root mean square (RMS) of the audio data
    samples = list(raw_samples)
    sum_squares = sum(float(s ** 2) for s in samples)
    rms = int((sum_squares / len(samples)) ** 0.5)

    # Check if the audio level exceeds the threshold
    if rms > THRESHOLD:
        print("Audio level:", rms)
        # Perform an action here, such as triggering an event or sending a notification
        # For demonstration purposes, we simply sleep for 2 seconds
        time.sleep(2)
