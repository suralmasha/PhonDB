def safe_divide(numerator, denominator):
    try:
        # return round(numerator / denominator, round_to)
        return numerator / denominator
    except ZeroDivisionError:
        return 0


def get_weights(vowels, sonorous, voiced, voiceless):
    groups = {'vowels': vowels, 'sonorous': sonorous, 'voiced': voiced, 'voiceless': voiceless}
    full_sum = sum(list(groups.values()))

    weights = []
    for k, v in groups.items():
        w = round(safe_divide((v * 100), full_sum), 2)
        weights.append(w)

    return weights
