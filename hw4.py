# import readfile libraries
animals = ['cat', 'dog', 'turtle', 'bird']
age_bins = [(1,10), (11,20), (21, 30), (31, 40), (41, 50), (51, 60), (61, 70), (71, 80), (81, 90), (91,100)]
adopted = [True, False]

Strd = False
D = True

def create_index(input_file, output_path, sorted):
    f = open(input_file, 'r')
    o = open(output_path, 'w')

    with f, o:
        for line in f:
            line = line.strip()

            animal_str, age_str, adopted_str = line.split(',')
            
            # cast
            age = int(age_str)
            if Strd: print("adopted_str:", adopted_str)
            adopted_val = (adopted_str == 'True')

            # animal bits
            if animal_str == 'cat':
                o.write('1000')
            elif animal_str == 'dog':
                o.write('0100')
            elif animal_str == 'turtle':
                o.write('0010')
            elif animal_str == 'bird':
                o.write('0001')
            else:
                o.write('0000')  # defensive

            # age bins
            for lo, hi in age_bins:
                if lo <= age <= hi:
                    o.write('1')
                else:
                    o.write('0')

            # adopted
            if adopted_val:
                o.write('10')
            else:
                o.write('01')

            # next line
            o.write('\n')

def compress_index(bitmap_index, output_path, compression_method, word_size):
    payload_size = word_size - 1  # 1 bit for control

    '''
    Compress each bitmap column independently 
    • payload_size = word_size - 1 
    • A chunk is: 
        o literal if mixed 
        o fill/run if all 0s or all 1s 
    • Even a single all-0 or all-1 chunk should be encoded as a run 
    • Final short chunk: 
        o pad on the right with 0s 
        o encode as literal if needed 
    • Output is written as characters, not true packed machine bits
    '''

    f = open(bitmap_index, 'r')
    o = open(output_path, 'w') 

    with f, o:
        l = []

        # read all lines into a list
        for line in f:
            if Strd: print("the line:", line.strip())
            l.append(line.strip())

        # turn rows into columns
        cols = []
        colLength = len(l[0])

        # nested for loop to read the i-th character of each line and concatenate them into a column string
        for i in range(colLength):
            buildCol = []
            if Strd: print("building col: ", i)
            for line in l:
                buildCol.append(line[i])
            cols.append(''.join(buildCol))

        
        for index, col in enumerate(cols):

            # WAH - 8
            if compression_method == "WAH":
                if word_size == 8:

                    # track column index
                    if D: print("column", index, "of length", len(col))
                    toAdd = compressWAH8(col, payload_size)

                    # Each column is compressed independently.
                    # We stay on the current column until all of its payload chunks
                    # have been turned into WAH words, then write that column's
                    # compressed output and move to the next column.
                    o.write(col + '\n') # newline

def readRowLine(column, i, payload_size):
    # read a whole line in
    chunk_chars = []
    bits_read = 0
    j = i

    while bits_read < payload_size and j < len(column):
        chunk_chars.append(column[j])
        j += 1
        bits_read += 1

    chunk = ''.join(chunk_chars)

    # if chunk < payload size, pad with 0s on the right
    if bits_read < payload_size:
        chunk = chunk + '0' * (payload_size - bits_read)
        
    return chunk

def compressWAH8(column, payload_size):
    # W = 8, payload = 7 bits
    # literal: 0 + 7 payload
    # fill: 1 + fillbit + 6-bit run count
    # count is measured in payload chunks of 7 bits
    i = 0
    while i < len(column):

        # split into 7 bits
        nextBits = readRowLine(column, i, payload_size)
        l = len(nextBits)

        if D: print("bits:", nextBits, "bits read:", l)
        
        # move to the right
        i = i + payload_size



    
    
    return '0000000'  # placeholder


if __name__ == "__main__":
    # bitmap index creation
    create_index("./data/animals.txt", "animals", False)
    create_index("./data/animals_sorted.txt", "animals_sorted", True)
    create_index("./data/animals_small.txt", "animals_small", False)

    # bitmap index compression
    compress_index("animals_small", "uncompressed_animals_small_WAH_8_mine", "WAH", 8)
    
