import os

model = []
for r, dirs, files in os.walk('../text_noise/cur'):
    # Get all the images
    for file in files:
        model.append(file)

for each in model:
    path = "../text_noise/cur/" + each
    inputdir = "input_best_model"
    outputdir = "outputdir"
    os.system("python ../test_model.py --weight_file %s --image_dir %s --output_dir %s" % (path, inputdir, outputdir))