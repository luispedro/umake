import sys
import pathlib
from umake import converters as cs

registry = {}
for c in [cs.XelateXConverter,
         cs.InkscapeConverter,
         cs.PandocConverter,
         cs.LibreOfficeConverter]:
    c.register(registry)

def parse_args(args):
    '''Parse command line arguments
    Valid examples:

    umake file.pdf
    umake --force file.pdf

    '''
    import argparse
    parser = argparse.ArgumentParser(description='Convert files')
    parser.add_argument('target', type=pathlib.Path, help='Target file to generate')
    parser.add_argument('--force', action='store_true', help='Execute even if target file exists')
    return parser.parse_args(args)


def main(args=None):
    args = parse_args(sys.argv[1:] if args is None else args)
    target = args.target
    if len(target.suffixes) != 1:
        raise IOError(f'Cannot parse {target}')
    ext1 = target.suffix
    candidates = []
    for c in target.absolute().parent.glob(f'{target.stem}.*'):
        if c.suffix != target.suffix:
            if (target.suffix, c.suffix) in registry:
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
        is_newer = target.stat().st_mtime > c.stat().st_mtime
        print(f'File {target} already exists ({"and is newer" if is_newer else "but is older"})', end=' ')
        if not args.force:
            print('Do you want to overwrite it? [y/N]')
            if input() not in ['y', 'Y']:
                return 0
        else:
            print('Overwriting')
    registry[(target.suffix, c.suffix)](target, c)

if __name__ == '__main__':
    sys.exit(main())
