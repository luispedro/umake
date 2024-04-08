import subprocess

registry = {}

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
        command = self.build_command(target, src)
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
    _conversions = [('.docx', '.md')]
    def build_command(self, target, src):
        return ['pandoc',
                src,
                '-o', target]

@register_converter
class XelateXConverter(SubprocessConverter):
    _conversions = [('.pdf', '.tex')]

    def build_command(self, target, src):
        return ['xelatex', src]

@register_converter
class LibreOfficeConverter(SubprocessConverter):
    _conversions = [('.pdf', '.docx'),
                    ('.pdf', '.doc'),
                    ('.pdf', '.odt'),
                    ('.pdf', '.rtf'),
                   ]
    def build_command(self, target, src):
        return ['libreoffice',
                '--headless',
                '--convert-to', 'pdf',
                src]

