import time
from ffpyplayer.player import MediaPlayer

url = "tcp://10.42.0.1:8888"

player = MediaPlayer(
    url,
    ff_opts={
        "vf": ["setpts=N/15"],
        "framedrop": True,
    },
    lib_opts={
        "fflags": "nobuffer",
        "flags": "low_delay",
    },
    loglevel="info",
)

print(f"Connecting to {url}...")
deadline = time.monotonic() + 12
frames = 0

try:
    while time.monotonic() < deadline and frames < 5:
        frame, delay = player.get_frame()

        if frame is not None:
            image, timestamp = frame
            frames += 1
            print(
                f"Frame {frames}: timestamp={timestamp:.3f}s, "
                f"size={image.get_size()}, format={image.get_pixel_format()}"
            )
            if frames == 1:
                print("Stream metadata:", player.get_metadata())

        elif isinstance(delay, str):
            print("Player status:", delay)
            if delay == "eof":
                break
            time.sleep(0.05)

        else:
            time.sleep(max(delay, 0.01))

    if frames == 0:
        print("No decoded frames arrived within 12 seconds.")
    else:
        print(f"Success: received {frames} decoded frames.")

finally:
    player = None