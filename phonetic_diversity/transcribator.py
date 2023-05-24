from os.path import isdir, isfile, join
from os import listdir
from tqdm import tqdm
from ru_transcript import RuTranscript


class Transcribator:
    def __init__(self, data_path):
        """
        Transcribes text data.

        :param data_path: Path to the dataset: txt file, directory with txt files.
        """
        self.data_path = data_path
        self.phonemes = []
        self.allophones = []
        self.errors = {}

    def _open_file(self):
        with open(self.data_path, encoding='utf-8') as f:
            data = f.readlines()

        return data

    def _open_dir(self):
        files = listdir(self.data_path)
        data = []
        for file in tqdm(files, desc=f'Reading files from {self.data_path}'):
            with open(join(self.data_path, file), encoding='utf-8') as f:
                file_data = f.readlines()
            data.extend(file_data)

        return data

    def transcribe(self):
        if isfile(self.data_path):
            data = self._open_file()
        elif isdir(self.data_path):
            data = self._open_dir()
        else:
            raise ValueError('data_path should be a txt file or a directory with txt files')

        for text in tqdm(data, desc=f'Transcribing text from {self.data_path}'):
            try:
                ru_transcript = RuTranscript(text, stress_place='before')
                ru_transcript.transcribe()
                self.phonemes.extend(ru_transcript.get_phonemes(save_spaces=True))
                self.allophones.extend(ru_transcript.get_allophones(save_spaces=True))
            except Exception as error:
                self.errors[text] = error

    def see_errors(self):
        for k, v in self.errors.items():
            print(f'{k} - {v}')
