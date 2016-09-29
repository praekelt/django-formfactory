from formfactory import actions


@actions.register
def dummy_action():
    return True
