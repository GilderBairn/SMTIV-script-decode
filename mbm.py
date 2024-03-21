import os
import sys

MAGIC_NUM_CONST = 65536
A_DIFF = ord('Ａ') - ord('A')

def fixSJISUnicode(text):
    fixed = ''
    for char in text:
        if ord(char) >= ord('！') and ord(char) <= ord('～'):
            fixed += chr(ord(char) - A_DIFF)
        elif char == '　':
            fixed += ' '
        elif char == '’':
            fixed += "'"
        else:
            fixed += char
    return fixed

def handleColorTag(bytesSegment):
    color = int.from_bytes(bytesSegment[0:2], byteorder='little') & 0xfff
    tagText = f'[Color:0x{color:x}]'
    remaining = bytesSegment[2:]
    return tagText, remaining

def handleNumberedVarTag(bytesSegment, name):
    num = int.from_bytes(bytesSegment[0:2], byteorder='little')
    tagText = f'[{name} {num}]'
    remaining = bytesSegment[2:]
    return tagText, remaining

def handleIntVarTag(bytesSegment, name):
    num = int.from_bytes(bytesSegment[0:4], byteorder='little')
    tagText = f'[{name} {num}]'
    remaining = bytesSegment[4:]
    return tagText, remaining

def handlePlayerTag(bytesSegment):
    num = int.from_bytes(bytesSegment[0:2], byteorder='little')
    tagText = f'[Ally {num}]'
    
    if (num == 0):
        tagText = '[Flynn]'
    
    remaining = bytesSegment[2:]
    return tagText, remaining

def handleDoubleIntVarTag(bytesSegment, name):
    num1 = int.from_bytes(bytesSegment[0:4], byteorder='little')
    num2 = int.from_bytes(bytesSegment[4:8], byteorder='little')
    tagText = f'[{name} {num1}, {num2}]'
    remaining = bytesSegment[8:]
    return tagText, remaining

def handleSpeakingCharacter(bytesSegment):
    split = bytesSegment.split(b'\x00\x00')
    return f'({split[0].decode("shift-jis")}) ', bytesSegment[len(split[0]) + 2:]

def parseFunctionToken(token, remaining):
    tokenText = ''
    strippedSection = remaining

    if token[1] == int.from_bytes(b'\x01'):
        tokenText = '\n'
    elif token[1] == int.from_bytes(b'\x02'):
        tokenText = '[->]'
    elif token[1] == int.from_bytes(b'\x04'):
        tokenText, strippedSection = handleColorTag(remaining)
    elif token[1] == int.from_bytes(b'\x11'):
        tokenText, strippedSection = handleNumberedVarTag(remaining, '11')
    elif token[1] == int.from_bytes(b'\x12'):
        tokenText, strippedSection = handleSpeakingCharacter(remaining)
    elif token[1] == int.from_bytes(b'\x13'):
        tokenText, strippedSection = handleDoubleIntVarTag(remaining, '13')
    elif token[1] == int.from_bytes(b'\x14'):
        tokenText, strippedSection = handleIntVarTag(remaining, 'button')
    elif token[1] == int.from_bytes(b'\x41'):
        tokenText, strippedSection = handleNumberedVarTag(remaining, '41')
    elif token[1] == int.from_bytes(b'\x42'):
        tokenText, strippedSection = handleNumberedVarTag(remaining, '42')
    elif token[1] == int.from_bytes(b'\x43'):
        tokenText, strippedSection = handlePlayerTag(remaining)
    elif token[1] >= int.from_bytes(b'\x51') and token[1] <= int.from_bytes(b'\x58'):
        tokenText, strippedSection = handleNumberedVarTag(remaining, f'{token[1]:x}')
    elif token[1] == int.from_bytes(b'\x70'):
        tokenText, strippedSection = handleNumberedVarTag(remaining, '70')
    elif token[1] == int.from_bytes(b'\x71'):
        tokenText, strippedSection = handleNumberedVarTag(remaining, '71')
    elif token[1] == int.from_bytes(b'\x72'):
        tokenText, strippedSection = handleNumberedVarTag(remaining, 'Item')
    elif token[1] == int.from_bytes(b'\x73'):
        tokenText, strippedSection = handleNumberedVarTag(remaining, 'Demon name')
    elif token[1] == int.from_bytes(b'\x74'):
        tokenText, strippedSection = handleNumberedVarTag(remaining, '74')
    elif token[1] == int.from_bytes(b'\x75'):
        tokenText, strippedSection = handleNumberedVarTag(remaining, 'Demon race')
    elif token[1] == int.from_bytes(b'\x77'):
        tokenText, strippedSection = handleNumberedVarTag(remaining, 'Skill')
    elif token[1] == int.from_bytes(b'\x78'):
        tokenText, strippedSection = handleNumberedVarTag(remaining, 'Amount')
    elif token[1] == int.from_bytes(b'\x79'):
        tokenText, strippedSection = handleNumberedVarTag(remaining, '79')
    elif token[1] == int.from_bytes(b'\x7a'):
        tokenText, strippedSection = handleNumberedVarTag(remaining, '7a')
    elif token[1] == int.from_bytes(b'\x7b'):
        tokenText, strippedSection = handleDoubleIntVarTag(remaining, '7b')
    elif token[1] == int.from_bytes(b'\x7c'):
        tokenText, strippedSection = handleIntVarTag(remaining, '7c')
    elif token[1] == int.from_bytes(b'\x7d'):
        tokenText, strippedSection = handleNumberedVarTag(remaining, '7d')
    else:
        tokenText += f'[{token[1]:x}]'
    return tokenText, strippedSection

def parseEntry(entryBytes):
    sectionText = ''
    remainingBytes = entryBytes
    
    while(remainingBytes):
        section = remainingBytes[0:2]
        remainingBytes = remainingBytes[2:]

        if len(section) == 1:
            section.append(b'\xff')

        if section == b'\xff\xff':
            sectionText += '[END]'
            remainingBytes = []
        elif section[0] & 0xf0 == 0xf0 or section[0] == 0x80:
            # its a function marker
            tokenText, remainingBytes = parseFunctionToken(section, remainingBytes)
            sectionText += tokenText
        else:
            # regular text
            try:
                sectionText += section.decode('shift-jis')
            except Exception as ex:
                print(f'Error occured while parsing file:\n{str(ex)}')
                print(f'Current byte section: {section}')
                print(f'Section text: {sectionText}')

    
    return fixSJISUnicode(sectionText)

def parseMBMFile(filename, debug=False):
    disk_size = os.path.getsize(filename)
    final_str = ''

    with open(filename, 'rb') as fp:
        leading_zero = int.from_bytes(fp.read(4), byteorder='little')
        msg2 = fp.read(4).decode('utf-8')
        magic_num = int.from_bytes(fp.read(4), byteorder='little')
        file_size = int.from_bytes(fp.read(4), byteorder='little')

        if debug:
            print(leading_zero)
            print(msg2)
            print(magic_num)
            print(f'reported size: {file_size}')
            print(f'size: {disk_size}')
        
        valid_mbm = leading_zero == 0 and msg2 == 'MSG2' and magic_num == MAGIC_NUM_CONST
        size_matches = file_size == disk_size

        if not valid_mbm:
            print('invalid file format - valid MSG2 file format not detected')
            return ''
        
        if not size_matches and debug:
            # I don't think this matters - I think I've solved it
            print('WARNING!! - mbm file size does not match what was listed in the file')
        
        num_entries = int.from_bytes(fp.read(4), byteorder='little')
        entries_offset = int.from_bytes(fp.read(4), byteorder='little')

        if debug:
            print(f'entries: {num_entries}')
            print(f'offset: {entries_offset}')
        
        found_entries = 0
        i = 0
        while found_entries < num_entries:
            fp.seek(entries_offset + (i*16))

            entry_id = int.from_bytes(fp.read(4), byteorder='little')
            entry_data_length = int.from_bytes(fp.read(4), byteorder='little')
            entry_data_offset = int.from_bytes(fp.read(4), byteorder='little')
            if (entry_id != i or entry_data_length == 0 or entry_data_offset == 0):
                #print(f'entry number is different from expected - skipping\nexpected: {i}, got: {entry_id}')
                i += 1
                continue
            
            found_entries += 1
            fp.seek(entry_data_offset)
            entry_data_bytes = fp.read(entry_data_length)
            entry_parsed = parseEntry(entry_data_bytes)

            final_str += f'{entry_id}: {entry_parsed}\n'
            i += 1
        
    return final_str

def get_all_in_one_filename(root):
    root_dir_name = os.path.split(root)[-1]
    return os.path.join(root, f'{root_dir_name}-ALL_IN_ONE.txt')


def convert_dir_mode(target, recursive, all_in_one, verbose=False):
    # try to reset the contents of the all-in-one file if it exists
    try:
        with open(get_all_in_one_filename(target), 'w') as fp:
            fp.write('')
    except:
        pass # this means the file isn't there, so like... no big deal? It'll be created later

    convert_dir_mode_recursive(target, target, recursive, all_in_one, verbose)

def convert_dir_mode_recursive(current, root, recursive, all_in_one, verbose=False):
    # find absolute paths for all .mbm files within the current directory
    mbm_files = [os.path.abspath(os.path.join(current, file)) for file in os.listdir(current) if file.endswith('.mbm')]
    # find child directories in the current directory
    dirs = [os.path.join(current, dir) for dir in os.listdir(current) if os.path.isdir(os.path.join(current, dir))]

    if len(mbm_files) > 0 and verbose:
        print(f'found {len(mbm_files)} mbm files within directory {current}. processing...')

    for mbm in mbm_files:
        if verbose:
            print(mbm)
        parsed = parseMBMFile(mbm)
        out_file = mbm.replace('.mbm', '.txt')

        if all_in_one in ('yes', 'no'):
            with open(out_file, 'wb') as out:
                if parsed:
                    out.write(parsed.encode('utf-8'))

        if all_in_one in ('yes', 'only'):
            all_in_one_target = get_all_in_one_filename(root)
            with open(all_in_one_target, 'ab') as out:
                if parsed:
                    out.write(f'{os.path.relpath(mbm, start=root)}:\n'.encode('utf-8'))
                    out.write(parsed.encode('utf-8'))
                    out.write('\n\n'.encode('utf-8'))
    if recursive:
        for dir in dirs:
            convert_dir_mode_recursive(dir, root, True, all_in_one)

def convert_single_mode(target, verbose):
    parsed = parseMBMFile(target, verbose)
    if verbose:
        print(parsed)
    out_file = target.replace('.mbm', '.txt')
    with open(out_file, 'wb') as out:
        if parsed:
            out.write(parsed.encode('utf-8'));

if __name__ == '__main__':
    target = './'
    dir_mode = True
    arg_error = False
    recursive_mode = False
    all_in_one = 'no'
    verbose = False

    if len(sys.argv) > 1 and sys.argv[1].endswith('.mbm'):
        # an individual mbm file is specified
        dir_mode = False
        target = sys.argv[1]
    elif len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        # a directory is specified
        target = sys.argv[1]
    else:
        arg_error = True
    
    if dir_mode and '-r' in sys.argv:
        recursive_mode = True
    if dir_mode and '-a' in sys.argv and '-A' not in sys.argv:
        all_in_one = 'yes'
    if dir_mode and '-A' in sys.argv and '-a' not in sys.argv:
        all_in_one = 'only'
    if '-v' in sys.argv or '-V' in sys.argv:
        verbose = True

    target = os.path.abspath(target)
    
    if arg_error:
        print("invalid argument")
    if dir_mode and not arg_error:
        convert_dir_mode(target, recursive_mode, all_in_one, verbose)
    else:
        convert_single_mode(target, verbose)
