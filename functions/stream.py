from vidgear.gears import CamGear

def get_stream():
    # Initialize CamGear stream
    youtube_stream = CamGear(
        source="https://www.youtube.com/live/OIqUka8BOS8?si=DVQmFImFtmlBB4QR",
        stream_mode=True,
        logging=True
    ).start()
    return youtube_stream
