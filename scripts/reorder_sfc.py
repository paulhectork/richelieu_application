# ***************************************************************
# so far, the vue sfc files are usually in order:
# <intro comment> - <template> - <script> - <style>
# batch-reorder them to:
# <template starting with intro comment> - <script> - <style>
# the reason is that the starting comment messes up github's 
# code syntax highlighting
# ***************************************************************

import re
import os
import shutil
import argparse
import typing as t

# ***************************************************************

CURDIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
FRONTEND = os.path.abspath(os.path.join(CURDIR, os.pardir, "frontend/"))
BACKUP = os.path.abspath(os.path.join(CURDIR, os.pardir, "frontend.bak/"))

# ***************************************************************

to_pattern = lambda start_tgt, end_tgt: (
    re.compile(rf"""
               ((?<=^)|(?<=\n))  # start of file or newline
                    <{start_tgt}>   # start tag
                        (.|\n)+?    # content
                    </{end_tgt}>    # end tag
                  ((?=$)|(?=\n))   # end of file or newline
                """
              , re.VERBOSE) )

template_pattern = to_pattern(r"template", r"template")
script_pattern   = to_pattern(r"script\s?(setup)?", r"script")
style_pattern    = to_pattern(r"style\s?(scoped)?", r"style")

def do_backup():
    """backup the full frontend"""
    if os.path.isdir(BACKUP):
        shutil.rmtree(BACKUP)
    shutil.copytree(FRONTEND, BACKUP)


def get_files() -> t.List:
    """retrieve all paths to `.vue` files and return them as an array"""
    vuefiles = []  # path to all matched files
    for root, dirs, files in os.walk(FRONTEND):
        vuefiles = vuefiles + [ os.path.join(root, f) 
                                for f in files 
                                if re.search(r"\.vue$", f) ]
    assert all(os.path.isfile(f) for f in vuefiles)
    return vuefiles


def reorder_file(fp:str, writefiles:bool) -> None:
    """
    open the file. if it contains a starting comment, 
    move that comment at the start of the template and
    update the file

    :param fp: path of the file to process
    :param writefiles: write the files instead of just printing the result
    """
    with open(fp, mode="r") as fh:
        filecontent = fh.read()
    
    # extract the different parts
    filecontent = re.sub(r"^[\s\t\n]*", "", filecontent)
    filecontent = re.sub(r"[\s\t\n]*$", "", filecontent)
    comment = re.search(r"^(\<\!\-\-(.|\n)+?\-\-\>)", filecontent)
    comment = comment[1] if comment else ""
    template = re.search(template_pattern, filecontent)
    template = template[0] if template else ""
    script = re.search(script_pattern, filecontent)
    script = script[0] if script else ""
    style = re.search(style_pattern, filecontent)
    style = style[0] if style else ""

    assert len(template) != 0 or len(script) != 0 or len(style) != 0, \
      f"{fp} : expected non-null length for `template`, `script`, `style`, got `{len(template)}, `{len(script)}, `{len(style)}`"
    if not comment:
        print(f"* no leading comment in file. not processing `{os.path.basename(fp)}`")
        return
    
    # reindent the comment
    comment = re.sub(r"^", "  ", comment, flags=re.MULTILINE)
    # move the comment at the start of `template`
    template = re.sub(r"^[\s\n\t]*<template>", "", template)
    template = f"<template>\n\n{comment}\n\n" + template
    # reorder `filecontent`
    filecontent = f"{template}\n\n\n{script}\n\n\n{style}\n"

    # update the files if writefiles, else do a dry run.
    if writefiles:
        with open(fp, mode="w") as fh:
            fh.write(filecontent)
    else:
        print("-------------------------------------------------------")
        print(fp)
        print(filecontent)
    return


# ***************************************************************

def prompt_run():
    cont = input("continue? [y/n]")
    if cont not in ["y","n"]:
        print("answer must be one of ['y', 'n']")
        prompt_run()
    else:
        return cont == "y"


if __name__ == "__main__":
    parser = argparse.ArgumentParser( prog="reorder_sfc"
                                    , usage="python reorder-src -w"
                                    , description="reorder your Vue from the format: \n<intro comment> - <template> - <script> - <style> to the format: \n<template starting with intro comment> - <script> - <style>. WARNING: CAN ONLY BE DONE ONCE AND WILL OVERWRITE YOUR FILES.")
    parser.add_argument( "-w"
                       , "--writefiles"
                       , help="write the reformatted version to file"
                       , action="store_true")
    args = parser.parse_args()

    print("\nWARNING : this only works if your files have the structure: \n```\n<!-- intro comment -->?\n<template/>\n<script/>\n<style/>\n```\n if option `writefiles` is provided, IT WILL OVERWRITE ALL YOUR FILES (a backup will be made before each run).")
    
    if prompt_run():
        print("* running...")
        do_backup()
        vuefiles = get_files()
        for fp in vuefiles:
            reorder_file(fp, args.writefiles)
        print("* pre-rewrite backup written to `frontend.bak/`")    
    else:
        print("* exiting")