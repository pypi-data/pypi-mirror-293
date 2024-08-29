import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_choice(num_options):
    while True:
        choice = input("输入选项编号: ")
        if choice.isdigit() and 1 <= int(choice) <= num_options:
            return int(choice)
        else:
            print("无效输入，请输入正确的编号。")
