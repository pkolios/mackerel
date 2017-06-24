from mackerel import navigation


def test_navigation(build_documents):
    nav = navigation.Navigation(build_documents)
    assert nav._build_documents == build_documents
