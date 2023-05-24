from phonetic_diversity import get_window_coefficient, get_full_coefficient


if __name__ == "__main__":
    data_path = r"C:\natasha_dataset\marks.txt"
    res_window = get_window_coefficient(data_path)
    res_full = get_full_coefficient(data_path)
    print(res_window, res_full)
