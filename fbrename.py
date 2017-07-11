""" This module renames files from the name of the book """
import pathlib
import zipfile
import sys


# coding: utf8
__version__ = '0.4'
__author__ = 'Telnov Oleg'


__path__ = pathlib.Path('.')
__list_of_files_fb__ = list(__path__.glob('*.fb2'))
__list_of_files_zip__ = list(__path__.glob('*.zip'))
__list_of_files__ = __list_of_files_fb__ + __list_of_files_zip__

try:
    __log__ = open('error.log', 'w', encoding='utf-8')
except OSError:
    print('I can not open the file "error.log"')

if __list_of_files__ is None:
    __log__.write('Books not found')
    quit()


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


__I__ = 0
__P__ = 100 / len(__list_of_files__)

for f in __list_of_files__:
    __I__ += 1
    per = '\t' + str(round(__I__*__P__, 2))
    print(per + '%', end='\r')
    try:
        fname = ''
        arr_bin = []
        if zipfile.is_zipfile(f):
            zf = zipfile.ZipFile(str(f), mode='r')
            zl = zf.namelist()
            if len(zl) == 1:
                if zl[0][-3:] == 'fb2':
                    fb = zf.open(zl[0], mode='r')
                    arr_bin = fb.read()
                    fb.close()
                    zf.close()
            else:
                zf.close()
                continue
        else:
            fb = open(f, 'rb')
            arr_bin = fb.read()
            fb.close()
        if arr_bin is not None:
            text = decoder(arr_bin)
            fname = getname(text, f)
            if not fname == '':
                if not pathlib.Path(fname).exists():
                    f.rename(fname)
    except OSError:
        zf.close()
        fb.close()
        __log__.write(str(f) + '\t->\t' + fname + '\n')
        __log__.write(str(sys.exc_info()) + '\n')
