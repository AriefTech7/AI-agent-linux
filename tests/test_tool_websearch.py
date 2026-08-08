import sys
from pathlib import Path

# Menambahkan root project (folder AI-agent-linux) ke sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
import pytest
from dotenv import load_dotenv
load_dotenv()
from unittest.mock import MagicMock

# cara menjalankan file ini :
# uv run pytest -v -m "integration" test_tool_websearch.py -> menjalankan unit menggunakan API asli Tavily
# uv run pytest -v -m "not integration" test_tool_websearch.py -> menjalankan unit test tanpa memanggil API Tavily

# -----------------------------------------------------------------------------
# Setup environment untuk unit test
# -----------------------------------------------------------------------------
# Jika TAVILY_API_KEY tidak ada, kita isi dummy supaya proses import tool
# tidak gagal saat unit test.
#
# Integration test tetap akan di-skip jika API key masih dummy.
# -----------------------------------------------------------------------------
UNIT_TEST_FALLBACK_API_KEY = "dummy-key-for-unit-test"

if not os.getenv("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = UNIT_TEST_FALLBACK_API_KEY


# -----------------------------------------------------------------------------
# Import module
# -----------------------------------------------------------------------------
# Ganti "app" dengan nama package Anda jika berbeda.
#
# Contoh:
# Jika struktur Anda:
#   mypackage/service.py
#   mypackage/tool_ws.py
#
# Maka import menjadi:
#   from mypackage.service import WebSearchTool
#   from mypackage import tool_ws
# -----------------------------------------------------------------------------

from tools.web_search.service import WebSearchTool
from tools.web_search import tool_ws

# -----------------------------------------------------------------------------
# Helper
# -----------------------------------------------------------------------------
def make_sample_results(n: int = 6):
    """
    Membuat contoh hasil pencarian dari Tavily.
    """
    return [
        {
            "title": f"Title {i}",
            "url": f"https://example.com/{i}",
            "content": f"Content {i}",
            "score": 0.99 - (i * 0.01),
            "raw_content": f"Raw content {i}",
            "extra_field": "should be removed",
        }
        for i in range(n)
    ]


def call_tool(tool_obj, query: str):
    """
    Helper untuk memanggil LangChain tool.

    Beberapa versi LangChain memiliki cara panggil yang sedikit berbeda.
    Helper ini mencoba method yang paling umum:
    - invoke
    - run
    - func
    """
    if hasattr(tool_obj, "invoke"):
        return tool_obj.invoke({"query": query})

    if hasattr(tool_obj, "run"):
        return tool_obj.run(query)

    if hasattr(tool_obj, "func"):
        return tool_obj.func(query)

    raise TypeError("Tool tidak memiliki method invoke, run, atau func.")


def get_tool_description(tool_obj) -> str:
    """
    Mengambil deskripsi tool.
    """
    return (
        getattr(tool_obj, "description", None)
        or getattr(tool_obj, "__doc__", None)
        or ""
    )


# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture
def sample_response():
    """
    Contoh response mentah dari Tavily.
    """
    return {
        "query": "python",
        "answer": "Python adalah bahasa pemrograman.",
        "results": make_sample_results(6),
        "images": [
            "https://example.com/image1.jpg",
            "https://example.com/image2.jpg",
        ],
    }


@pytest.fixture
def mock_tavily(monkeypatch, sample_response):
    """
    Mock TavilyClient agar tidak memanggil API saat unit test.
    """
    mock_client = MagicMock()
    mock_client.search.return_value = sample_response

    mock_constructor = MagicMock(return_value=mock_client)

    # Patch TavilyClient di module service.py
    module_name = WebSearchTool.__module__
    monkeypatch.setattr(
        f"{module_name}.TavilyClient",
        mock_constructor
    )

    return mock_client, mock_constructor


@pytest.fixture
def service(mock_tavily):
    """
    Instance WebSearchTool dengan TavilyClient yang sudah di-mock.
    """
    return WebSearchTool()


@pytest.fixture
def expected_tool_payload():
    """
    Contoh output yang diharapkan dari tool setelah dibersihkan.
    """
    return {
        "query": "python",
        "answer": "Python adalah bahasa pemrograman.",
        "results": [
            {
                "title": "Python Official",
                "url": "https://python.org",
                "content": "Python adalah bahasa pemrograman.",
                "score": 0.99,
            }
        ],
    }


# -----------------------------------------------------------------------------
# Test service.py
# -----------------------------------------------------------------------------
class TestWebSearchService:
    def test_search_basic_calls_tavily_with_correct_params(
        self,
        service,
        mock_tavily
    ):
        """
        Memastikan search_basic memanggil Tavily dengan parameter yang benar.
        """
        mock_client, _ = mock_tavily

        result = service.search_basic("python")

        mock_client.search.assert_called_once_with(
            query="python",
            max_results=5,
            search_depth="basic",
            include_answer=True,
            include_raw_content=False,
            include_images=False,
        )

        assert result["query"] == "python"
        assert result["answer"] == "Python adalah bahasa pemrograman."
        assert "results" in result

    def test_search_basic_returns_only_clean_fields(
        self,
        service
    ):
        """
        Memastikan output hanya berisi field yang dibutuhkan.
        """
        result = service.search_basic("python")

        assert len(result["results"]) > 0

        first_result = result["results"][0]

        assert set(first_result.keys()) == {
            "title",
            "url",
            "content",
            "score",
        }

        assert "extra_field" not in first_result
        assert "raw_content" not in first_result

    def test_search_basic_limits_results_based_on_current_implementation(
        self,
        service
    ):
        """
        Implementasi saat ini memakai:

            results[0:5]

        Artinya hanya 5 hasil yang dikembalikan.

        Jika Anda ingin maksimal 5 hasil, ubah di service.py menjadi:

            results[:5]

        lalu ubah assert di bawah ini menjadi:

            assert len(result["results"]) == 5
        """
        result = service.search_basic("python")

        assert len(result["results"]) == 5

    def test_search_advanced_calls_tavily_with_correct_params(
        self,
        service,
        mock_tavily
    ):
        """
        Memastikan search_advanced memanggil Tavily dengan parameter yang benar.
        """
        mock_client, _ = mock_tavily

        result = service.search_advanced("python")

        mock_client.search.assert_called_once_with(
            query="python",
            max_results=5,
            search_depth="advanced",
            include_answer=True,
            include_raw_content=True,
            include_images=True,
        )

        assert result["query"] == "python"
        assert result["answer"] is not None
        assert "results" in result

    def test_search_advanced_output_does_not_include_raw_content_or_images(
        self,
        service
    ):
        """
        Walaupun search_advanced meminta raw_content dan images,
        output yang dibersihkan saat ini tidak mengembalikan field tersebut.

        Ini penting untuk memastikan output tetap hemat token.
        """
        result = service.search_advanced("python")

        assert "images" not in result

        first_result = result["results"][0]
        assert "raw_content" not in first_result

    def test_search_fast_calls_tavily_with_correct_params(
        self,
        service,
        mock_tavily
    ):
        """
        Memastikan search_fast memanggil Tavily dengan parameter yang benar.

        Catatan:
        Jika versi Tavily Anda tidak mendukung search_depth="fast",
        Anda bisa menyesuaikan implementasi service.py, misalnya:

            search_depth="basic",
            max_results=3,
            include_answer=False

        lalu sesuaikan test ini.
        """
        mock_client, _ = mock_tavily

        result = service.search_fast("python")

        mock_client.search.assert_called_once_with(
            query="python",
            max_results=5,
            search_depth="fast",
            include_answer=True,
            include_raw_content=False,
            include_images=False,
        )

        assert result["query"] == "python"
        assert "results" in result

    def test_empty_response_is_handled(
        self,
        service,
        mock_tavily
    ):
        """
        Jika Tavily mengembalikan response kosong, service tetap harus aman.
        """
        mock_client, _ = mock_tavily
        mock_client.search.return_value = {}

        result = service.search_basic("python")

        assert result == {
            "query": None,
            "answer": None,
            "results": [],
        }

    def test_response_without_results_is_handled(
        self,
        service,
        mock_tavily
    ):
        """
        Jika Tavily tidak mengembalikan results, service tetap harus aman.
        """
        mock_client, _ = mock_tavily
        mock_client.search.return_value = {
            "query": "python",
            "answer": "Python adalah bahasa pemrograman.",
        }

        result = service.search_basic("python")

        assert result["query"] == "python"
        assert result["answer"] == "Python adalah bahasa pemrograman."
        assert result["results"] == []

    def test_response_with_missing_fields_is_handled(
        self,
        service,
        mock_tavily
    ):
        """
        Jika ada field yang hilang di result Tavily, service tetap harus aman.
        """
        mock_client, _ = mock_tavily
        mock_client.search.return_value = {
            "query": "python",
            "results": [
                {
                    "title": "Python",
                    # url hilang
                    "content": "Python adalah bahasa pemrograman.",
                    # score hilang
                }
            ],
        }

        result = service.search_basic("python")

        first_result = result["results"][0]

        assert first_result["title"] == "Python"
        assert first_result["url"] is None
        assert first_result["content"] == "Python adalah bahasa pemrograman."
        assert first_result["score"] is None


# -----------------------------------------------------------------------------
# Test tool_ws.py
# -----------------------------------------------------------------------------
class TestWebSearchTools:
    def test_web_search_basic_tool_calls_service(
        self,
        monkeypatch,
        expected_tool_payload
    ):
        """
        Memastikan tool web_search_basic memanggil service.search_basic.
        """
        mock_search_basic = MagicMock(return_value=expected_tool_payload)

        monkeypatch.setattr(
            tool_ws.search_tool,
            "search_basic",
            mock_search_basic
        )

        result = call_tool(tool_ws.web_search_basic, "python")

        mock_search_basic.assert_called_once_with("python")
        assert result == expected_tool_payload

    def test_web_search_advanced_tool_calls_service(
        self,
        monkeypatch,
        expected_tool_payload
    ):
        """
        Memastikan tool web_search_advanced memanggil service.search_advanced.
        """
        mock_search_advanced = MagicMock(return_value=expected_tool_payload)

        monkeypatch.setattr(
            tool_ws.search_tool,
            "search_advanced",
            mock_search_advanced
        )

        result = call_tool(tool_ws.web_search_advanced, "python")

        mock_search_advanced.assert_called_once_with("python")
        assert result == expected_tool_payload

    def test_web_search_fast_tool_calls_service(
        self,
        monkeypatch,
        expected_tool_payload
    ):
        """
        Memastikan tool web_search_fast memanggil service.search_fast.
        """
        mock_search_fast = MagicMock(return_value=expected_tool_payload)

        monkeypatch.setattr(
            tool_ws.search_tool,
            "search_fast",
            mock_search_fast
        )

        result = call_tool(tool_ws.web_search_fast, "python")

        mock_search_fast.assert_called_once_with("python")
        assert result == expected_tool_payload

    def test_all_tools_have_description(self):
        """
        Memastikan setiap tool memiliki deskripsi.

        Ini penting karena AI agent biasanya memilih tool berdasarkan deskripsi.
        """
        basic_desc = get_tool_description(tool_ws.web_search_basic)
        advanced_desc = get_tool_description(tool_ws.web_search_advanced)
        fast_desc = get_tool_description(tool_ws.web_search_fast)

        assert len(basic_desc) > 0
        assert len(advanced_desc) > 0
        assert len(fast_desc) > 0

    def test_basic_tool_description_mentions_simple_use_case(self):
        """
        Memastikan deskripsi tool basic cukup informatif untuk agent.
        """
        description = get_tool_description(tool_ws.web_search_basic).lower()

        assert "simple" in description or "quick" in description

    def test_advanced_tool_description_mentions_in_depth_use_case(self):
        """
        Memastikan deskripsi tool advanced cukup informatif untuk agent.
        """
        description = get_tool_description(tool_ws.web_search_advanced).lower()

        assert "advanced" in description or "in-depth" in description

    def test_fast_tool_description_mentions_speed_or_quick(self):
        """
        Memastikan deskripsi tool fast menyebutkan pencarian cepat.
        """
        description = get_tool_description(tool_ws.web_search_fast).lower()

        assert "quick" in description or "fast" in description or "rapid" in description


# -----------------------------------------------------------------------------
# Integration test
# -----------------------------------------------------------------------------
# Integration test hanya berjalan jika TAVILY_API_KEY asli tersedia.
#
# Jalankan dengan:
#
#   pytest -v -m integration
#
# Jika tidak ingin menjalankan integration test:
#
#   pytest -v -m "not integration"
# -----------------------------------------------------------------------------
@pytest.mark.integration
@pytest.mark.skipif(
    os.getenv("TAVILY_API_KEY") in ("", UNIT_TEST_FALLBACK_API_KEY),
    reason="TAVILY_API_KEY asli belum diset."
)
class TestWebSearchIntegration:
    def test_basic_search_integration(self):
        """
        Memanggil API Tavily secara nyata menggunakan web_search_basic.
        """
        result = call_tool(
            tool_ws.web_search_basic,
            "Python programming language"
        )

        assert isinstance(result, dict)
        assert "results" in result
        assert isinstance(result["results"], list)

        if result["results"]:
            first = result["results"][0]

            assert "title" in first
            assert "url" in first
            assert "content" in first

    def test_advanced_search_integration(self):
        """
        Memanggil API Tavily secara nyata menggunakan web_search_advanced.
        """
        result = call_tool(
            tool_ws.web_search_advanced,
            "Python FastAPI vs Flask comparison"
        )

        assert isinstance(result, dict)
        assert "results" in result
        assert isinstance(result["results"], list)

    def test_fast_search_integration(self):
        """
        Memanggil API Tavily secara nyata menggunakan web_search_fast.

        Catatan:
        Jika Tavily versi Anda tidak mendukung search_depth="fast",
        test ini bisa gagal. Jika itu terjadi, sesuaikan search_fast
        di service.py.
        """
        result = call_tool(
            tool_ws.web_search_fast,
            "Python"
        )

        assert isinstance(result, dict)
        assert "results" in result
        assert isinstance(result["results"], list)