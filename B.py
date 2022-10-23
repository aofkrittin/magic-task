from magic import magicmodel

magic = magicmodel(input_video="B.mp4", min_threshold = 35, max_threshold = 55)
magic.count_wave(plot=False)