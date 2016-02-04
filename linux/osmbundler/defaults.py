
maxPhotoDimension = 1200
matchingEngine = "bundler"
featureExtractor = "siftvlfeat"

bundlerOptions = (
"--match_table matches.init.txt\n",
"--output bundle.out\n",
"--output_all bundle_\n",
"--output_dir bundle\n",
"--variable_focal_length\n",
"--use_focal_estimate\n",
"--constrain_focal\n",
"--constrain_focal_weight 0.0001\n",
"--estimate_distortion\n",
"--run_bundle\n"
)