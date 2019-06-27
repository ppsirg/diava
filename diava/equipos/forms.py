class EquipoForm(forms.form):
    # TODO: Define form fields here

    def __init__(self, *args, **kwargs):
        super(EquipoForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(EquipoForm, self).clean()
        return cleaned_data

    def save(self):
        cleaned_data = super(EquipoForm, self).clean()
