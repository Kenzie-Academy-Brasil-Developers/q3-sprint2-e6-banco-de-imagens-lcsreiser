from http import HTTPStatus
from flask import Flask, jsonify, request, safe_join, send_file, send_from_directory
import os

ALLOWED_EXTENSIONS = {"png", "jpg", "gif"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1000 * 1000

IMAGES_DIRECTORY = os.getenv("IMAGES_DIRECTORY")


# CRIA OS DIRETORIO DE IMAGENS
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


create_dir()


@app.post("/upload")
def post_multipart_file():

    try:
        files = request.files["file"]
        image_name = files.filename
        image_extension = image_name[-3::]

        if image_extension not in ALLOWED_EXTENSIONS:
            return {
                "message": "Extensão de arquivo não suportada"
            }, HTTPStatus.UNSUPPORTED_MEDIA_TYPE

        for file in os.listdir(f"./images/{image_extension}"):
            if image_name == file:
                return {"message": "Nome de arquivo já existente"}, HTTPStatus.CONFLICT
        print("aqui")

        files.save(f"./images/{image_extension}/{files.filename}")

        return {"message": "Upload realizado com sucesso!"}, HTTPStatus.CREATED
    except:
        return {
            "message": "Arquivo é maior do que 1mb"
        }, HTTPStatus.REQUEST_ENTITY_TOO_LARGE


# MOSTRA TODOS OS ARQUIVOS
@app.get("/files")
def show_all_files():

    files_list = []

    files_png = os.listdir("./images/png")
    file_jpg = os.listdir("./images/jpg")
    file_gif = os.listdir("./images/gif")

    files_list.extend(files_png + file_jpg + file_gif)

    return jsonify(files_list), HTTPStatus.OK


# MOSTRA SÓ OS ARQUIVOS COM O FORMATO DESEJADO
@app.get("/files/<file_format>")
def show_extension_files(file_format):

    try:
        files_list = os.listdir(f"./images/{file_format}")
        return jsonify(files_list), HTTPStatus.OK
    except:
        return {"message": "Formato inválido"}, HTTPStatus.NOT_FOUND


# FAZ O DOWNLOAD DOS ARQUIVOS
@app.get("/download/<filename>")
def download(filename: str):
    file_extension = filename[-3::]
    abs_path = os.path.abspath(f"./images/{file_extension}")
    filepath = safe_join(abs_path, filename)

    try:
        return send_file(filepath, as_attachment=True), HTTPStatus.OK
    except:
        return {"message": "Arquivo inexistente"}, HTTPStatus.NOT_FOUND


# FAZ O DOWNLOAD DOS ARQUIVOS EM ZIP
@app.get("/download-zip")
def download_zip():

    default_extension = "jpg"
    file_type = request.args.get("file_type")
    file_extension = file_type if file_type else default_extension
    compression_rate = request.args.get("compression_rate", 6)

    try:

        abs_path = f"./images/{file_extension}"
        files = os.listdir(abs_path)

        if not files:
            return {
                "message": f"Não existem arquivos com esses formato"
            }, HTTPStatus.NOT_FOUND
        print("aqui")
        # os.system(f"zip -{compression_rate} -r -j /tmp/{file_extension}")
        os.system(
            f"zip -r /tmp/{file_extension} {IMAGES_DIRECTORY}/{file_type} -{compression_rate}"
        )

        return (
            send_from_directory(
                directory="/tmp/", path=f"{file_extension}.zip", as_attachment=True
            ),
            HTTPStatus.OK,
        )

    except:
        return {"message": "Extensão inválida"}, HTTPStatus.BAD_REQUEST
