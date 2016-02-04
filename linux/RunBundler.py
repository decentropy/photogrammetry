import logging
import osmbundler

logging.basicConfig(level=logging.INFO, format="%(message)s")

# initialize OsmBundler manager class
manager = osmbundler.OsmBundler()

manager.preparePhotos()

manager.matchFeatures()

manager.doBundleAdjustment()

manager.openResult()

