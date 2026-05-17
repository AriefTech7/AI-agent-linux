# AI-agent-linux

## 📋 Gambaran Umum

**AI-agent-linux** adalah asisten pribadi berbasis AI yang berjalan di terminal Linux, dirancang khusus untuk membantu administrasi sistem, otomatisasi, dan produktivitas. Agent ini dapat mengeksekusi perintah Linux, memberikan informasi sistem, dan berinteraksi secara natural dengan pengguna.

Agent bernama **"Alexi"** dengan kepribadian yang tenang, cerdas, dan efisien (terinspirasi JARVIS/FRIDAY dari Avengers).

---

## 🏗️ Arsitektur Proyek

```
AI-agent-linux/
├── main.py                 # Entry point dan logika utama agent
├── system_prompt.py        # Konfigurasi kepribadian & aturan agent
├── pyproject.toml          # Dependensi proyek
└── .env                    # File environment variables (API keys, dll)
```

---

## 🚀 Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| **Eksekusi Perintah Linux** | Menjalankan perintah shell dengan aman |
| **Pengecekan Waktu** | Mendapatkan jam dan tanggal saat ini |
| **Pemilihan Model Dinamis** | Switch antara Ollama (local) dan OpenAI (cloud) berdasarkan kompleksitas percakapan |
| **Manajemen Memori** | Menyimpan riwayat percakapan per thread |
| **Keamanan Terintegrasi** | Memblokir perintah berbahaya secara otomatis |

---

## 🔧 Persyaratan Sistem

### Prasyarat
- **Python** ≥ 3.12
- **Linux** (Ubuntu/Debian/Fedora/Arch direkomendasikan)
- **Ollama** terinstall (untuk model lokal)
- **API Key OpenAI** (opsional, untuk model advanced)


## Contoh Sesi Interaksi
```
🐧 Linux Agent siap. Ketik 'exit' untuk keluar.
User: Lihat jam sekarang
Assistant: Waktu saat ini adalah 14:35.

User: Tolong cek penggunaan disk di /home
Assistant: Saya akan menjalankan 'du -sh /home' untuk Anda.
[Hasil: 2.3G    /home]

User: Hapus semua file log
Assistant: Maaf, saya tidak dapat menghapus semua file log.

User: exit
Exiting...
```
