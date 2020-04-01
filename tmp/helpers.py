# # --------------------------------------------------
# # P33 模块和包
# # --------------------------------------------------

# # ----- Creating module
# # helpers.py
# def display(message, is_warning=False):
#     if is_warning:
#         print('This is a Warning!!')
#     print(message)


# --------------------------------------------------
# P35 实操自定义模块、包、虚拟环境
# --------------------------------------------------
from pip._vendor.colorama import init, Fore

def display(message, is_warning=False):
    if is_warning:
        print(Fore.RED + message)
    else:
        print(Fore.BLUE + message)