# Random String generator for trantion id

def order_id():
    import random
    import string
    lower =  string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    combine = list(lower+upper+num)
    random.shuffle(combine)
    final_id = ''.join(combine)[:8]
    data =  'TRN'+final_id

    from core.models import Transtions
    if Transtions.objects.filter(transtion_id = data).exists():
        data = order_id()
        
    return data


def custom_id(stri):
    import random
    import string
    lower =  string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    combine = list(lower+upper+num)
    random.shuffle(combine)
    final_id = ''.join(combine)[:8]
    data =  stri + final_id

    from authentication.models import User
    if User.objects.filter(unique_key = data).exists():
        data = order_id(stri)
        
    return data



# remove spaces from strings
def remove_spaces(str):
    return str.replace(" ","")


# create refrence num
def refrance_no():
    import random
    import string
    num = string.digits
    combine = list(num)
    random.shuffle(combine)
    final_id = ''.join(combine)[:9]

    return final_id


# create reffer code for reffering
def reffer_id():
    import random
    import string
    lower =  string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    combine = list(lower+upper+num)
    random.shuffle(combine)
    join_final_id = ''.join(combine)[:5]
    final_id = 'TREZ' + join_final_id

    from authentication.models import User
    if User.objects.filter(reffer_code = final_id).exists():
        final_id = reffer_id()
    return  final_id





