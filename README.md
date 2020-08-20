# n2n-watermark-remove
run : python train.py --image_dir dataset/train --test_dir dataset/test --image_size 360 60 --batch_size 8 --lr 0.01 --source_noise_model text,0,50 --target_noise_model clean,0,50 --val_noise_model text,25,25 --loss mae --output_path text_noise

test : 
python test_model.py --weight_file text_noise/cur/weights.031-3.642-30.28125.hdf5  --image_dir inputdir --output_dir outputdir_cont

find the best model : python ./compare_model/compare_model.py  # 運行前需要取消test_model.py 71、72的注釋