'''
На першому етапі наш бот-асистент повинен вміти зберігати ім'я
та номер телефону, знаходити номер телефону за ім'ям, змінювати записаний
номер телефону, виводити в консоль всі записи, які зберіг.
Щоб реалізувати таку нескладну логіку, скористаємося словником.
У словнику будемо зберігати ім'я користувача як ключ і номер телефону
як значення.
'''
import sys
import re


CONTACTS = {}


def input_error(func):
    '''
    This is the Errors handling function wrapper
    '''

    def inner(*args):
        '''
        THIS is the errors handling functions
        '''

        try:

            return func(*args)

        except (KeyError, ValueError, IndexError, TypeError) as err:
            return f'Error: {err}'

    return inner

@input_error
def hello_func():
    '''
    "hello", відповідає у консоль "How can I help you?"
    '''
    return 'How can I help you?'


@input_error
def add_func(*args):
    '''
    "add ...". За цією командою бот зберігає у пам'яті (у словнику наприклад)
    новий контакт. Замість ... користувач вводить ім'я та номер телефону,
    обов'язково через пробіл.
    '''
    name_regexp = re.compile(r'^[a-zA-Zа-яА-Я]+$')
    number_regexp = re.compile(r'^\d{3,14}$')
    res = ''
    if len(args) == 2 and name_regexp.match(args[0]) and number_regexp.match(args[1]):

        if args[0] in CONTACTS:
            raise ValueError('This contact is already in the list.\
                            Do you want to change the number?')

        CONTACTS[args[0]] =  args[1]
        res = f'{args[0]} was added'
    else:
        res = 'Wrong Name_Number pattern'

    return res


@input_error
def change_func(*args):
    '''
    "change ..." За цією командою бот зберігає в пам'яті новий номер телефону
    існуючого контакту. Замість ... користувач вводить ім'я та номер телефону,
    обов'язково через пробіл.
    '''
    if len(args) != 2:
        raise KeyError('Enter ONE name and ONE number')

    number_regexp = re.compile(r'^\d{3,14}$')


    if not number_regexp.match(args[1]):
        raise ValueError('Enter a correct number')


    if args[0] in CONTACTS:
        CONTACTS[args[0]] = args[1]

    else:
        raise KeyError('No such name in the list')

    return f'Contact {args[0]}: Number changed to {CONTACTS[args[0]]}'


@input_error
def phone_func(*args):
    '''
    "phone ...." За цією командою бот виводить у консоль номер телефону
    для зазначеного контакту. Замість ... користувач вводить ім'я контакту,
    чий номер треба показати.
    '''
    if len(args) > 1:
        raise ValueError('Enter one name')

    if args[0] in CONTACTS:
        return CONTACTS[args[0]]

    return 'No such name in the list'


@input_error
def show_func():
    '''
    "show all". За цією командою бот виводить всі збереженні контакти
    з номерами телефонів у консоль.
    '''
    #if len(args) > 1 or args[0] != 'all':
        #raise ValueError('Wrong command. Did you mean "show all"')

    display = ''
    for name, number in CONTACTS.items():
        display += f'{name}: {number}\n'

    return display[:-1]


@input_error
def exit_func():
    '''
    "good bye", "close", "exit" по будь-якій з цих команд бот завершує
    свою роботу після того, як виведе у консоль "Good bye!".
    '''
    return 'Good bye'



def main():
    '''
    This is the main function
    '''

    COMMANDS = {
        'hello': hello_func,
        'add': add_func,
        'change': change_func,
        'phone': phone_func,
        'show all': show_func,
        'exit': exit_func,
        'close': exit_func,
        'good bye': exit_func
        }

    while True:
        command = input('Enter the command: ')
        command_words = command.strip().split(' ')

        for _ in filter(lambda x: x == '.', command_words):
            sys.exit()

        command_words[0] = command_words[0].lower()

        if len(command_words) == 2:
            if ' '.join([command_words[0], command_words[1].lower()]) in COMMANDS:
                command_words[0] = ' '.join([command_words[0], command_words[1].lower()])
                del command_words[1]

        if command_words[0] in COMMANDS:
            func_reply = COMMANDS[command_words[0]](*command_words[1:])
            if func_reply:
                print(func_reply)
            if func_reply == 'Good bye':
                sys.exit()
        else:
            print('wrong command')




if __name__ == '__main__':

    main()
