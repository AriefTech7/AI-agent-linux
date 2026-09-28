# AI Agent Linux

AI Agent Linux adalah asisten AI berbasis terminal untuk pengguna Linux. Agent ini bernama **Alexi** dan dirancang untuk membantu administrasi sistem, manajemen file, pencarian web, produktivitas, serta troubleshooting melalui antarmuka TUI.

Project ini dibangun menggunakan LangGraph, LangChain, OpenAI, Textual, Tavily, dan PostgreSQL sebagai penyimpanan checkpoint/memori.

## Fitur Utama

- Agent ReAct berbasis LangGraph dengan kemampuan memanggil tool secara otomatis.
- Antarmuka terminal interaktif menggunakan Textual.
- Working memory menggunakan LangGraph checkpoint PostgreSQL.
- Episodic memory menggunakan LangGraph PostgreSQL store.
- Integrasi OpenAI melalui `ChatOpenAI`.
- Dukungan model lokal Ollama/Qwen tersedia di modul `llm/qwen.py`.
- Tool manajemen file untuk membaca, membuat, menghapus, memindahkan, menyalin, mengganti nama file, membuat folder, membaca folder, dan menghitung ukuran folder.
- Tool informasi sistem Linux untuk CPU, hostname, kernel, OS, disk, memori, uptime, dan informasi sistem umum.
- Tool pencarian web menggunakan Tavily mode basic dan advanced.
- System prompt khusus untuk karakter Alexi yang fokus pada keamanan, efisiensi, dan administrasi Linux.

## Teknologi

- Python 3.12 atau lebih baru.
- LangGraph untuk graph agent dan checkpoint.
- LangChain untuk integrasi LLM dan tool.
- OpenAI untuk model utama `gpt-5-nano`.
- Ollama untuk opsi model lokal `qwen2.5:3b`.
- Textual untuk terminal UI.
- Tavily untuk pencarian web.
- PostgreSQL untuk checkpoint dan memory store.
- uv untuk manajemen dependency dan menjalankan project.
- pytest untuk testing.

## Struktur Project

```text
AI-agent-linux/
├── agent/
│   └── react_agent.py          # Definisi graph agent LangGraph
├── config/
│   └── connect_db.py           # Koneksi PostgreSQL untuk checkpoint dan store
├── helper/
│   ├── flow_graph.py           # Helper tambahan untuk graph
│   └── stream.py               # Helper streaming output
├── llm/
│   ├── chatgpt.py              # Konfigurasi model OpenAI
│   └── qwen.py                 # Konfigurasi model Ollama/Qwen
├── memory/
│   ├── episodic.py             # Episodic memory berbasis PostgreSQL store
│   ├── procedural.py           # Modul memori prosedural
│   ├── semantic.py             # Modul memori semantik
│   └── working.py              # Wrapper working memory/checkpointer
├── tools/
│   ├── file_management/        # Tool operasi file dan folder
│   ├── linux_system/           # Tool informasi sistem Linux
│   ├── web_search/             # Tool pencarian web Tavily
│   └── tool_manager.py         # Registrasi semua tool agent
├── tui/
│   └── app.py                  # Textual TUI untuk chat Alexi
├── tests/                      # Unit/integration test
├── main.py                     # Entry point aplikasi
├── system_prompt.py            # Persona, aturan, dan safety policy Alexi
├── pyproject.toml              # Metadata dan dependency project
├── .env.example                # Contoh environment variable
└── uv.lock                     # Lockfile dependency uv
```

## Cara Kerja Singkat

1. `main.py` membuat koneksi PostgreSQL untuk working memory dan episodic memory.
2. `agent/react_agent.py` membuat graph LangGraph dengan node `agent` dan `tool`.
3. Model OpenAI dari `llm/chatgpt.py` di-bind dengan daftar tool dari `tools/tool_manager.py`.
4. Saat user mengirim pesan melalui TUI, graph menentukan apakah perlu menjawab langsung atau memanggil tool.
5. Jika ada tool call, node `tool` menjalankan tool lalu hasilnya dikirim kembali ke agent untuk dibuatkan jawaban akhir.
6. Percakapan disimpan menggunakan checkpoint PostgreSQL berdasarkan `thread_id`.

## Prasyarat

- Linux.
- Python 3.12 atau lebih baru. File `.python-version` pada project saat ini berisi `3.14`.
- PostgreSQL aktif dan dapat diakses.
- OpenAI API key.
- Tavily API key jika ingin memakai fitur web search.
- uv terinstall.
- Ollama opsional jika ingin memakai model lokal dari `llm/qwen.py`.

## Instalasi

Clone atau masuk ke folder project:

```bash
cd /home/awn/Projects/experiman/chatbot/AI-agent-linux
```

Install dependency menggunakan uv:

```bash
uv sync
```

Jika tidak memakai uv, dependency dapat dilihat di `pyproject.toml`.

## Konfigurasi Environment

Salin file contoh environment:

```bash
cp .env.example .env
```

Isi nilai berikut sesuai kebutuhan:

```env
OPENAI_API_KEY=your-api-key
LANGSMITH_ENDPOINT=your-api-key
LANGSMITH_API_KEY=your-api-key
LANGSMITH_PROJECT="your-name-project"
TAVILY_API_KEY=your-api-key

DB_HOST=localhost
DB_NAME=your-name-database
DB_USER=your-user-database
DB_PASSWORD=your-password-database
DB_PORT=your-port-database
```

Catatan: implementasi saat ini di `config/connect_db.py` masih memakai `DB_URL` hardcoded:

```python
postgresql://agent_linux:linux@localhost:5432/aiagentdb?sslmode=disable
```

Pastikan PostgreSQL memiliki user, password, host, port, dan database yang sesuai dengan nilai tersebut, atau ubah `DB_URL` di `config/connect_db.py` agar sesuai dengan environment lokal.

## Setup Database

Buat user dan database PostgreSQL sesuai konfigurasi default project:

```bash
createdb aiagentdb
```

Jika user `agent_linux` belum ada, buat user tersebut di PostgreSQL dan berikan akses ke database `aiagentdb`.

LangGraph checkpointer/store membutuhkan tabel internal. Di `main.py` pemanggilan `setup()` masih dikomentari:

```python
# await checkpointer.setup()
# await store.setup()
```

Jika database masih kosong dan aplikasi gagal karena tabel belum tersedia, aktifkan sementara baris setup tersebut atau jalankan setup dari script terpisah sesuai dokumentasi LangGraph PostgreSQL.

## Menjalankan Aplikasi

Jalankan aplikasi TUI:

```bash
uv run python main.py
```

Shortcut TUI:

- `Ctrl+C` untuk keluar.
- `Ctrl+N` untuk membuat percakapan baru dengan `thread_id` baru.

## Tool Yang Tersedia

### File Management

Tool berada di `tools/file_management/` dan didaftarkan melalui `tools/tool_manager.py`.

- `filesystem_read_file`
- `filesystem_delete_file`
- `filesystem_move_file`
- `filesystem_copy_file`
- `filesystem_rename_file`
- `filesystem_create_file`
- `filesystem_create_folder`
- `filesystem_read_folder`
- `filesystem_get_folder_size`

Operasi file dibatasi oleh `_get_secure_path()` di `tools/file_management/service.py` agar akses tidak keluar dari base directory yang dihitung oleh service.

### Linux System

Tool berada di `tools/linux_system/`.

- `get_cpu_info`
- `get_hostname`
- `get_os_info`
- `get_kernel_info`
- `get_disk_usage`
- `get_memory_usage`
- `get_uptime`
- `get_system_info`

Tool ini menjalankan perintah Linux seperti `lscpu`, `hostname`, `uname -a`, `df -h`, `free -h`, `uptime`, dan `hostnamectl` menggunakan `subprocess.run()` dengan `shell=False`.

### Web Search

Tool berada di `tools/web_search/` dan membutuhkan `TAVILY_API_KEY`.

- `web_search_basic` untuk pencarian cepat dan faktual.
- `web_search_advanced` untuk riset lebih mendalam.

Hasil pencarian dibersihkan agar hanya mengembalikan query, jawaban ringkas, dan maksimal 5 sumber.

## Model LLM

Model utama yang aktif saat ini ada di `llm/chatgpt.py`:

```python
ChatOpenAI(
    model='gpt-5-nano',
    temperature=0.7
)
```

Modul `llm/qwen.py` menyediakan konfigurasi Ollama:

```python
ChatOllama(
    model='qwen2.5:3b',
    temperature=0
)
```

Saat ini agent di `agent/react_agent.py` menggunakan `llm/chatgpt.py`.

## Memory

Project memiliki dua jenis memori utama:

- Working memory: wrapper untuk `AsyncPostgresSaver` di `memory/working.py`.
- Episodic memory: wrapper untuk `AsyncPostgresStore` di `memory/episodic.py`.

Working memory dipakai sebagai checkpointer saat graph dikompilasi. Episodic memory dikirim sebagai `store` ke LangGraph dan menyediakan method untuk mengambil, menyimpan, mencari, menghapus, dan melihat namespace memory.

## Testing

Jalankan test dengan:

```bash
uv run pytest
```

Menjalankan test tanpa integration test:

```bash
uv run pytest -m "not integration"
```

Menjalankan integration test Tavily:

```bash
uv run pytest -m integration
```

Catatan: beberapa file test saat ini terlihat belum sinkron dengan struktur folder terbaru, misalnya masih mengacu ke `tools.filesystem`, sedangkan implementasi aktual berada di `tools.file_management`. Jika test gagal karena import path, sesuaikan test ke struktur folder terbaru.

## Catatan Keamanan

System prompt di `system_prompt.py` menginstruksikan Alexi untuk:

- Tidak menjalankan perintah destruktif tanpa konfirmasi.
- Memblokir perintah berbahaya seperti `rm -rf /`, `mkfs`, fork bomb, dan pola malware.
- Meminta konfirmasi sebelum menghapus file, mengubah konfigurasi sistem, menginstal/menghapus paket, membunuh proses penting, atau mengubah permission secara rekursif.
- Menggunakan tool sistem saat user meminta informasi sistem.

Namun, tetap review implementasi tool sebelum memberi akses ke environment penting karena sebagian safety policy berada di prompt, bukan seluruhnya dipaksakan di layer kode.

## Troubleshooting

Jika aplikasi gagal karena OpenAI API key:

- Pastikan `.env` berisi `OPENAI_API_KEY` yang valid.
- Pastikan `load_dotenv()` berhasil membaca file `.env` dari root project.

Jika aplikasi gagal terhubung ke database:

- Periksa `DB_URL` di `config/connect_db.py`.
- Pastikan PostgreSQL berjalan.
- Pastikan database `aiagentdb` ada.
- Pastikan user `agent_linux` memiliki akses.
- Jalankan setup tabel LangGraph jika tabel checkpoint/store belum tersedia.

Jika web search gagal:

- Pastikan `TAVILY_API_KEY` valid.
- Jalankan test non-integration terlebih dahulu untuk memastikan logic service berjalan tanpa API asli.

Jika tool file tidak bisa mengakses path yang diinginkan:

- Periksa base directory di `FileService.base_dir`.
- `_get_secure_path()` sengaja menolak akses di luar base directory untuk alasan keamanan.

## Lisensi

Project ini menggunakan lisensi Apache 2.0. Lihat file [LICENSE](LICENSE).

## Author

- LinkedIn: https://www.linkedin.com/in/arif-wahyudi-8058462a7/
- Instagram: https://www.instagram.com/arf_wahyudi/
