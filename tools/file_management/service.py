from pathlib import Path
from typing import Dict,List


class FileService:
    def __init__(self):
        # Kunci semua operasi ke direktori utama (root proyek)
        self.base_dir = Path("/home/aiAgent").resolve().parent.parent.parent
        
    def _get_secure_path(self, user_path: str) -> Path:
        """
        Fungsi internal pembantu (helper) untuk mengamankan path.
        Menggabungkan path dari user dengan base_dir, lalu memastikan
        hasil akhirnya tidak keluar dari folder proyek.
        """
        # Hapus awalan '/' atau '\' agar tidak dianggap sebagai path absolut root sistem linux/windows
        clean_path = str(user_path).lstrip("/\\")
        
        # Resolve akan mengeksekusi '../' dan menghasilkan path absolut asli
        target_path = (self.base_dir / clean_path).resolve()

        # VALIDASI KEAMANAN: Pastikan path tujuan diawali dengan path proyek kita
        if not str(target_path).startswith(str(self.base_dir)):
            raise PermissionError(f"Security Alert: Akses ditolak! Path '{user_path}' berada di luar direktori proyek.")
            
        return target_path
    
    def read_file(self, path: str)->str:
        # hanya untuk membaca file
        file = self._get_secure_path(path)

        if not file.is_file():
            raise FileNotFoundError(path)

        return file.read_text(encoding="utf-8")

    def delete_file(self, path: str) -> Dict:
        # hanya untuk menghapus file
        file = self._get_secure_path(path)

        if not file.is_file():
            raise FileNotFoundError(path)
        
        file.unlink()

        return {
            "success": True,
            "deleted": str(file)
        }

    def move_file(self, pathNow: str, pathTo: str) -> Dict:
        # hanya untuk memindahkan file
        file_now = self._get_secure_path(pathNow)
        file_to = self._get_secure_path(pathTo)

        if not file_now.is_file():
            raise FileNotFoundError(pathNow)

        file_to.parent.mkdir(parents=True, exist_ok=True)
        new_path = file_now.move(file_to)

        return {
            "success": True,
            "destination": str(new_path),
            "source": str(file_now)
        }

    def copy_file(self, source: str, destination: str) -> Dict:
        # hanya untuk mencopy file
        src = self._get_secure_path(source)
        dst = self._get_secure_path(destination)

        if not src.is_file():
            raise FileNotFoundError(source)

        dst.parent.mkdir(parents=True, exist_ok=True)

        copied = src.copy(dst)

        return {
            "success": True,
            "source": str(src),
            "destination": str(copied)
        }

    def rename_file(self, path: str, new_name_file:str)->Dict:
        # hanya untuk mengubah nama file
        old_file = self._get_secure_path(path)

        if not old_file.is_file():
            raise FileNotFoundError(path)

        new_file_path = old_file.with_name(new_name_file)
        old_file.rename(new_file_path)

        return {
            "success": True,
            "old_name": old_file.name,
            "new_name": new_file_path.name
        }

    def create_file(self, path: str, filename: str) -> Dict:
        # hanya untuk membuat file baru
        file = self._get_secure_path(path) / filename
        file.parent.mkdir(parents=True, exist_ok=True)

        file.touch(exist_ok=False)

        return {
            "success": True,
            "path": str(file)
        }

    

    def create_folder(self, path: str, nameFolder: str) -> Dict:
        # hanya untuk membuat folder baru
        folder_baru = self._get_secure_path(path) / nameFolder

        folder_baru.mkdir(exist_ok=True)

        return {
            "success": True,
            "path": str(folder_baru)
        }

    def read_folder(self, path: str) -> List[Dict]:
        # hanya untuk melihat isi folder
        folder = self._get_secure_path(path)

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

    def check_size_folder(self, path: str) -> Dict:
        # hanya untuk cek size folder
        folder = self._get_secure_path(path)

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
    
    # def write_file_service(self):
