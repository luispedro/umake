from umake import converters as cs

def test_has_conversions():
    assert ('.pdf', '.doc') in cs.registry
    assert ('.pdf', '.docx') in cs.registry
    assert ('.pdf', '.svg') in cs.registry

    assert ('.jpeg', '.heic') in cs.registry

    assert ('.docx', '.pdf') not in cs.registry
