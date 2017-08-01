# Change this if you want to run a custom version of firefly
appScript = 'firefly/firefly.py'

# Initially set an empty data path variable. This will be filled by the dataset config
# file (if we choose one). If the app runs with this unset, we will show a splash screen.
datasetPath = None

# Execute the firefly script after the data config file had a chance to load
from threading import Timer
def main():
    queueCommand(':r ' + appScript)
bt = Timer(0.1, main)
bt.start()
