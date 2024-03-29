from django import forms

"""
Пример вывода select с редактирвоанием объекта:
    contractor = MyModelChoiceField(required=False,
                                    queryset=Contractor.objects.all(),
                                    widget=CustomSelect(attrs={
                                        'class': 'edit-select',
                                        'onchange': 'append_to_a(this, "contractor");'
                                    }))
"""
class CustomSelect(forms.Select):
    template_name = 'widgets/select.html'
    # input_type = 'select'
    # option_template_name = 'crm/widgets/select_option.html'
    # add_id_index = False
    # checked_attribute = {'selected': True}
    # option_inherits_attrs = False

    def __init__(self, attrs=None, choices=()):
        self.custom_attrs = {}
        super().__init__(attrs, choices)

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        index = str(index) if subindex is None else "%s_%s" % (index, subindex)
        if attrs is None:
            attrs = {}
        option_attrs = self.build_attrs(self.attrs, attrs) if self.option_inherits_attrs else {}
        if selected:
            option_attrs.update(self.checked_attribute)
        if 'id' in option_attrs:
            option_attrs['id'] = self.id_for_label(option_attrs['id'], index)

        # setting the attributes here for the option
        if len(self.custom_attrs) > 0:
            if value in self.custom_attrs:
                custom_attr = self.custom_attrs[value]
                for k, v in custom_attr.items():
                    option_attrs.update({k: v})

        return {
            'name': name,
            'value': value,
            'label': label,
            'selected': selected,
            'index': index,
            'attrs': option_attrs,
            'type': self.input_type,
            'template_name': self.option_template_name,
        }

class MyModelChoiceField(forms.ModelChoiceField):

    # custom method to label the option field
    def label_from_instance(self, obj):
        # since the object is accessible here you can set the extra attributes
        if hasattr(obj, 'type'):
            self.widget.custom_attrs.update({obj.pk: {'type': obj.type}})
        return obj.__str__()