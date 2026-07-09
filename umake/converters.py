import pathlib
import subprocess

registry = {}

def _rename_output(target, src):
    '''libreoffice and xelatex name their output after the source stem, so
    move it onto the target if the names differ'''
    target = pathlib.Path(target).absolute()
    produced = target.with_name(pathlib.Path(src).stem + target.suffix)
    if produced != target:
        produced.replace(target)

def register_converter(cls):
    cls.register(registry)


class Converter:
    pass

class SubprocessConverter(Converter):
    def __init__(self, **kwargs):
        self.quiet = kwargs.get('quiet', False)

    @classmethod
    def register(cls, registry):
        for k in cls._conversions:
            registry[k] = cls()

    def build_command(self, target, src):
        raise NotImplementedError

    def __call__(self, target, src):
        command = self.build_command(str(target), str(src))
        if not self.quiet:
            print(' '.join(map(str,command)))
        subprocess.check_call(command)

@register_converter
class InkscapeConverter(SubprocessConverter):
    _conversions = [
                ('.pdf', '.svg'),
                ('.png', '.svg'),
                ]
    def build_command(self, target, src):
        return ['inkscape'
                , '--export-filename', target
                ,'--export-dpi=300'
                ,src]

@register_converter
class PandocConverter(SubprocessConverter):
    _conversions = [
        ('.docx', '.md'),
        ('.pdf', '.md'),
        ('.html', '.md'),
        ('.md', '.docx'),
    ]

    def build_command(self, target, src):
        return [
            'pandoc',
            src,
            '-o',
            target,
        ]

@register_converter
class XelateXConverter(SubprocessConverter):
    _conversions = [('.pdf', '.tex')]

    def build_command(self, target, src):
        return ['xelatex',
                '-output-directory', str(pathlib.Path(target).absolute().parent),
                src]

    def __call__(self, target, src):
        # run twice so cross-references and tables of contents are up to date
        super().__call__(target, src)
        super().__call__(target, src)
        _rename_output(target, src)


@register_converter
class LibreOfficeConverter(SubprocessConverter):
    _conversions = [('.pdf', '.docx'),
                    ('.pdf', '.doc'),
                    ('.pdf', '.odt'),
                    ('.pdf', '.rtf'),
                    ('.csv', '.xlsx'),
                    ('.csv', '.xls'),
                    ('.csv', '.ods'),
                   ]
    def build_command(self, target, src):
        if target.endswith('.pdf'):
            to = 'pdf'
        elif target.endswith('.csv'):
            to = 'csv'
        else:
            raise NotImplementedError(f'LibreOfficeConverter: Conversion to {target} not implemented')
        return ['libreoffice',
                '--headless',
                '--convert-to', to,
                '--outdir', str(pathlib.Path(target).absolute().parent),
                src]

    def __call__(self, target, src):
        super().__call__(target, src)
        _rename_output(target, src)


@register_converter
class HeifConverter(SubprocessConverter):
    _conversions = [('.jpeg', '.heic'),
                    ('.jpg',  '.heic'),
                    ('.png',  '.heic'),
                   ]
    def build_command(self, target, src):
        return ['heif-convert', src, target]


@register_converter
class ImageMagickConverter(SubprocessConverter):
    _conversions = [
        ('.jpg', '.png'),
        ('.png', '.jpg'),
    ]

    def build_command(self, target, src):
        return ['convert', src, target]

