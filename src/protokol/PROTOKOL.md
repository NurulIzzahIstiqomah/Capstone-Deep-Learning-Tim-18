# Protokol Evaluasi Tim 18

Diisi oleh Penjaga Data & Evaluasi pada Sprint 0.
Protokol diajukan melalui Pull Request dan disetujui
pembimbing sebelum dibekukan.

| Butir | Isi |
|---|---|
| Kasus | Status alat (kipas, lampu, pompa) dari citra |
| Sumber dataset | Menunggu dataset resmi Tim 18 dari Workbench |
| Jenis tugas (`TUGAS`) | Klasifikasi |
| Target / label | Kombinasi status kipas, pompa, dan lampu. `muat()` menghasilkan angka kelas 0–7. Setiap `run.py` mengubahnya menjadi 3 label biner |
| Ukuran data latih / validasi / uji | Menunggu dataset tersedia |
| Cara split | Data uji dipisahkan berdasarkan blok kondisi cahaya yang tidak digunakan saat pelatihan. Data latih dan validasi menggunakan `src.common.split.indeks` dengan seed 2026 dan porsi validasi 10% |
| Metrik utama | Akurasi dan macro-F1 |
| Metrik tambahan | F1-score per alat dan per kondisi cahaya |
| Praproses | Citra kamera 1280 × 720, membuang 1 detik pertama setiap kondisi, membentuk urutan 4 frame berukuran 224 × 224, dan menghitung parameter normalisasi hanya dari data latih |
| Anggaran komputasi per run | Maksimal 20 menit CPU laptop atau sesuai persetujuan pembimbing |
| Evaluasi data uji | Dilakukan satu kali oleh Penjaga Data & Evaluasi pada sprint terakhir menggunakan `--final` |
| `data_hash` saat dibekukan | Menunggu dataset final |

**Persetujuan pembimbing**

Disetujui pada: Menunggu persetujuan pembimbing.

Tautan Pull Request: Menunggu pengajuan PR.