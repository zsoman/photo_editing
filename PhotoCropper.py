import argparse
from os import listdir, makedirs
from os.path import isfile, join, basename, dirname, isdir

from PIL import Image
from tqdm import tqdm


# folder_path = 'photos'
# left, top, right, bottom = 559, 225, 1361, 0
# -d ./photos -s ./photos2 -c -a 559 225 1361 0

def build_argparse():
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--directory', help = 'perform the action on all photos in a directory', type = str,
                        default = False)
    parser.add_argument('-f', '--file', help = 'perform the action on one photo', type = str, default = False)
    parser.add_argument('-n', '--name', help = 'new file name', type = str, default = '')
    parser.add_argument('-s', '--save', help = 'destination directory to save the new photos', type = str,
                        default = False)
    parser.add_argument('-c', '--crop', help = 'crop the image(s) in a rectangle', action = 'store_true')
    parser.add_argument('-a', '--area', help = 'define the rectangle to crop, the order of sequence is: left, top, '
                                               'right, bottom', type = int, nargs = 4, default = [0, 0, 0, 0])
    parser.add_argument('-l', '--left', help = 'the left pixel from to crop', type = int, default = 0)
    parser.add_argument('-t', '--top', help = 'the top pixel from to crop', type = int, default = 0)
    parser.add_argument('-r', '--right', help = 'the right pixel from to crop', type = int, default = 0)
    parser.add_argument('-b', '--bottom', help = 'the bottom pixel from to crop', type = int, default = 0)

    args = parser.parse_args()

    return args


def photo_crop(image_path, save_to_path, left = 0, top = 0, right = 0, bottom = 0, number = 0, new_file_name = ''):
    with Image.open(image_path) as image:
        image_colors = image.load()
        if left == 0 and right == 0 and top == 0 and bottom == 0:
            right, bottom = image.size
        if bottom == 0:
            for y in range(400, image.size[1]):
                if image_colors[1358, y] == (181, 181, 181, 255):
                    bottom = y
        bottom += 2
        cropped_image = image.crop((left, top, right, bottom))
        if new_file_name == '':
            cropped_image.save(join(save_to_path, basename(image_path)))
        else:
            if '.' in new_file_name:
                cropped_image.save(join(save_to_path, '{}{:02d}.{}'.format(new_file_name.split('.')[0], number if number > 0 else '', basename(new_file_name).split('.')[1])))
            else:
                cropped_image.save(join(save_to_path, '{}{:02d}.{}'.format(new_file_name.split('.')[0], number if number > 0 else '', basename(image_path).split('.')[1])))


def all_files_in_folder(folder_path):
    return [join(folder_path, f) for f in listdir(folder_path) if isfile(join(folder_path, f))]


def main():
    args = build_argparse()
    if args.crop:
        if args.area != [0, 0, 0, 0]:
            left, top, right, bottom = args.area
        else:
            left = args.left
            top = args.top
            right = args.right
            bottom = args.bottom
        if args.directory:
            if args.save:
                path_to_save = args.save
                if not isdir(path_to_save):
                    makedirs(path_to_save)
            else:
                path_to_save = args.directory
            for i, image_path in enumerate(tqdm(all_files_in_folder(args.directory))):
                photo_crop(image_path, path_to_save, left, top, right, bottom, i+1, args.name)
            print("The operations are completed check the {} folder for the photos.".format(path_to_save))
        elif args.file:
            if args.save:
                path_to_save = args.save
                if not isdir(path_to_save):
                    makedirs(path_to_save)
            else:
                path_to_save = dirname(args.file)
            photo_crop(args.file, path_to_save, left, top, right, bottom, 0, args.name)
            print("The operation is completed check the {} folder for the photo.".format(path_to_save))


main()
