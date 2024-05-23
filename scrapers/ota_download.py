import os

import pandas as pd

from .ota import Ota


class OtaDownload(Ota):
    """
    Class to download scraping results as excel and pdf
    """

    def __init__(self):
        super().__init__()
        self.df = None

    def finish(self):
        self.__download_as_csv()
        self.__download_as_excel()

    def __prepare_for_download(self):
        """
        Utility: Convert to df and creating result/ directory
        """
        if self.df is None:
            self.df = pd.DataFrame(self.scraping_results)
        if not os.path.exists("result"):
            os.makedirs("result")

    def __download_as_excel(self):
        """
        Utility: Download result df as excel
        """
        self.__prepare_for_download()
        file_path = os.path.join("result", "ota.xlsx")  # Default output path
        self.df.to_excel(file_path, sheet_name="Hotels", index=False)
        print(f"Successfully downloaded to {file_path}")

    def __download_as_csv(self):
        """
        Utility: Download result df as csv
        """
        self.__prepare_for_download()
        file_path = os.path.join("result", "ota.csv")  # Default output path
        self.df.to_csv(file_path, sep=",", index=False)
        print(f"Successfully downloaded to {file_path}")
