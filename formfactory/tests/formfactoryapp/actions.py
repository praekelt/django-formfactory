from formfactory import actions


@actions.register
def dummy_action(form_instance):
    return True


@actions.register
def store_form_data(form_dict, **kwargs):
    """
    Test wizard action to save each form's data
    """
    for key, form in form_dict.items():
        form.save()
