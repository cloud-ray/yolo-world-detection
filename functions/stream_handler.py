from vidgear.gears import CamGear

def initialize_stream(source):
    cap = CamGear(source=source, stream_mode=True, logging=True).start()
    return cap
