import subprocess

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

class PandocConverter(SubprocessConverter):
    _conversions = [('.docx', '.md')]
    def build_command(self, target, src):
        return ['pandoc',
                src,
                '-o', target]

class XelateXConverter(SubprocessConverter):
    _conversions = [('.pdf', '.tex')]

    def build_command(self, target, src):
        return ['xelatex', src]
