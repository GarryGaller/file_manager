import os
from functools import partial
from collections import defaultdict
from pathlib import Path

def clear():
    '''очистка экрана консоли'''
    os.system('cls' if os.name == 'nt' else "clear")
    return None,None


def type_entry(entry):
    '''определяем тип записи'''
    types = {16384:'dir',32768:'file',40960:'link'}
    for bits,type in types.items():
        if entry.stat().st_mode & bits:
            return type
    return None


def get_path_from_int(inp):
    '''получает имя записи по номеру, если передано число;
    если номер отсутствует, то число возвращается как есть, 
    интепретируясь как имя директории или файла;
    если передано не число, возвращаем как есть
    '''
    if ROOT in LAST_SCANDIR:
        try:
            inp = LAST_SCANDIR[ROOT][int(inp)]  
        except (ValueError,IndexError):
            pass 
        else:
            inp = inp.name
    return inp 


def enum_dir(inp):
    '''перечисление содержимого директории в виде записей
    класса DirEntry
    '''
    global ROOT
    add_entries = True
    
    if ROOT != inp: ROOT = inp
    print('ROOT:',inp)
    
    if ROOT in LAST_SCANDIR:
        entries = LAST_SCANDIR[ROOT]
        add_entries = False    
    else:
        entries = os.scandir(inp)
    
    for i,entry in enumerate(entries):
        print("{:4}:{}:{}".format(
            i,entry.name,
            type_entry(entry)
        ))
        if add_entries:
            LAST_SCANDIR[ROOT].append(entry) 


def after_input(inp):
    '''если передан файл - возвращаем его;
    если директория - перечисляем ее содержимое'''
    
    result = None,None
    inp = get_path_from_int(inp)
    
    if not os.path.isabs(inp):
        inp = os.path.realpath(os.path.join(ROOT,inp))
    
    if os.path.exists(inp):
        if Path(inp).is_file(): 
            result = 1,inp
        else:
            enum_dir(inp)
    # not exists        
    else:
        result = 0,inp  
    return result

def get_selected_file():
    '''цикл опроса и возврата выбранного файла'''
    result = None,None
    while 1:
        inp = input(
            'exit:   Выход\n'
            'clear:  Очистка экрана\n'
            'current:{}\n>>'.format(ROOT)
        )
        
        # если вам скажут, что в Python нет switch - покажите ему это:
        result = {
            ''     :partial(after_input,ROOT.lower()),
            'exit' :lambda:(-1,None), # выход из цикла, без выхода из приложения
            'clear':clear      # очистка экрана консоли
        }.get(inp,
            # ветка default
            partial(after_input,inp.lower())
        )()      
        
        if result[0] == 0:
            print("Path not found:",result[1])
        # выходим, если получили что-то отличное от None
        elif result[0] is not None:
            break   
        
    return result

if __name__ == "__main__":
    ROOT = os.path.abspath('.').lower()
    LAST_SCANDIR = defaultdict(list)
    err, sfile = get_selected_file()
    if err != -1:
        print("Выбран файл:", sfile)
    else:
        print("Файл не выбран")

   
        
        
