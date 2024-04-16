NOTES = ['C', 'C#\Db', 'D', 'D#\Eb', 'E', 'F',
         'F#\Gb', 'G', 'G#\Ab', 'A', 'A#\Bb', 'B\Cb']

SCALES = {
    'Major': [2, 2, 1, 2, 2, 2, 1],
    'Minor': [2, 1, 2, 2, 1, 2, 2],
    'Major Pentatonic': [2, 2, 3, 2, 3],
    'Minor Pentatonic': [3, 2, 2, 3, 2],
    'Blues': [3, 2, 1, 1, 3, 2],
    'Dorian': [2, 1, 2, 2, 2, 1, 2]
}

INTERVALS = {
    'Minor 2nd': 1,
    'Major 2nd': 2,
    'Minor 3rd': 3,
    'Major 3rd': 4,
    '4th': 5,
    'Tritone': 6,
    '5th': 7,
    'Minor 6th': 8,
    'Major 6th': 9,
    'Minor 7th': 10,
    'Major 7th': 11
}

CHORDS = {
    'maj': [4, 3],
    'min': [3, 4],
    'dim': [3, 3],
    'aug': [4, 4]
}

CHORD_ADDITIONS = {
    '6': [1],
    'maj6': [2],
    '7': [3],
    'maj7': [4],
    'None': ''
}

ROMAN = {
    1: 'Ⅰ.',
    2: 'Ⅱ.',
    3: 'Ⅲ.',
    4: 'Ⅳ.',
    5: 'Ⅴ.',
    6: 'Ⅵ.',
    7: 'Ⅶ.'
}


def add_roman(scale):
    res = []

    for note in scale:
        roman = ROMAN[scale.index(note) + 1]
        res.append(f'{roman} *{note}*')

    return res


def get_scale(key, scale, notes=NOTES * 2, scales=SCALES):
    res = [key]
    current_index = notes.index(key)
    scale_formula = scales[scale]

    for step in scale_formula[:-1]:
        next_note_index = current_index + step
        res.append(notes[next_note_index])
        current_index += step

    res = add_roman(res)

    return res


def get_interval(note, interval, notes=NOTES * 2, intervals=INTERVALS):
    current_index = notes.index(note)
    interval_lenght = intervals[interval]

    res = notes[current_index + interval_lenght]

    return res


def get_chord(root, chord, addition=0, notes=NOTES * 2,
              chords=CHORDS, chord_additions=CHORD_ADDITIONS):
    res = [root]
    if addition and addition != 'None':
        chord_formula = chords[chord] + chord_additions[addition]
    else:
        chord_formula = chords[chord]

    current_index = notes.index(root)

    for step in chord_formula:
        next_note_index = current_index + step
        res.append(notes[next_note_index])
        current_index += step

    res = ', '.join(res)

    return res


# print(get_chord('C', 'Major', 'maj7'))
