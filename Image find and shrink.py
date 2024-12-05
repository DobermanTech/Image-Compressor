import os
from PIL import Image
import glob
import shutil

def find_files(folder_path):
    jpeg_files = glob.glob(os.path.join(folder_path, '**', '*.jpg'), recursive= True)
    print(f"Found {len(jpeg_files)} files ending in .jpg")
    return jpeg_files


def copy_the_files(files, src_folder, dst_folder):
    for file in files:
        # Calculate relative path and new destination path
        relative_path = os.path.relpath(file, src_folder)
        new_path = os.path.join(dst_folder, relative_path)
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        shutil.copy2(file, new_path)


def dowwnsize(directory, decide_delete):
    # Use glob to search recursively for .jpg files
    files = glob.glob(os.path.join(directory, '**', '*.jpg'), recursive=True)
    for file_path in files:
        if suffix_to_ignore not in os.path.basename(file_path):
            print(f"Processing file: {file_path}")  # Debugging print
            with Image.open(file_path) as img:
                width, height = img.size
                #print(f"Original size: {width}x{height}")  # Debugging print
                if width < height:
                    new_height = 1440
                    new_width = int((1440 / height) * width)
                else:
                    new_width = 1440
                    new_height = int((1440 / width) * height)
                        
                resized_img = img.resize((new_width, new_height), Image.LANCZOS)
                #print(f"New size: {new_width}x{new_height}")  # Debugging print
                new_filename = f"{os.path.splitext(os.path.basename(file_path))[0]} (Resized for KWA Archive).jpg"
                new_file_path = os.path.join(os.path.dirname(file_path), new_filename)
                resized_img.save(new_file_path, 'JPEG', quality=50)
                if decide_delete.lower() == "y":
                    os.remove(file_path)


def get_relative_paths(files, base_folder, suffix_to_ignore):
    relative_paths = {}
    for file in files:
        relative_path = os.path.relpath(file, base_folder)
        cleaned_path = relative_path.replace(suffix_to_ignore, '')
        relative_paths[cleaned_path] = file
    return relative_paths                                               

def delete_matching_files(src_files, tgt_files):
    for relative_path, src_file in src_files.items():
        if relative_path in tgt_files:
            print(f"Deleting file: {src_file}")  # Debugging print
            os.remove(src_file)
        else:
            print(f"Did not find a matching copy for {src_file}")


number_of_images = 0
suffix_to_ignore = ' (Resized for KWA Archive)'



#Setup Questions

print('By Default, Deleting Source images only works on the source image that is inside the downsized images folder. If downloading images to your machine, choose  Y  to delete. You will recieve an option to delete matching files.')

decide_cache = input("Do you want to create the new files locally in this folder on this computer?(Y/N)")
decide_delete = input("Do you want to delete the Source Images on the fly?(Y/N)")
decide_delete = decide_delete.lower()
decide_cache = decide_cache.lower()
dst_folder = os.path.join(os.getcwd(), 'new images')



#### MAIN LOGIC
while True:
    raw_folder_path = input(r"Where Would you like to search for images?")
    source_folder_path = raw_folder_path.replace('\\', '/')
    jpg_files = find_files(source_folder_path)
    input("Press Enter to continue...")
    if decide_cache == 'n':
        dowwnsize(source_folder_path, decide_delete)
    elif decide_cache == 'y':
        copy_the_files(jpg_files, source_folder_path, dst_folder)
        dowwnsize(dst_folder, decide_delete)
    ##In case working remotely and desiring deletion
    if decide_cache == 'y' and decide_delete == 'y':
        
        print("Content Aware Deletion: comparing the downsampled list to Original list")
        # Input directories from the user
        # Find files in both directories
        print('Files found in the source directory:')
        src_files = find_files(source_folder_path)
        print('Files found on your computer:')
        tgt_files = find_files(dst_folder)
        
        # Get relative paths
        src_files_rel = get_relative_paths(src_files, source_folder_path, '')
        tgt_files_rel = get_relative_paths(tgt_files, dst_folder, suffix_to_ignore)
        delete_match = input('Would you like to delete all the Source files that match ones you just made? (Y/N)').lower()
        if delete_match == 'y':
            # Delete matching files in the source directory
            delete_matching_files(src_files_rel, tgt_files_rel)

    repeat = input('Would you like to scrape a different folder with the same (Y/N) settings? (y/n)').lower()
    if repeat !='y':
        break

