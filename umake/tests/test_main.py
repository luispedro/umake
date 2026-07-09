import pytest

from umake.main import parse_args


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
