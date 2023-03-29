import subprocess

class Converter:
    pass

class SubprocessConverter(Converter):
    def __init__(self, **kwargs):
        self.quiet = kwargs.get('quiet', False)

    def build_command(self, target, src):
        raise NotImplementedError

    def __call__(self, target, src):
        command = self.build_command(target, src)
        if not self.quiet:
            print(' '.join(map(str,command)))
        subprocess.check_call(command)

class InkscapeConverter(SubprocessConverter):
    def build_command(self, target, src):
        return ['inkscape'
                , '--export-filename', target
                ,'--export-dpi=300'
                ,src]

class PandocConverter(SubprocessConverter):
    def build_command(self, target, src):
        return ['pandoc',
                src,
                '-o', target]

class XelateXConverter(SubprocessConverter):

    @classmethod
    def register(cls, converters):
        converters['.pdf', '.tex'] = cls()

    def build_command(self, target, src):
        return ['xelatex', src]
