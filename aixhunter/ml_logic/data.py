
from multiprocessing import Pool

from aixhunter.params import BUCKET_IMAGES


# import tensorflow_datasets as tfds
from tensorflow.keras.utils import image_dataset_from_directory



def load_images_from_bucket(image_bucket, labels:str ='inferred', label_mode:str ='binary'
                               , image_size:tuple =(32, 32), batch_size:int =32):
    print('Loading images from google storage ... this might take some time ...')
    dataset = image_dataset_from_directory(
        directory=f'gs://{image_bucket}',
        labels=labels,
        label_mode=label_mode,
        image_size=image_size,
        batch_size=1,
        shuffle=True
    )
    return dataset


if __name__ == '__main__':
    load_images_from_bucket(BUCKET_IMAGES)
