from PIL import Image, ExifTags


def print_exif_data(img_path):
    img = Image.open(img_path)
    img_exif = img.getexif()
    print(type(img_exif))

    if img_exif is None:
        print('Sorry, image has no exif data.')
    else:
        for key, val in img_exif.items():
            if key in ExifTags.TAGS:
                print(f'{ExifTags.TAGS[key]}:{val}')
            else:
                print(f'{key}:{val}')


if __name__ == '__main__':
    print_exif_data('../imgs/yoga.JPG')

