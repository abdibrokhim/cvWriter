from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
import uvicorn
import json
import openai
from starlette.responses import FileResponse

from copilot import Copilot
import pdf_writer
import pdf_reader

import sys

sys.dont_write_bytecode = True

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import django

django.setup()

from app import models

from asgiref.sync import sync_to_async

@sync_to_async
def _post_client(username, password):
    try:
        models.Client(
            username=username,
            password=password,
        ).save()

        return True
    except Exception as e:
        print(e)
        return False

@sync_to_async
def _is_client(username):
    return models.Client.objects.filter(username=username).exists()

@sync_to_async
def _get_client(username):
    return models.Client.objects.filter(username=username).values()


app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/v1/api/cover-letter/')
async def generate_cover_letter(resume: str, job: str):
    copilot = Copilot()
    a = copilot.get_cover_letter(resume, job)
    f = pdf_writer.get_pdf(a)

    return {"filename": f}


@app.post('/v1/api/resume/')
async def generate_resume(resume: str, job: str):
    copilot = Copilot()
    a = copilot.get_resume(resume, job)
    f = pdf_writer.get_pdf(a)

    return {"filename": f}


@app.post('/v1/api/cover-letter/upload-file/')
async def generate_cover_letter_by_file_upload(file: UploadFile, job: str):
    pdf_txt = pdf_reader.read_pdf(file.file)

    copilot = Copilot()
    a = copilot.get_cover_letter(pdf_txt, job)
    f = pdf_writer.get_pdf(a)

    return {"filename": f}


@app.post('/v1/api/resume/upload-file/')
async def generate_resume_by_file_upload(file: UploadFile, job: str):
    pdf_txt = pdf_reader.read_pdf(file.file)
    
    copilot = Copilot()
    a = copilot.get_resume(pdf_txt, job)
    f = pdf_writer.get_pdf(a)

    return {"filename": f}


@app.get('/v1/api/login/')
async def login(email: str, password: str):

    is_client = await _is_client(email)

    if not is_client:
        return {"status": "user does not exist", "key": 404}

    client = await _get_client(email)

    if client[0]['password'] != password:
        return {"status": "wrong password", "key": 202}

    return {"status": "successefully logged in", "key": 200}


@app.post('/v1/api/signup/')
async def signup(email: str, password: str):

    is_client = await _is_client(email)

    if is_client:
        return {"status": "user already exists", "key": 202}

    post = await _post_client(email, password)

    if post:
        return {"status": "successefully signed up", "key": 200}
    else:
        return {"status": "failed to signup", "key": 404}
