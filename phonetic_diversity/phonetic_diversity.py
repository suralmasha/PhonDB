from tqdm import tqdm
from ru_transcript import get_allophone_info

from transcribator import Transcribator
from weights import get_weights, safe_divide


def count_phonemes_and_allophones(sounds, group):
    if group == 'vowels':
        group = 'vowel'
    elif group in ['deaf', 'silent']:
        group = 'voiceless'
    if group not in ['vowel', 'sonorous', 'voiced', 'voiceless']:
        return

    result = []
    for i, phon in enumerate(sounds):
        try:
            if get_allophone_info(phon)['class'] == group:
                result.append(phon)
        except KeyError:
            continue

    return result


def phoneme_allophone_ratio(ph, al):
    n_allophones = len(al)
    n_phonemes = len(set(ph))

    return safe_divide(n_phonemes, n_allophones)


def phon_db(text_ph, text_al, vowels_weight=0.4, sonorous_weight=0.3, voiced_weight=0.2, voiceless_weight=0.1,
            print_inter_res=False):
    # Phonetic diversity
    vowels_ph = count_phonemes_and_allophones(text_ph, 'vowels')
    vowels_al = count_phonemes_and_allophones(text_al, 'vowels')
    sonorous_ph = count_phonemes_and_allophones(text_ph, 'sonorous')
    sonorous_al = count_phonemes_and_allophones(text_al, 'sonorous')
    voiced_ph = count_phonemes_and_allophones(text_ph, 'voiced')
    voiced_al = count_phonemes_and_allophones(text_al, 'voiced')
    voiceless_ph = count_phonemes_and_allophones(text_ph, 'voiceless')
    voiceless_al = count_phonemes_and_allophones(text_al, 'voiceless')

    vowels = phoneme_allophone_ratio(vowels_ph, vowels_al)
    sonorous = phoneme_allophone_ratio(sonorous_ph, sonorous_al)
    voiced = phoneme_allophone_ratio(voiced_ph, voiced_al)
    voiceless = phoneme_allophone_ratio(voiceless_ph, voiceless_al)

    if print_inter_res:
        print(
            f'vowels: {round(vowels, 8)} ({len(set(vowels_ph))}, {len(vowels_al)})\n'
            f'sonor: {round(sonorous, 8)} ({len(set(sonorous_ph))}, {len(sonorous_al)})\n'
            f'voiced: {round(voiced, 8)} ({len(set(voiced_ph))}, {len(voiced_al)})\n'
            f'voiceless: {round(voiceless, 8)} ({len(set(voiceless_ph))}, {len(voiceless_al)})\n'
        )

    x1, x2, x3, x4 = get_weights(len(vowels_al), len(sonorous_al), len(voiced_al), len(voiceless_al))
    vowels_weight = vowels_weight * x1
    sonorous_weight = sonorous_weight * x2
    voiced_weight = voiced_weight * x3
    voiceless_weight = voiceless_weight * x4
    res = round(
        (
                vowels * vowels_weight
                + sonorous * sonorous_weight
                + voiced * voiced_weight
                + voiceless * voiceless_weight
        ) * 100,
        4
    )

    return res


def phon_db_window(text_ph, text_al, window_length=50):
    words_ph = ' '.join(text_ph).split('_')
    words_al = ' '.join(text_al).split('_')

    if len(words_ph) < (window_length + 1):
        ma_par = phon_db(text_ph, text_al)
    else:
        sum_par = 0
        denom = 0
        for x in tqdm(range(len(words_ph))):
            try:
                window_words_ph = words_ph[x:(x + window_length)]
                window_words_al = words_al[x:(x + window_length)]
            except IndexError:
                break
            denom += 1
            window_text_ph = ' '.join(window_words_ph).split()
            window_text_al = ' '.join(window_words_al).split()
            sum_par += phon_db(window_text_ph, window_text_al)
        ma_par = safe_divide(sum_par, denom)

    return ma_par


def get_window_coefficient(data_path, window_length=50):
    transcribator = Transcribator(data_path)
    transcribator.transcribe()
    return phon_db_window(transcribator.phonemes, transcribator.allophones, window_length=window_length)


def get_full_coefficient(data_path):
    transcribator = Transcribator(data_path)
    transcribator.transcribe()
    return phon_db(transcribator.phonemes, transcribator.allophones)
