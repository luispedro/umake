import pytest

from umake.main import main, parse_args


def test_no_arguments_exits():
    with pytest.raises(SystemExit):
        parse_args([])


def test_parse_target():
    args = parse_args(['file.pdf'])
    assert args.target.name == 'file.pdf'


def test_supports_without_target():
    args = parse_args(['--supports', 'docx', 'pdf'])
    assert args.target is None
    assert args.supports == ['docx', 'pdf']


def test_no_suffix(capsys):
    assert main(['Makefile']) == 1
    assert 'no suffix' in capsys.readouterr().err


def test_candidate_selection_rejects_bad_input(tmp_path, monkeypatch):
    from umake import converters as cs
    (tmp_path / 'doc.md').write_text('')
    (tmp_path / 'doc.docx').write_text('')
    converted = []
    class FakeConverter:
        def __call__(self, target, src):
            converted.append(src)
    monkeypatch.setitem(cs.registry, ('.pdf', '.md'), FakeConverter())
    monkeypatch.setitem(cs.registry, ('.pdf', '.docx'), FakeConverter())
    answers = iter(['not a number', '7', '-1', '0'])
    monkeypatch.setattr('builtins.input', lambda: next(answers))
    monkeypatch.chdir(tmp_path)
    main(['doc.pdf'])
    assert len(converted) == 1


def test_list(capsys):
    assert main(['--list']) == 0
    out = capsys.readouterr().out
    assert 'docx -> pdf' in out
    assert 'svg -> png' in out
