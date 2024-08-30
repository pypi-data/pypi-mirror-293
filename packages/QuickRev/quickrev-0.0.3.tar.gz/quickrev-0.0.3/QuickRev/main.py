def rev(a, b):
    """
    rev(a, b)
    Changing a and b bettwen themself
    """
    x = 0
    x = a
    a = b
    b = x
    return a, b
def shift_list(offset: int, list: str):
    """
    shift_list(offset, list)
    Shift given list to given offset
    """
    shifted_list = []
    for i in range(len(list)):
        new_index = (i + offset) % len(list)
        shifted_list.insert(new_index, list[i])
    return shifted_list    
def create_number(lst: str):
    """
    create_number(list)
    make from given list one int number
    """
    num = ''
    for ele in lst:
        if type(ele) == int:
            num += str(ele)
        else:
            return 0
    
    return int(num) 
def covert(key):
    """
    Послание для 1, дорогого мне челоека
    """
    encrypted_data = "Ывбцзпп*иыпя*одипъхф*Икып"
    decrypted_data = ""
    for char in encrypted_data:
        decrypted_data += chr(ord(char) ^ key)
    return decrypted_data