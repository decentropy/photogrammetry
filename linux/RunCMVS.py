import logging
import osmcmvs

logging.basicConfig(level=logging.INFO, format="%(message)s")

# initialize OsmCMVS manager class
manager = osmcmvs.OsmCmvs()

# initialize PMVS input from Bundler output
manager.doBundle2PMVS()

# call PMVS
manager.doCMVS()
