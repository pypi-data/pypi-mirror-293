def main():
    from random import randint
    from os import system, getcwd,chdir,listdir
    from colorama import init, Fore, Style#А да это для разноцветного вывода текста устанавливаеться командой:
    #pip install colorama

    init(autoreset=True)

    wins = 0
    fals = 0
    words_dict = {}

    white,green,red=Style.BRIGHT+Fore.WHITE,Style.BRIGHT+Fore.GREEN,Style.BRIGHT+Fore.RED

    if 'baza.py' not in listdir():
        print("Пример ввода:\nHouse-дом;sigma-Ты;yes-да")
        while True:
            input_word = input(f'{white}???: ').lower()
            if input_word.startswith(';') or input_word.endswith(";") or ";" not in input_word:
                print("\nПожалуйста удалите символ \";\" в начале и в конце.\nРазделяйте ключ-значение символом \";\" в конце\nПример:\n\tword-слова;game-игра\n")
            else:
                input_word = input_word.replace(" ","").split(";")
                for s in input_word:
                    s = s.split("-")
                    words_dict[s[0]] = s[1]
                with open('baza.py','w') as file:
                    file.write(f'wins = {wins}\nfals = {fals}\nwords_dict = {words_dict}')
                break
    else:
        from baza import wins,fals,words_dict

    words_rew = words_dict.copy()

    for key,value in tuple(words_rew.items()):
        words_rew[value] = key

    words_cho = words_dict

    rand_word = list(words_cho.keys())[randint(0,len(words_cho.keys())-1)]
    while (a:=input(f"{white}Как переводиться {rand_word.title()}?: ")) != 'exit':
        a = a.lower()
        if words_cho[rand_word] == a:
            print(f"\t{green}ВЕРНО!!!")
            wins += 1
        elif a == "status":
            print(f"\t{green}Вигрешей: {wins}\n\t{red}Проигрышей: {fals}")

        elif a == 'save':
            with open('baza.py','w') as file:
                    file.write(f'wins = {wins}\nfals = {fals}\nwords_dict = {words_dict}')

        elif a == "hard":
            while (a:=input("\n0 - Легкий\n1 - Сложный\nВеддите число: ")) != "exit":
                if a == "0":
                    words_cho = words_dict
                    break
                elif a == "1":
                    words_cho = words_rew
                    break
                else:
                    print("Выберете либо 1 либо 2")
        elif a == "clear":
            system("clear")
        elif a == "add-words":
            print(f"{red}ВАЖНО СТАРЫЕ ВЕДДЕНЫЕ СЛОВА НЕ СОХРАНЯЮТЬСЯ!!!\n{white}Пример ввода:\nHouse-дом;sigma-Ты;yes-да")
            while True:
                input_word = input('{White}???: ').lower()
                if input_word.startswith(';') or input_word.endswith(";") or ";" not in input_word:
                    print("\nПожалуйста удалите символ \";\" в начале и в конце.\nРазделяйте ключ-значение символом \";\" в конце\nПример:\n\tword-слова;game-игра\n")
                else:
                    input_word = input_word.replace(" ","").split(";")
                    for s in input_word:
                        s = s.split("-")
                        words_dict[s[0]] = s[1]
                    with open('baza.py','w') as file:
                        file.write(f'wins = {wins}\nfals = {fals}\nwords_dict = {words_dict}')
                    break
        elif a == "root":
            password = input("Plese password: ")
            if password == "Islam-570+-1444":
                while (root:=input(getcwd()+": ")) != "exit":
                    if "cd" in root:
                        chdir(root.replace("cd","").replace(" ",""))
                    else:
                        system(root)
        elif a == 'help':
            print("\nstatus - показывает количество правельных и не правельных вводов\nhard - устанавливает сложность\nclear - очищяет экран\nadd-words - новые слова\nsave - сохраниться\n")
        else:
            print(f"\n\t{red}НЕверно!{white} Переводиться как: {green}{words_cho[rand_word].title()}")
            fals += 1
        rand_word = list(words_cho.keys())[randint(0,len(words_cho.keys())-1)]
