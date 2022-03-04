from http import HTTPStatus
from flask import Flask, jsonify, request, safe_join, send_file, send_from_directory
import os

from app.kenzie import create_dir, filepath_with_safe, show_files, download_query_params


ALLOWED_EXTENSIONS = {"png", "jpg", "gif"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1000 * 1000

IMAGES_DIRECTORY = os.getenv("IMAGES_DIRECTORY")


# CRIA OS DIRETORIO DE IMAGENS
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

    files_list = show_files()

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

    filepath = filepath_with_safe(filename)

    try:
        return send_file(filepath, as_attachment=True), HTTPStatus.OK
    except:
        return {"message": "Arquivo inexistente"}, HTTPStatus.NOT_FOUND


# FAZ O DOWNLOAD DOS ARQUIVOS EM ZIP
@app.get("/download-zip")
def download_zip():

    file_type, file_extension, compression_rate = download_query_params(request.args)

    try:

        abs_path = f"./images/{file_extension}"
        files = os.listdir(abs_path)

        if not files:
            return {
                "message": f"Não existem arquivos com esses formato"
            }, HTTPStatus.NOT_FOUND
        print("aqui")

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
