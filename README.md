# UMake

`umake` is a simple command line tool to convert files from one format to another.

It is best illustrated with an example: if you have a file called `file.docx`
and you want to convert it to `file.pdf`, you can use `umake` to do it.

```bash
umake file.pdf
```

This will call `libreoffice` on the command line to convert the file to `pdf`.

Currently supported transformations:

- `SVG` to `PNG`/`PDF`: `umake file.png` or `umake file.pdf` (uses [inkscape](https://inkscape.org/) on the command line)
- `DOCX`/`DOC`/`ODT`/`RTF` to `PDF`: `umake file.pdf` (uses `libreoffice` on the command line)
- `XLSX`/`XLS`/`ODS` to `CSV`: `umake file.csv` (uses `libreoffice` on the command line)
- `TEX` to `PDF`: `umake file.pdf` (uses `xelatex` on the command line)
- `MD` to `DOCX`/`PDF`/`HTML`: `umake file.docx`, `umake file.pdf`, or `umake file.html` (uses [pandoc](https://pandoc.org/) on the command line)
- `DOCX` to `MD`: `umake file.md` (uses `pandoc` on the command line)
- `HEIC` to `JPEG`/`JPG`/`PNG`: `umake file.jpeg` or `umake file.png` (uses `heif-convert` on the command line)
- `PNG` to `JPG` and `JPG` to `PNG`: `umake file.jpg` or `umake file.png` (uses `convert` from ImageMagick)


