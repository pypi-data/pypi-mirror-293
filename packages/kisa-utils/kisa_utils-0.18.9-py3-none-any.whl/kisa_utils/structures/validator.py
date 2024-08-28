'''
this modules handle data structure validation to ensure that
data is passed in expected formats/structures
'''

from typing import Any, get_args
from types import UnionType
from kisa_utils.structures.utils import Value
from kisa_utils.response import Response, Ok, Error

def validate(instance:Any, structure:Any, path:str='$') -> dict:
    '''
    validate payload/instance against a pre-defined structure
    
    returns {
        'status':bool,
        'log':STRING
    }
    '''
    
    result = {'status':False, 'log':''}

    # union types such as int|float...
    if isinstance(structure, UnionType):
        if not isinstance(instance, get_args(structure)):
            expectedTypes = [str(_).split("'")[1] for _ in get_args(structure)]
            result['log'] = f'E06: types not similar:: {path}, expected one of {"|".join(expectedTypes)} but got {str(type(instance))[7:-1]}'
            return result

    # when the structure is a block type/class eg dict,list,tuple,etc
    elif type(structure)==type(type) or isinstance(structure, Value):
        _structure = structure._valueType if isinstance(structure, Value) else structure

        if instance!=_structure and not isinstance(instance, _structure):
            result['log'] = f'E01: types not similar:: {path}, expected {str(_structure)[7:-1]} but got {str(type(instance))[7:-1]}'
            return result

        if isinstance(structure, Value):
            if not (response:=structure.validate(instance)):
                result['log'] = f'E01-01: {path}:: validator error({response.log})'
                return result

        result['status'] = True
        return result
    else:
        if not isinstance(instance,type(structure)):
            result['log'] = f'E02: types not similar:: {path}, expected {str(type(structure))[7:-1]} but got {str(type(instance))[7:-1]}'
            return result

        if isinstance(structure,dict):
            _path = path
            for key in structure:
                path = f'{_path}->{key}'
                if key not in instance:
                    result['log'] = f'E03: missing key:: {path}'
                    return result
                res = validate(instance[key],structure[key], path=path)
                if not res['status']:
                    return res
        elif isinstance(structure,(list,tuple)):
            _path = path
            for index,item in enumerate(structure):
                path = f'{_path}->[#{index}]'
                if len(instance)<=index:
                    expectedTypes = str(type(item))[7:-1] if not isinstance(item,type) else str(item)[7:-1]
                    if isinstance(item, UnionType):
                        expectedTypes = "|".join([str(_).split("'")[1] for _ in get_args(item)])

                    result['log'] = f'E04: missing item at index:: {path}, expects {expectedTypes}'
                    return result
                res = validate(instance[index],item, path=path)
                if not res['status']:
                    return res

    result['status'] = True
    return result

def validateWithResponse(instance:Any, structure:Any) -> Response:
    response = validate(instance, structure)
    if response['status']: return Ok()
    return Error(response['log'])