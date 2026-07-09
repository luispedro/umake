from umake import converters as cs

def test_has_conversions():
    assert ('.pdf', '.doc') in cs.registry
    assert ('.pdf', '.docx') in cs.registry
    assert ('.pdf', '.svg') in cs.registry

    assert ('.jpeg', '.heic') in cs.registry

    assert ('.jpg', '.png') in cs.registry
    assert ('.png', '.jpg') in cs.registry
    assert ('.md', '.docx') in cs.registry
    assert ('.pdf', '.md') in cs.registry

    assert ('.docx', '.pdf') not in cs.registry


def test_build_command_output_directory():
    cmd = cs.registry[('.pdf', '.docx')].build_command('/some/dir/report.pdf', '/some/dir/report.docx')
    assert cmd[cmd.index('--outdir') + 1] == '/some/dir'

    cmd = cs.registry[('.csv', '.xlsx')].build_command('/some/dir/table.csv', '/some/dir/table.xlsx')
    assert cmd[cmd.index('--outdir') + 1] == '/some/dir'

    cmd = cs.registry[('.pdf', '.tex')].build_command('/some/dir/report.pdf', '/some/dir/report.tex')
    assert cmd[cmd.index('-output-directory') + 1] == '/some/dir'
