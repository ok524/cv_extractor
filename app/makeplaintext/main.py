import os
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from dotenv import load_dotenv
load_dotenv()

from util.util import lower, vars

import json
import time
import datetime
import logging
import logging.config
import argparse

import tika
from tika import parser as tika_parser

def makeplaintext():
    return 'a'

def output2text(text, filename, hash_val="", outputfolder="./output_files"):
    """
    Output to plaintext file
    """
    ts = time.strftime("%Y%m%d-%H%M%S")
    if outputfolder is None:
        outputfolder="./output_files"

    with open(f"{outputfolder}/converted_{filename}_{hash_val}.txt", "w+", encoding="utf-8") as f:
        f.write(text)

    return f"{outputfolder}/converted_{filename}_{hash_val}.txt"


def convert2text(filepath, filename, hash_val="", outputfolder="./output_files"):
    """
    Call Apache Tika to convert docx to text
    """
    text = ""
    stats = {}
    stats["STATUS"] = "Success"
    process_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start_time = time.time()

    if not os.path.exists(filepath):
        logging.error(f"Filepath not found: {filepath}.\n")
        raise Exception("filepath not found.")
        return

    if not filetype(filepath):
        logging.error(f"File {filename} has filetype: {filetype}, is not supported.\n")
        raise Exception("filetype is not supported.")
        return

    if not filesize(filepath):
        logging.warning(f"File size is over limit: {filepath}\n")
        raise Exception("File size is over limit.")
        return

    print(f"> Processing: {filepath}")
    try:
        parsed = tika_parser.from_file(filepath)
        print(f"\n> Metadata:\n{parsed['metadata']}\n\n")
        text = parsed["content"]
        text = text.strip("\n")
    except Exception as e:
        stats["STATUS"] = "Failed"
        logging.error(f"[Error] Convert error: {e}\n", exc_info=True)
        pass

    ## Remove Page Numbers in Word
    if filepath.endswith(".docx"):
        textlist = text.split("\n")

        for i in range(0, len(textlist)):
            if textlist[i] == ("2"):
                textlist[i]=""

        text = "\n".join(textlist)

    stats["data"] = text
    stats["file_time_proceessed"] = process_time
    stats["time_process"] = float("{:.3f}".format(time.time() - start_time))

    # ## Output JSON
    # with open(f"{outputfolder}/task_{process_time}_{filename}.json", "w") as f:
    #     json.dump(stats, f, indent=4, ensure_ascii=False)
    #     print("Statistics Generated. Please check the output on output_files folder")

    ## Output plaintext
    return output2text(text, filename, hash_val, outputfolder)


def filetype(filepath):
    """
    Check if file type is supported
    """
    return filepath.endswith(".docx") or filepath.endswith(".pdf")


def filesize(filepath):
    """
    Check if file size is within bounds (< 50MB)
    """
    return (os.stat(filepath).st_size < 50000000)

def create_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                    description="""\
                Convert .docx content to plaintext
                --------------------------------
                    The file produced by this
                        program is json
                        You can find them in
                    folder "result/<file_name> 

        Output: converted_<file_name>_.json

        Example: python run_tika.py ./input.docx -o ./
                                    """)
    parser.add_argument("filepath", type=str, help="File path of docx file.")
    parser.add_argument("-o", "--outputfolder", help="Folder of output.")
    return parser

if __name__ == "__main__":

    variables = vars()

    filepath = variables['PDFPATH']
    outputfolder = variables['PLAINTEXT_FOLDER']

    if outputfolder is None:
        outputfolder="./output_files"
    if not os.path.exists(outputfolder):
        os.makedirs(outputfolder)

    arr_folder = filepath.split("/")
    filename = arr_folder[len(arr_folder) - 1]

    print(filename)

    # ## Setup logger
    # logger = logging.getLogger(__name__)
    # logging.basicConfig(filename=f"{outputfolder}/app.log", filemode="a", format = "%(asctime)s - %(message)s", level = logging.INFO, datefmt="%Y-%m-%d %H:%M:%S %z")

    ## Main process
    text = ""
    try:
        text = convert2text(filepath, filename, outputfolder)
        print(text)
    except Exception as e:
        print(f"Main process error: {e}.\n")
        # logging.error(f"Main process error: {e}.\n", exc_info=True)
        pass
