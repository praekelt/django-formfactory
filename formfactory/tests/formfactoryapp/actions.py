from formfactory import actions


@actions.register
def dummy_action(form_instance):
    return True


@actions.register
def dummy_wizard_action(form_dict, **kwargs):
    return True
