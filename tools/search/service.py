from typing import List
from pathlib import Path

class Search():
    def find_file(self, path: str, filename: str) -> List[str]:
            # hanya untuk menemukan file
            folder = self._get_secure_path(path)

            if not folder.is_dir():
                raise NotADirectoryError(
                    f"Path '{path}' bukan sebuah folder yang valid.")

            return [
                str(file)
                for file in folder.rglob(filename)
                if file.is_file()
            ]
    def locate_file():
        pass
    
    def which_command():
        pass
    
    def whereis_command():
        pass