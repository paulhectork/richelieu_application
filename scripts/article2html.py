import argparse
import shutil
import os
import re


# *************************************************************
# read a .txt file containing an article text (directly
# copy/pasted from the INHA cloud) and transform it into
# an HTML blob.
#
# THIS DOES NOT PROCESS:
# * footnotes
# * images
# * hyperlinks
# * images and any other kind of markup that isn't
#   visible in a raw text file
# both of these will have to be added manually
# *************************************************************


def txt2html(txt:str) -> str:
    """transform an article copied from the INHA cloud into an HTML blob"""
    roman_regex = re.compile(r"""(?<=\W)              # non-word before
                                 (?=[A-Z]{2,})        # match will contain at least 2 uppercase chars (else it will match all words with uppercase)
                                 (                    # 1st group: the roman number
                                     M{0,4}
                                     (CM|CD|D?C{0,3})
                                     (XC|XL|L?X{0,3})
                                     (IX|IV|V?I{0,3})
                                 )
                                 ([a-zéè])+           # 5th group: `e`, `ème`... (suffix of the roman number)
                                 (?=\W)               # non-word after
                              """, re.VERBOSE)
    txt = (txt.replace("’", "'")                            # d', l'... : replace fancy apostrophes by "'".
              .replace(" ", " "))                           # the cloud adds this weird space. replace it by a normal space
    txt = re.sub(r"^\s+", "", txt)                          # strip leading spaces
    txt = re.sub(r"\s+$", "", txt)                          # strip trailing spaces
    txt = re.sub(r"[«“] ?", r"<q>&nbsp;", txt)                 # add opening quote
    txt = re.sub(r" ?[»”]", r"&nbsp;</q>", txt)                # add closing quote
    txt = re.sub(r" ([\:\;\?\!])", r"&nbsp;\1", txt)              # add non-breakable space before `;` and `:`
    txt = re.sub(r"^(.+)$", r"<p>\1</p>", txt, flags=re.M)  # create html paragraphs
    txt = re.sub(roman_regex, r"\1<sup>\5</sup>", txt)      # exposant en superscript
    txt = re.sub(r"(.{50}[^ ]+)", r"\1\n", txt)             # return carriage every 50 chars
    txt = re.sub(r"</p>", r"\n</p>", txt)                   # line jump for closing paragraph
    txt = re.sub(r"\n+", r"\n", txt)                        # normalize line jumps
    txt = re.sub(r"<p>[\s\n]*</p>", "\n", txt)              # remove empty paragraphs that we inserted
    txt = re.sub(r"^\s+", "", txt, flags=re.M)              # strip leading spaces
    txt = re.sub(r"\s+$", "", txt, flags=re.M)              # strip trailing spaces
    txt = re.sub(r"^(?!\</?p\>)", "  ", txt, flags=re.M)    # add indentation
    return txt


if __name__ == "__main__":
    parser = argparse.ArgumentParser( prog="article2html"
                                    , description="read a `.txt` file containing an article text (directly copy/pasted from the INHA cloud) and transform it into an HTML blob. print and exit."
                                    )
    parser.add_argument("filename", help="the filename to process")

    args = parser.parse_args()

    with open(args.filename, mode="r") as fh:
        txt = fh.read()
    txt = txt2html(txt)
    try: l = shutil.get_terminal_size().columns
    except: l = 60
    print("\n" + "*" * l)
    print(txt)
    print("*" * l, "\n")




