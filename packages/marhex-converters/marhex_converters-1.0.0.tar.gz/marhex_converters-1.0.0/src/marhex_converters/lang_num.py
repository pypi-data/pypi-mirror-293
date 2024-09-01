persian_num = {'0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴', '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'}
english_num = {'۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4', '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'}


def english_to_persian(arg):
    
    result = ''
    
    try:
        for item in str(arg):
            result += persian_num[item]
        return result
    except:
        raise ValueError('Just can Entre English Number by [int] or [str] type.')


def persian_to_english(arg):

    result = ''
    
    try:
        for item in str(arg):
            result += english_num[item]
        return result
    except:
        raise ValueError('Just can Entre Persian Number by [str] type.')

   
