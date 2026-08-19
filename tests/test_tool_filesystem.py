
import sys
from pathlib import Path

# Menambahkan root project (folder AI-agent-linux) ke sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pytest
from unittest.mock import patch, MagicMock

# Import class dan fungsi tool
from tools.filesystem.service import FileService
from tools.filesystem.tool import (
    filesystem_read_file,
    filesystem_delete_file,
    filesystem_move_file,
    filesystem_copy_file,
    filesystem_rename_file,
    filesystem_create_file,
    filesystem_find_file,
    filesystem_create_folder,
    filesystem_read_folder,
    filesystem_get_folder_size,
)


# =====================================================================
# 1. TEST UNIT FOR FileService (service.py)
# =====================================================================

class TestFileService:

    @pytest.fixture
    def service(self):
        return FileService()

    def test_create_and_read_file(self, service, tmp_path):
        # Test create_file
        res = service.create_file(str(tmp_path), "test.txt")
        file_path = tmp_path / "test.txt"
        
        assert res["success"] is True
        assert file_path.exists()

        # Isi konten manual
        file_path.write_text("Hello World", encoding="utf-8")

        # Test read_file
        content = service.read_file(str(file_path))
        assert content == "Hello World"

    def test_read_file_not_found(self, service, tmp_path):
        non_existing = tmp_path / "not_found.txt"
        with pytest.raises(FileNotFoundError):
            service.read_file(str(non_existing))

    def test_create_file_already_exists(self, service, tmp_path):
        service.create_file(str(tmp_path), "existing.txt")
        # Touch exist_ok=False akan melempar FileExistsError jika file sudah ada
        with pytest.raises(FileExistsError):
            service.create_file(str(tmp_path), "existing.txt")

    def test_delete_file(self, service, tmp_path):
        file_path = tmp_path / "to_delete.txt"
        file_path.touch()

        res = service.delete_file(str(file_path))
        assert res["success"] is True
        assert not file_path.exists()

    def test_delete_file_not_found(self, service, tmp_path):
        with pytest.raises(FileNotFoundError):
            service.delete_file(str(tmp_path / "ghost.txt"))

    def test_rename_file(self, service, tmp_path):
        old_file = tmp_path / "old_name.txt"
        old_file.touch()

        res = service.rename_file(str(old_file), "new_name.txt")
        assert res["success"] is True
        assert res["old_name"] == "old_name.txt"
        assert res["new_name"] == "new_name.txt"
        assert (tmp_path / "new_name.txt").exists()
        assert not old_file.exists()

    def test_create_and_read_folder(self, service, tmp_path):
        # Test create_folder
        res = service.create_folder(str(tmp_path), "my_folder")
        folder_path = tmp_path / "my_folder"
        
        assert res["success"] is True
        assert folder_path.is_dir()

        # Buat dummy file di dalam folder
        (folder_path / "file1.txt").touch()

        # Test read_folder
        contents = service.read_folder(str(folder_path))
        assert len(contents) == 1
        assert contents[0]["name"] == "file1.txt"
        assert contents[0]["type"] == "file"

    def test_find_file(self, service, tmp_path):
        sub_dir = tmp_path / "subdir"
        sub_dir.mkdir()
        (sub_dir / "target.txt").touch()
        (tmp_path / "other.log").touch()

        results = service.find_file(str(tmp_path), "*.txt")
        assert len(results) == 1
        assert "target.txt" in results[0]

    def test_check_size_folder(self, service, tmp_path):
        # Buat file dengan ukuran 1024 bytes (1 KB)
        file1 = tmp_path / "file1.bin"
        file1.write_bytes(b"a" * 1024)

        size_info = service.check_size_folder(str(tmp_path))
        assert size_info["bytes"] == 1024
        assert size_info["kb"] == 1.0

    @patch.object(Path, "move")
    def test_move_file(self, mock_move, service, tmp_path):
        # Menguji move_file (menggunakan mock karena Pathlib standar Python tidak memiliki metode .move())
        src = tmp_path / "src.txt"
        src.touch()
        dst = tmp_path / "sub" / "dst.txt"
        mock_move.return_value = dst

        res = service.move_file(str(src), str(dst))
        assert res["success"] is True
        assert res["destination"] == str(dst)

    @patch.object(Path, "copy")
    def test_copy_file(self, mock_copy, service, tmp_path):
        # Menguji copy_file (menggunakan mock karena Pathlib standar Python tidak memiliki metode .copy())
        src = tmp_path / "src.txt"
        src.touch()
        dst = tmp_path / "dst.txt"
        mock_copy.return_value = dst

        res = service.copy_file(str(src), str(dst))
        assert res["success"] is True
        assert res["destination"] == str(dst)


# =====================================================================
# 2. TEST INTEGRATION FOR LangChain Tools (tool.py)
# =====================================================================

class TestLangChainTools:

    @patch("tools.filesystem.tool.file_service")
    def test_filesystem_read_file_tool(self, mock_service):
        mock_service.read_file.return_value = "content from service"
        
        # Panggil tool menggunakan `.invoke()` (standar LangChain Tool)
        result = filesystem_read_file.invoke({"path": "/path/to/file.txt"})
        
        mock_service.read_file.assert_called_once_with("/path/to/file.txt")
        assert result == "content from service"

    @patch("tools.filesystem.tool.file_service")
    def test_filesystem_create_file_tool(self, mock_service):
        mock_service.create_file.return_value = {"success": True, "path": "/path/data.txt"}
        
        result = filesystem_create_file.invoke({"path": "/path", "filename": "data.txt"})
        
        mock_service.create_file.assert_called_once_with("/path", "data.txt")
        assert result == {"success": True, "path": "/path/data.txt"}

    @patch("tools.filesystem.tool.file_service")
    def test_filesystem_delete_file_tool(self, mock_service):
        mock_service.delete_file.return_value = {"success": True, "deleted": "/path/file.txt"}
        
        result = filesystem_delete_file.invoke({"path": "/path/file.txt"})
        
        mock_service.delete_file.assert_called_once_with("/path/file.txt")
        assert result == {"success": True, "deleted": "/path/file.txt"}

    @patch("tools.filesystem.tool.file_service")
    def test_filesystem_create_folder_tool(self, mock_service):
        mock_service.create_folder.return_value = {"success": True, "path": "/path/Backups"}
        
        result = filesystem_create_folder.invoke({"path": "/path", "nameFolder": "Backups"})
        
        mock_service.create_folder.assert_called_once_with("/path", "Backups")
        assert result == {"success": True, "path": "/path/Backups"}