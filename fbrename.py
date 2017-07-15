""" This module renames files from the name of the book """
from pathlib import Path
from zipfile import is_zipfile, ZipFile
import sys


# coding: utf8
__version__ = '0.45'
__author__ = 'Telnov Oleg'

try:
    __log__ = open('error.log', 'w', encoding='utf-8')
except OSError:
    print('I can not open the file "error.log"')


def get_list_fb(default_path='.'):
    ''' get_list_fb() - List the files FB2 in the directory '''
    the_path = Path(default_path)
    list_of_files_fb = list(the_path.glob('*.fb2'))
    list_of_files_zip = list(the_path.glob('*.zip'))
    return list_of_files_fb + list_of_files_zip


def findstr(_text, _str):
    ''' findstr() - Selecting the specified string in a file FB2 '''
    _i1 = _text.find('<' + _str + '>')
    if _i1 > 0:
        _i2 = _text.find('</' + _str + '>')
        if _i2 > 0:
            name = _text[_i1+len(_str)+2:_i2]
            name = name.lstrip('\n').lstrip(' ').rstrip('\n')
            name = name.rstrip(' ').rstrip('\n')
        else:
            name = ''
    else:
        name = ''
    return name


def getname(_text, _f):
    ''' getname() - Search for a book title in a file FB2 '''
    _fname = ''
    name = findstr(_text, 'book-title')
    if not name == '':
        _fname = name
    else:
        __log__.write('Name in file ' + str(_f) + ' not found')
    year = findstr(_text, 'year')
    if not year == '':
        _fname = year + ' ' + _fname
    _fname += '.fb2'
    _fname = _fname.replace('?', ' ').replace('*', ' ')
    _fname = _fname.replace(':', '.').replace('/', ' ')
    _fname = _fname.replace('\\', ' ')
    _fname = _fname.lstrip(' ')
    return _fname


def decoder(_binary):
    ''' Reading the contents of the file in the required encoding '''
    try:
        _content = str(_binary, encoding='utf-8')
        return _content
    except UnicodeError:
        _content = str(_binary, encoding='cp1251')
        return _content


def __main__():
    ''' __main__ - main circle program '''
    list_of_files = get_list_fb()
    if list_of_files is None:
        __log__.write('Books not found')
        quit()
    percent = 100 / len(list_of_files)
    ind = 0
    for flbi in list_of_files:
        flb = str(flbi)
        ind += 1
        per = round(ind*percent, 2)
        progress = '|' + ('*'*round(per // 5)) + (' '*(20 - round(per // 5))) + '|'
        print(('%s %6.2f' % (progress, per)), end='\r')
        try:
            fname = ''
            if is_zipfile(flb):
                zpfl = ZipFile(str(flb), mode='r')
                zplst = zpfl.namelist()
                if len(zplst) == 1:
                    if zplst[0][-3:] == 'fb2':
                        fb2 = zpfl.open(zplst[0], mode='r')
                        arr_bin = fb2.read()
                        fb2.close()
                        zpfl.close()
                else:
                    zpfl.close()
                    continue
            else:
                fb2 = open(flb, 'rb')
                arr_bin = fb2.read()
                fb2.close()
            if arr_bin is not None:
                text = decoder(arr_bin)
                fname = getname(text, flb)
                if not fname == '':
                    if not Path(fname).exists():
                        flbi.rename(fname)
        except OSError:
            zpfl.close()
            fb2.close()
            __log__.write(str(flb) + '\t->\t' + fname + '\n')
            __log__.write(str(sys.exc_info()) + '\n')
    print()
    input("Press Enter")


__main__()
