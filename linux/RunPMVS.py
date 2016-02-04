import logging
import osmpmvs

logging.basicConfig(level=logging.INFO, format="%(message)s")

# initialize OsmPMVS manager class
manager = osmpmvs.OsmPmvs()

# initialize PMVS input from Bundler output
manager.doBundle2PMVS()

# call PMVS
manager.doPMVS()
