#math functions ------------------------------------------------------------------------------------------------------
def exponential(value,exp=9,num=-1):
    return multiply_it(value,exp_it(10,exp,num))

def return_0(*args):
    for arg in args:
        if arg == None or not is_number(arg) or arg in [0,'0','','null',' ']:
            return float(0)
        
def exp_it(number,integer,mul):
    if return_0(number,integer,mul)==float(0):
        return float(0)
    return float(number)**float(float(integer)*int(mul))

def divide_it(number_1,number_2):
    if return_0(number_1,number_2)==float(0):
        return float(0)
    return float(number_1)/float(number_2)

def multiply_it(number_1,number_2):
    if return_0(number_1,number_2)==float(0):
        return float(0)
    return float(number_1)*float(number_2)

def add_it(number_1,number_2):
    if return_0(number_1,number_2)==float(0):
        return float(0)
    return float(number_1)+float(number_2)

def get_percentage(owner_balance,address_balance):
    retained_div = divide_it(owner_balance,address_balance)
    retained_mul = multiply_it(retained_div,100)
    return round(retained_mul,2)
