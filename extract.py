import datetime
import glob
import os
import sys
import shutil


# map file format of ASIAIR to one that Siril can use
# example usage  python extract.py /Volumes/ASTRO/ASIAIR/Autorun ~/Desktop/test
# ./Lights/M31/*.fits -> ./11-2-22/M31/Ha/lights/*.fits


def make_dir_for_spectrum(obj, spectrum_name):
    spectrum_dir = os.path.join(obj, spectrum_name)
    os.mkdir(spectrum_dir)
    os.mkdir(os.path.join(spectrum_dir, "lights"))
    os.mkdir(os.path.join(spectrum_dir, "darks"))
    os.mkdir(os.path.join(spectrum_dir, "flats"))


def make_dir_for_object(date_dir, object_name):
    spectrums = ["Ha", "S", "O", "RGB", "R", "G", "B", "NONE"]

    obj = os.path.join(date_dir, object_name)
    os.mkdir(obj)

    for spectrum in spectrums:
        make_dir_for_spectrum(obj, spectrum)

    return obj


def copy_images(copied_set, from_path, to_path, file_pattern, sub_dir):
    print(from_path, to_path, file_pattern, sub_dir)
    lights = os.path.join(from_path, file_pattern)

    files_copied = 0
    to_dest = os.path.join(to_path, sub_dir)
    exists = os.path.exists(to_dest)
    if not exists:
        return 0

    for filename in glob.glob(lights):
        print("Moving " + filename + " to " + to_dest)
        if filename not in copied_set:

            files_copied = files_copied + 1
            shutil.copy(filename, to_dest)
            copied_set.add(filename)

    return files_copied


def extract(argv):
    in_path = sys.argv[1]
    out_path = sys.argv[2]
    copied_files = {""}

    print(in_path + " " + out_path)
    lights = os.path.join(in_path, "Light")

    for filename in os.listdir(lights):
        object_dir = os.path.join(lights, filename)
        if os.path.isdir(object_dir):

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
            ha_count = copy_images(copied_files, object_dir, to_object_dir, "*_Ha_*.fit", "Ha/lights")
            o_count = copy_images(copied_files, object_dir, to_object_dir, "*_O_*.fit", "O/lights")
            s_count = copy_images(copied_files, object_dir, to_object_dir, "*_S_*.fit", "S/lights")
            none_count = copy_images(copied_files, object_dir, to_object_dir, "*_NONE_*.fit", "S/lights")
            rgb_count = copy_images(copied_files, object_dir, to_object_dir, "*.fit", "RGB/lights")


if __name__ == '__main__':
    print("foo")
    extract(sys.argv[1:])
