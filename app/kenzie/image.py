import os

from flask import request, safe_join


def create_dir():

    try:
        path_images = os.path.join("./", "images")
        path_png = os.path.join("./images", "png")
        path_jpg = os.path.join("./images", "jpg")
        path_gif = os.path.join("./images", "gif")

        os.makedirs(path_images)
        os.makedirs(path_png)
        os.makedirs(path_jpg)
        os.makedirs(path_gif)
    except:
        ...


def show_files():
    files_list = []

    files_png = os.listdir("./images/png")
    file_jpg = os.listdir("./images/jpg")
    file_gif = os.listdir("./images/gif")

    files_list.extend(files_png + file_jpg + file_gif)

    return files_list


def filepath_with_safe(filename):
    file_extension = filename[-3::]
    abs_path = os.path.abspath(f"./images/{file_extension}")
    filepath = safe_join(abs_path, filename)

    return filepath


def download_query_params(request):
    default_extension = "jpg"
    # file_type = request.args.get("file_type")
    file_type = request.get("file_type")
    file_extension = file_type if file_type else default_extension
    # compression_rate = request.args.get("compression_rate", 6)
    compression_rate = request.get("compression_rate", 6)

    return file_type, file_extension, compression_rate
