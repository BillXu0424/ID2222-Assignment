import os


class TextLoader:
    def __init__(self, dataset_path: str):
        """
        Initialize a text loader.
        :param dataset_path: Path where corpus is stored.
        """

        self.dataset_path = dataset_path

    def load_text(self) -> dict:
        """
        Load all texts from specified dataset path.
        :return: A dict, of which the key is file name and the value is raw text.
        """

        data_dic = {}
        files_name = os.listdir(self.dataset_path)
        for file_name in files_name:
            with open(os.path.join(self.dataset_path, file_name), 'r', encoding='utf-8') as f:
                text = f.read()
            data_dic[file_name] = text.strip()
        return data_dic
