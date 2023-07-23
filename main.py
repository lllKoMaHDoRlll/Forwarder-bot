from backend.forwarder import Forwarder

if __name__ == "__main__":
    forwarder = Forwarder()

    forwarder.load()
    forwarder.start()
