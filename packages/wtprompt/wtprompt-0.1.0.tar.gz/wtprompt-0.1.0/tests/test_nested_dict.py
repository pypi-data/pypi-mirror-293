from wtprompt.utils.nested_dict import NestedDictionary


def test_nested_dict():
    data = {
        'a/b': 'value_ab',
        'a/c': 'value_ac',
        'd': 'value_d'
    }

    nested_dict = NestedDictionary(data)
    assert nested_dict.a.b == 'value_ab'
    assert nested_dict.a.c == 'value_ac'
    assert nested_dict.d == 'value_d'
    'a' in nested_dict
    nested_dict['a/e'] = 'value_ae'
    assert nested_dict.a.e == 'value_ae'

    assert nested_dict['a/b'] == data['a/b']
