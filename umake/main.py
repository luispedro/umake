import sys
import pathlib
from umake import converters

converters = {
    ('.png', '.svg') : converters.InkscapeConverter(),
    ('.docx', '.md') : converters.PandocConverter(),
}

def main(args=None):
    if args is None:
        args = sys.argv
    target = pathlib.Path(args[1])
    if len(target.suffixes) != 1:
        raise IOError(f'Cannot parse {target}')
    ext1 = target.suffix
    candidates = []
    for c in target.absolute().parent.glob(f'{target.stem}.*'):
        if c.suffix != target.suffix:
            if (target.suffix, c.suffix) in converters:
                candidates.append(c)
    if len(candidates) == 0:
        sys.stderr.write(f'No candidates found for {target}\n')
        return 1
    elif len(candidates) > 1:
        print(f'Multiple candidates found for {target}:')
        for i,c in enumerate(candidates):
            print(f'[{i}] {c}')
        print('Which one do you want to convert?')
        i = int(input())
        c = candidates[i]
    else:
        [c] = candidates
    if target.exists():
        print(f'File {target} already exists. Overwrite?')
        if input() not in ['y', 'Y']:
            return 0
    converters[(target.suffix, c.suffix)](target, c)

if __name__ == '__main__':
    sys.exit(main())
