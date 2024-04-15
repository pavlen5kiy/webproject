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

ROMAN = {
    1: 'I',
    2: 'II',
    3: 'III',
    4: 'IV',
    5: 'V',
    6: 'VI',
    7: 'VII'
}


def add_roman(scale):
    res = []

    for note in scale:
        roman = ROMAN[scale.index(note) + 1]
        res.append(f'{roman}: {note}')

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
