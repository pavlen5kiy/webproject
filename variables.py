from markups import scale_markup, intervals_markup, chords_markup

API_TOKEN = '7161683104:AAHqONitwtt3N4x2Wx-2MFMxC55f-d0ShVU'

last_messages = []
destination = ''
current_note = ''
current_scale = ''
current_interval = ''
current_chord = ''
current_addition = ''

destinations = {
    'Scale': {'text': 'OK. In which scale?', 'markup': scale_markup},
    'Intervals': {'text': 'OK. What interval?', 'markup': intervals_markup},
    'Chords': {'text': 'OK. What chord?', 'markup': chords_markup}
}
