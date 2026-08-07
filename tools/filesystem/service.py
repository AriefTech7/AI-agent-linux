from pathlib import Path


class FileService:

    def read_file(self, path: str):
        # hanya untuk membaca file
        file = Path(path)

        if not file.is_file():
            raise FileNotFoundError(path)

        return file.read_text(encoding="utf-8")

    def delete_file(self, path: str) -> dict:
        # hanya untuk menghapus file
        file = Path(path)

        if not file.is_file():
            raise FileNotFoundError(path)

        return {
            "success": True,
            "deleted": str(file)
        }

    def move_file(self, pathNow: str, pathTo: str) -> dict:
        # hanya untuk memindahkan file
        file_now = Path(pathNow)
        file_to = Path(pathTo)

        if not file_now.is_file():
            raise FileNotFoundError(pathNow)

        file_to.parent.mkdir(parents=True, exist_ok=True)
        new_path = file_now.move(file_to)

        return {
            "success": True,
            "destination": str(new_path),
            "source": str(file_now)
        }

    def copy_file(self, source: str, destination: str) -> dict:
        # hanya untuk mencopy file
        src = Path(source)
        dst = Path(destination)

        if not src.is_file():
            raise FileNotFoundError(source)

        dst.parent.mkdir(parents=True, exist_ok=True)

        copied = src.copy(dst)

        return {
            "success": True,
            "source": str(src),
            "destination": str(copied)
        }

    def rename_file(self, path: str, new_name_file:str):
        # hanya untuk mengubah nama file
        old_file = Path(path)

        if not old_file.is_file():
            raise FileNotFoundError(path)

        new_file_path = old_file.with_name(new_name_file)
        old_file.rename(new_file_path)

        return {
            "success": True,
            "old_name": old_file.name,
            "new_name": new_file_path.name
        }

    def create_file(self, path: str, filename: str) -> dict:
        # hanya untuk membuat file baru
        file = Path(path) / filename
        file.parent.mkdir(parents=True, exist_ok=True)

        file.touch(exist_ok=False)

        return {
            "success": True,
            "path": str(file)
        }

    def find_file(self, path: str, filename: str) -> list[str]:
        # hanya untuk menemukan file
        folder = Path(path)

        if not folder.is_dir():
            raise NotADirectoryError(
                f"Path '{path}' bukan sebuah folder yang valid.")

        return [
            str(file)
            for file in folder.rglob(filename)
            if file.is_file()
        ]

    def create_folder(self, path: str, nameFolder: str) -> dict:
        # hanya untuk membuat folder baru
        folder_baru = Path(path) / nameFolder

        folder_baru.mkdir(exist_ok=True)

        return {
            "success": True,
            "path": str(folder_baru)
        }

    def read_folder(self, path: str) -> list[dict]:
        # hanya untuk melihat isi folder
        folder = Path(path)

        if not folder.is_dir():
            raise NotADirectoryError(path)

        return [
            {
                "name": item.name,
                "path": str(item),
                "type": "directory" if item.is_dir() else "file"
            }
            for item in folder.iterdir()
        ]

    def check_size_folder(self, path: str) -> dict:
        # hanya untuk cek size folder
        folder = Path(path)

        if not folder.is_dir():
            raise NotADirectoryError(path)

        total_size = sum(
            f.stat().st_size
            for f in folder.rglob('*')
            if f.is_file())

        return {
            "bytes": total_size,
            "kb": round(total_size / 1024, 2),
            "mb": round(total_size / (1024**2), 2),
            "gb": round(total_size / (1024**3), 2)
        }
