import datetime
import glob
import os
import sys
import shutil


def make_dir_for_object(date_dir, object_name):
    obj = os.path.join(date_dir, object_name)
    os.mkdir(obj)

    spectrum = os.path.join(obj, "Ha")
    os.mkdir(spectrum)
    os.mkdir(os.path.join(spectrum, "lights"))
    os.mkdir(os.path.join(spectrum, "darks"))
    os.mkdir(os.path.join(spectrum, "flats"))

    spectrum = os.path.join(obj, "S")
    os.mkdir(spectrum)
    os.mkdir(os.path.join(spectrum, "lights"))
    os.mkdir(os.path.join(spectrum, "darks"))
    os.mkdir(os.path.join(spectrum, "flats"))

    spectrum = os.path.join(obj, "O")
    os.mkdir(spectrum)
    os.mkdir(os.path.join(spectrum, "lights"))
    os.mkdir(os.path.join(spectrum, "darks"))
    os.mkdir(os.path.join(spectrum, "flats"))

    spectrum = os.path.join(obj, "Color")
    os.mkdir(spectrum)
    os.mkdir(os.path.join(spectrum, "lights"))
    os.mkdir(os.path.join(spectrum, "darks"))
    os.mkdir(os.path.join(spectrum, "flats"))

    return obj


def copy_images(copied_set, from_path, to_path, file_pattern, sub_dir):
    print(from_path, to_path, file_pattern, sub_dir)
    lights = os.path.join(from_path, file_pattern)

    to_dest = os.path.join(to_path, sub_dir)
    for filename in glob.glob(lights):
        print("Moving " + filename + " to " + to_dest)
        if filename not in copied_set:
            shutil.copy(filename, to_dest)
            copied_set.add(filename)


def extract(argv):
    in_path = sys.argv[1]
    out_path = sys.argv[2]
    copied_files = {""}

    print(in_path + " " + out_path)
    lights = os.path.join(in_path, "Light")

    for filename in os.listdir(lights):
        object_dir = os.path.join(lights, filename)
        if os.path.isdir(object_dir):
            print(object_dir)
            m_time = os.path.getmtime(object_dir)
            dt_m = datetime.datetime.fromtimestamp(m_time)
            date_time = dt_m.strftime("%m-%d-%y")
            print('Modified on:', date_time)
            date_of_capture = os.path.join(out_path, date_time)
            exists = os.path.exists(date_of_capture)
            if not exists:
                os.mkdir(date_of_capture)
            to_object_dir = make_dir_for_object(date_of_capture, filename)
            # now go through all the images on from and move
            copy_images(copied_files, object_dir, to_object_dir, "*_Ha_*.fit", "Ha/lights")
            copy_images(copied_files, object_dir, to_object_dir, "*_O_*.fit", "O/lights")
            copy_images(copied_files, object_dir, to_object_dir, "*_S_*.fit", "S/lights")
            copy_images(copied_files, object_dir, to_object_dir, "*.fit", "Color/lights")


if __name__ == '__main__':
    print("foo")
    extract(sys.argv[1:])
# python extract.py /Volumes/ASTRO/ASIAIR/Autorun ~/Desktop/test
