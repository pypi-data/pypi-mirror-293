import typer
from typing import Optional
import os

import pylagg.cgr.kmer_input as kmer_input

app = typer.Typer()
dir_path = os.path.dirname(os.path.realpath(__file__))

@app.command()
def cgr_generate_single(file_name: str, dest: Optional[str] = None):
    #print(dir_path)
    counts_file_path=dir_path + "/" + file_name
    with open(counts_file_path) as f:
        if(dest):
            path = dest + "/" + file_name + ".png"
            kmer_input.count_file_to_image_file(f, dest + '/' + file_name + '.png')
        else:
            path = dir_path + "/" + file_name + ".png"
            kmer_input.count_file_to_image_file(f, path)

@app.command()
def cgr_generate_batch(file_name: str, dest: Optional[str] = None):
    #kmer_input.counts_zip_to_images_zip(dir_path + '/' + file_name, dir_path + '/' + file_name)
    if(dest):
        kmer_input.counts_zip_to_images_zip(dir_path + '/' + file_name, dest + '/' + file_name)
    else:
        kmer_input.counts_zip_to_images_zip(dir_path + '/' + file_name, dir_path + '/' + file_name)

def cli():
    app()