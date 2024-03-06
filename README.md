# UMake

`umake` is a simple command line tool to convert files from one format to another.

It is best illustrated with an example: if you have a file called `file.docx`
and you want to convert it to `file.pdf`, you can use `umake` to do it.

```bash
umake file.pdf
```

This will call `libreoffice` on the command line to convert the file to `pdf`.

Currently supported transformations:

- `SVG` to `PNG`/`SVG`: `umake file.pdf` (uses [inkscape](https://inkscape.org/) on the command line)
- `DOCX`/`DOC`/`ODT` to `PDF`: `umake file.pdf` (uses libreoffice on the command line)
- `MD` to `DOCX`: `umake file.docx` (uses [pandoc](https://pandoc.org/) on the command line)


