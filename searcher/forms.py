from django import forms
from searcher.models import Exploit, Shellcode


OPERATOR_CHOICES = [
        (0, u'AND'),
        (1, u'OR'),
    ]


def get_type_values():
    """
    Get a list containing all the values that 'vulnerability_type' attribute can assume.
    :return: a list containing all the values that 'vulnerability_type' attribute could assume.
    """
    index = 1
    type_choices = [(0, 'All')]
    type_list = []
    queryset = Exploit.objects.order_by().values('vulnerability_type').distinct().exclude(vulnerability_type__exact='')
    for vulnerability_type in queryset:
        type_list.append(dict(vulnerability_type).get('vulnerability_type'))
    queryset = Shellcode.objects.order_by().values('vulnerability_type').distinct().exclude(vulnerability_type__exact='')
    for vulnerability_type in queryset:
        if not type_list.__contains__(dict(vulnerability_type).get('vulnerability_type')):
            type_list.append(dict(vulnerability_type).get('vulnerability_type'))
    type_list = sorted(type_list)
    for vulnerability_type in type_list:
        type_choices.append((index, vulnerability_type))
        index = index + 1
    return type_choices


def get_platform_values():
    """
    Get a list containing all the values that 'platform' attribute can assume.
    :return: a list containing all the values that 'platform' attribute could assume.
    """
    index = 1
    platform_choices = [(0, 'All')]
    platform_list = []
    queryset = Exploit.objects.order_by().values('platform').distinct().exclude(platform__exact='')
    for platform in queryset:
        platform_list.append(dict(platform).get('platform'))
    queryset = Shellcode.objects.order_by().values('platform').distinct().exclude(platform__exact='')
    for platform in queryset:
        if not platform_list.__contains__(dict(platform).get('platform')):
            platform_list.append(dict(platform).get('platform'))
    platform_list = sorted(platform_list)
    for platform in platform_list:
        platform_choices.append((index, platform))
        index = index + 1
    return platform_choices


class AdvancedSearchForm(forms.Form):
    """
    The Django Form containing all the type of filters that the user can use for the
    advanced search.
    """
    search_text = forms.CharField(label='', required=False)
    operator = forms.ChoiceField(label='Operator', choices=OPERATOR_CHOICES)
    author = forms.CharField(label='author', max_length=100, required=False)
    type = forms.ChoiceField(label='Type', choices=get_type_values())
    platform = forms.ChoiceField(label='Platform', choices=get_platform_values())
    port = forms.IntegerField(label='Port', min_value=0, max_value=65535, required=False)
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)


class SimpleSearchForm(forms.Form):
    """
    The Django Form the is used for the standard search.
    """
    search_text = forms.CharField(label='', required=True)
