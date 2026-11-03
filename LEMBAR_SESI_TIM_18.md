# Lembar Sesi Eksperimen Meja Uji — Tim 18

**Kasus:** Status Alat (Kipas, Lampu, Pompa) dari Citra (Klasifikasi Multi-label)  
**Meja Uji:** Ruang Cerdas 5 V, Lab Sains Data ITERA  
**Dosen Pembimbing:** Ade Lailani  
**Total Kondisi:** 144 (Seed: 1018) | 6 s rekam + 1 s jeda (~17 menit bersih, ~21 menit dengan pergantian blok)  
**Muat di slot:** slot 60 menit dikurangi persiapan dan penutupan ±10 menit = ±50 menit rekam efektif; perkiraan ±21 menit sehingga muat.

## Jadwal Penting

| Tanggal | Kegiatan |
|:--------|:---------|
| **Rabu, 4 Nov 2026, 12.00 WIB** | Batas rencana final `t18-status-alat-citra.yaml`: (a) disetujui pembimbing (komentar persetujuan di tugas) **dan** (b) berkas final diserahkan ke pengelola meja |
| **Senin, 9 Nov 2026, 10.00–11.00 WIB** | Slot Operator (hadir 09.50) |
| Kamis, 12 Nov 2026 | Slot cadangan (bila sesi gagal/terpotong) |
| **Minggu, 15 Nov 2026** | Demo Sprint 1: tiap jalur dilatih pada data primer (min. 1 seed), pembanding non-DL berjalan, `metrics.json` valid |
| 16–23 Nov 2026 | Sprint 2: 3 seed, penyetelan, perbandingan lengkap |
| **Rabu, 18 Nov 2026, 09.00–09.30 WIB** | Uji purwarupa Sprint 2 |

> Data baru tersedia setelah 9 Nov, sehingga hanya ±6 hari menuju Demo Sprint 1. Seluruh persiapan kode (pemotong jendela, `PROTOKOL.md`, pembanding non-DL) harus sudah berjalan pada data mode simulasi **sebelum** slot.

---

## Pembagian Peran di Meja
1. **Koordinator Sesi:** Kevin Antoni Junior
2. **Operator Rekam:** Nurul Izzah Istiqomah (menekan Enter setelah pembimbing memeriksa) *(usulan)*
3. **Operator Alat:** Hanifah Inaya Sani (memasang keadaan cahaya ruang tiap blok) *(usulan)*
4. **Pencatat Kejadian:** Luthfia Laila Ramadhani (mencatat nomor kondisi yang terganggu) *(usulan)*
5. **Penjaga Bingkai:** Refa Destiny Pranata (memastikan tidak ada tangan, badan, atau bayangan di bingkai) *(usulan)*

Pembimbing memeriksa pengaturan ruang sebelum setiap blok dimulai. Peran bertanda *(usulan)* dikonfirmasi bersama pembimbing sebelum 9 Nov.

## Pembagian Jalur Model (setelah data tersedia)

| Jalur | Penanggung jawab |
|:------|:-----------------|
| CNN | Nurul Izzah Istiqomah |
| TL (transfer learning) | Luthfia Laila Ramadhani |
| RNN (CNN-LSTM atas urutan frame) | Refa Destiny Pranata |
| Transformer | Kevin Antoni Junior |
| AE (autoencoder) | Hanifah Inaya Sani |
| Pembanding non-DL (histogram warna + HOG + Random Forest) | Kevin Antoni Junior  |

---

## Rencana Singkat

| Butir | Keterangan |
|:------|:-----------|
| Faktor manual | `cahaya_ruang`: lampu ruang menyala, lampu ruang mati, jendela/tirai terbuka (3 blok) |
| Faktor otomatis | `kipas`, `pompa`, `lampu`: masing-masing 0 atau 255 (8 kombinasi) |
| Struktur | 3 blok × 8 kombinasi × 6 ulangan = 144 kondisi (48 per blok, diacak dalam blok) |
| Perekam aktif | Kamera 1280×720 tiap 0,5 detik; sensor ESP32 (getaran, arus, suhu, kelembapan, lux, PIR, pintu) |
| Audio | Nonaktif |
| Label | Kolom `kipas`, `pompa`, `lampu` (dari perintah skrip); cahaya ruang dari `cahaya_ruang`; lux dari `lux` |
| Masukan model | Urutan **4 frame 224×224** (citra 1280×720 diperkecil; 4 frame agar kipas berputar dapat dibedakan dari kipas diam); 1 detik pertama tiap kondisi dibuang |
| Metrik | **F1 per alat, per kondisi cahaya**; rata-rata ± simpangan dari 3 seed; ukuran ONNX (KB); latensi (ms) di laptop meja |
| Pemisahan data | Data uji dipisah **per blok cahaya**; normalisasi dihitung dari data latih saja |

**8 kombinasi alat (acuan):**

| Kombinasi | Kipas | Pompa | Lampu meja |
|:---------:|:-----:|:-----:|:----------:|
| 1 | 0 | 0 | 0 |
| 2 | 0 | 0 | 255 |
| 3 | 0 | 255 | 0 |
| 4 | 0 | 255 | 255 |
| 5 | 255 | 0 | 0 |
| 6 | 255 | 0 | 255 |
| 7 | 255 | 255 | 0 |
| 8 | 255 | 255 | 255 |

## Definisi Operasional Faktor Manual (`cahaya_ruang`)
Disepakati tim dan pembimbing sebelum slot; dibacakan dengan kalimat yang sama pada setiap blok.

| Taraf | Lampu ruang | Tirai/jendela | Pintu ruang | Lux acuan (kira-kira) |
|:------|:-----------:|:-------------:|:-----------:|:---------------------:|
| lampu ruang menyala | | | | |
| lampu ruang mati | | | | |
| jendela/tirai terbuka | | | | |

*Isi keadaan tiap benda (mis. menyala/mati, terbuka/tertutup) sehingga tiga taraf berbeda jelas dan konsisten antar-blok.*

---

## A. Checklist Sebelum Hari Slot (selesai sebelum Senin 9 Nov)
- [ ] Rencana final `t18-status-alat-citra.yaml` disetujui pembimbing (komentar persetujuan di tugas) dan berkas diserahkan ke pengelola meja **paling lambat Rabu, 4 Nov 2026 pukul 12.00**.
- [ ] Seluruh anggota dapat menjelaskan faktor, taraf, dan asal label (kolom `kipas`, `pompa`, `lampu` dari perintah skrip; `cahaya_ruang` dari desain; `lux` dari sensor).
- [ ] Definisi operasional `cahaya_ruang` (tabel di atas) terisi dan disetujui pembimbing.
- [ ] Perkiraan durasi dan jumlah kondisi yang dicetak mode simulasi dicocokkan dengan angka di lembar ini (termasuk format nomor kondisi di layar; sesuaikan kolom "Kondisi ID" bila berbeda).
- [ ] Jalankan mode simulasi: `python meja.py --simulasi jalankan ../rencana/t18-status-alat-citra.yaml`
- [ ] Skrip mencetak **144 kondisi**.
- [ ] Pemotong jendela (4 frame) diuji pada folder sesi simulasi.
- [ ] `PROTOKOL.md` dan pembanding non-DL berjalan pada data mode simulasi.
- [ ] Pembagian peran dan jalur disepakati (kolom *usulan* dikonfirmasi pembimbing).

## B. Checklist Hari Slot — Sebelum Menyalakan Skrip
- [ ] Datang **10 menit lebih awal** (09.50); program harian dihentikan oleh pengelola meja.
- [ ] Berkas rencana final diserahkan ke pengelola; namanya `t18-…yaml` dan isinya sama dengan versi yang disetujui pembimbing.
- [ ] Pengelola menjalankan `python meja.py periksa`: ESP32 dan kamera terdeteksi (sensor ESP32 merekam).
- [ ] Air di wadah A cukup untuk seluruh sesi (pompa menyala total ±7 menit; pompa tidak boleh menyala kering).
- [ ] Bingkai kamera cocok dengan foto acuan meja; tiang kamera tidak digeser sedikit pun selama sesi.
- [ ] Benda di luar rencana disingkirkan dari bingkai (termasuk tas dan botol minum tim).
- [ ] Saklar lampu ruang dan tirai dapat diatur selama slot.
- [ ] Cuaca saat slot dicatat: ______________________
- [ ] Seluruh anggota berada pada posisi masing-masing dan di luar bingkai.
- [ ] Uji satu kondisi: jalankan rencana asli, Ctrl+C setelah 1–2 kondisi, cek bingkai kamera dan instruksi layar. Beri catatan "uji" di lembar sesi (tidak dipakai sebagai data).

---

## Keselamatan
- Tidak ada cairan di dekat ESP32 dan laptop; pompa tidak dijalankan dalam keadaan kering.
- Tangan tidak dimasukkan ke kisi kipas yang berputar.
- Bila tercium bau hangus atau ada kabel panas: hentikan sesi dengan **Ctrl+C** dan beri tahu pengelola meja.
- Bila tidak ada perintah dari laptop selama 10 detik, ESP32 mematikan semua alat sebagai pengaman.

---

## Alur Pergantian Blok (Ulangi 3 Kali)
1. Layar menampilkan, misalnya, *Siapkan: Atur ruang: lampu ruang menyala*.
2. Operator Alat memasang keadaan cahaya ruang tersebut.
3. Pembimbing memeriksa.
4. **Tunggu ±10 detik** agar pengaturan otomatis kamera stabil.
5. Operator Rekam menekan **Enter** hanya setelah tangan semua orang lepas dari meja dan semua anggota berada di luar bingkai.
6. Selama kondisi berlangsung: tidak ada tangan, badan, atau bayangan di bingkai.

**Urutan blok (diacak seed 1018, isi sesuai tampilan layar):**

| Urutan | Keadaan cahaya ruang | Cuaca / catatan | Lux (kira-kira) | Jam mulai | Jam selesai |
|:------:|:---------------------|:----------------|:---------------:|:---------:|:-----------:|
| Blok 1 | | | | | |
| Blok 2 | | | | | |
| Blok 3 | | | | | |

*Kolom Kipas/Pompa/Lampu pada tabel di bawah diisi 0 atau 255 sesuai tampilan layar. Nomor kondisi tetap berurutan 001–144 lintas blok.*

---

## Catatan Kondisi Blok 1 (Kondisi 001–048) — Cahaya: ______________________

| No | Kondisi ID | Kipas | Pompa | Lampu | Status | Catatan Gangguan |
|:--:|:----------:|:-----:|:-----:|:-----:|:------:|:-----------------|
| 1 | [001/144] | | | | [ ] OK | |
| 2 | [002/144] | | | | [ ] OK | |
| 3 | [003/144] | | | | [ ] OK | |
| 4 | [004/144] | | | | [ ] OK | |
| 5 | [005/144] | | | | [ ] OK | |
| 6 | [006/144] | | | | [ ] OK | |
| 7 | [007/144] | | | | [ ] OK | |
| 8 | [008/144] | | | | [ ] OK | |
| 9 | [009/144] | | | | [ ] OK | |
| 10 | [010/144] | | | | [ ] OK | |
| 11 | [011/144] | | | | [ ] OK | |
| 12 | [012/144] | | | | [ ] OK | |
| 13 | [013/144] | | | | [ ] OK | |
| 14 | [014/144] | | | | [ ] OK | |
| 15 | [015/144] | | | | [ ] OK | |
| 16 | [016/144] | | | | [ ] OK | |
| 17 | [017/144] | | | | [ ] OK | |
| 18 | [018/144] | | | | [ ] OK | |
| 19 | [019/144] | | | | [ ] OK | |
| 20 | [020/144] | | | | [ ] OK | |
| 21 | [021/144] | | | | [ ] OK | |
| 22 | [022/144] | | | | [ ] OK | |
| 23 | [023/144] | | | | [ ] OK | |
| 24 | [024/144] | | | | [ ] OK | |
| 25 | [025/144] | | | | [ ] OK | |
| 26 | [026/144] | | | | [ ] OK | |
| 27 | [027/144] | | | | [ ] OK | |
| 28 | [028/144] | | | | [ ] OK | |
| 29 | [029/144] | | | | [ ] OK | |
| 30 | [030/144] | | | | [ ] OK | |
| 31 | [031/144] | | | | [ ] OK | |
| 32 | [032/144] | | | | [ ] OK | |
| 33 | [033/144] | | | | [ ] OK | |
| 34 | [034/144] | | | | [ ] OK | |
| 35 | [035/144] | | | | [ ] OK | |
| 36 | [036/144] | | | | [ ] OK | |
| 37 | [037/144] | | | | [ ] OK | |
| 38 | [038/144] | | | | [ ] OK | |
| 39 | [039/144] | | | | [ ] OK | |
| 40 | [040/144] | | | | [ ] OK | |
| 41 | [041/144] | | | | [ ] OK | |
| 42 | [042/144] | | | | [ ] OK | |
| 43 | [043/144] | | | | [ ] OK | |
| 44 | [044/144] | | | | [ ] OK | |
| 45 | [045/144] | | | | [ ] OK | |
| 46 | [046/144] | | | | [ ] OK | |
| 47 | [047/144] | | | | [ ] OK | |
| 48 | [048/144] | | | | [ ] OK | |

---

## Catatan Kondisi Blok 2 (Kondisi 049–096) — Cahaya: ______________________

| No | Kondisi ID | Kipas | Pompa | Lampu | Status | Catatan Gangguan |
|:--:|:----------:|:-----:|:-----:|:-----:|:------:|:-----------------|
| 1 | [049/144] | | | | [ ] OK | |
| 2 | [050/144] | | | | [ ] OK | |
| 3 | [051/144] | | | | [ ] OK | |
| 4 | [052/144] | | | | [ ] OK | |
| 5 | [053/144] | | | | [ ] OK | |
| 6 | [054/144] | | | | [ ] OK | |
| 7 | [055/144] | | | | [ ] OK | |
| 8 | [056/144] | | | | [ ] OK | |
| 9 | [057/144] | | | | [ ] OK | |
| 10 | [058/144] | | | | [ ] OK | |
| 11 | [059/144] | | | | [ ] OK | |
| 12 | [060/144] | | | | [ ] OK | |
| 13 | [061/144] | | | | [ ] OK | |
| 14 | [062/144] | | | | [ ] OK | |
| 15 | [063/144] | | | | [ ] OK | |
| 16 | [064/144] | | | | [ ] OK | |
| 17 | [065/144] | | | | [ ] OK | |
| 18 | [066/144] | | | | [ ] OK | |
| 19 | [067/144] | | | | [ ] OK | |
| 20 | [068/144] | | | | [ ] OK | |
| 21 | [069/144] | | | | [ ] OK | |
| 22 | [070/144] | | | | [ ] OK | |
| 23 | [071/144] | | | | [ ] OK | |
| 24 | [072/144] | | | | [ ] OK | |
| 25 | [073/144] | | | | [ ] OK | |
| 26 | [074/144] | | | | [ ] OK | |
| 27 | [075/144] | | | | [ ] OK | |
| 28 | [076/144] | | | | [ ] OK | |
| 29 | [077/144] | | | | [ ] OK | |
| 30 | [078/144] | | | | [ ] OK | |
| 31 | [079/144] | | | | [ ] OK | |
| 32 | [080/144] | | | | [ ] OK | |
| 33 | [081/144] | | | | [ ] OK | |
| 34 | [082/144] | | | | [ ] OK | |
| 35 | [083/144] | | | | [ ] OK | |
| 36 | [084/144] | | | | [ ] OK | |
| 37 | [085/144] | | | | [ ] OK | |
| 38 | [086/144] | | | | [ ] OK | |
| 39 | [087/144] | | | | [ ] OK | |
| 40 | [088/144] | | | | [ ] OK | |
| 41 | [089/144] | | | | [ ] OK | |
| 42 | [090/144] | | | | [ ] OK | |
| 43 | [091/144] | | | | [ ] OK | |
| 44 | [092/144] | | | | [ ] OK | |
| 45 | [093/144] | | | | [ ] OK | |
| 46 | [094/144] | | | | [ ] OK | |
| 47 | [095/144] | | | | [ ] OK | |
| 48 | [096/144] | | | | [ ] OK | |

---

## Catatan Kondisi Blok 3 (Kondisi 097–144) — Cahaya: ______________________

| No | Kondisi ID | Kipas | Pompa | Lampu | Status | Catatan Gangguan |
|:--:|:----------:|:-----:|:-----:|:-----:|:------:|:-----------------|
| 1 | [097/144] | | | | [ ] OK | |
| 2 | [098/144] | | | | [ ] OK | |
| 3 | [099/144] | | | | [ ] OK | |
| 4 | [100/144] | | | | [ ] OK | |
| 5 | [101/144] | | | | [ ] OK | |
| 6 | [102/144] | | | | [ ] OK | |
| 7 | [103/144] | | | | [ ] OK | |
| 8 | [104/144] | | | | [ ] OK | |
| 9 | [105/144] | | | | [ ] OK | |
| 10 | [106/144] | | | | [ ] OK | |
| 11 | [107/144] | | | | [ ] OK | |
| 12 | [108/144] | | | | [ ] OK | |
| 13 | [109/144] | | | | [ ] OK | |
| 14 | [110/144] | | | | [ ] OK | |
| 15 | [111/144] | | | | [ ] OK | |
| 16 | [112/144] | | | | [ ] OK | |
| 17 | [113/144] | | | | [ ] OK | |
| 18 | [114/144] | | | | [ ] OK | |
| 19 | [115/144] | | | | [ ] OK | |
| 20 | [116/144] | | | | [ ] OK | |
| 21 | [117/144] | | | | [ ] OK | |
| 22 | [118/144] | | | | [ ] OK | |
| 23 | [119/144] | | | | [ ] OK | |
| 24 | [120/144] | | | | [ ] OK | |
| 25 | [121/144] | | | | [ ] OK | |
| 26 | [122/144] | | | | [ ] OK | |
| 27 | [123/144] | | | | [ ] OK | |
| 28 | [124/144] | | | | [ ] OK | |
| 29 | [125/144] | | | | [ ] OK | |
| 30 | [126/144] | | | | [ ] OK | |
| 31 | [127/144] | | | | [ ] OK | |
| 32 | [128/144] | | | | [ ] OK | |
| 33 | [129/144] | | | | [ ] OK | |
| 34 | [130/144] | | | | [ ] OK | |
| 35 | [131/144] | | | | [ ] OK | |
| 36 | [132/144] | | | | [ ] OK | |
| 37 | [133/144] | | | | [ ] OK | |
| 38 | [134/144] | | | | [ ] OK | |
| 39 | [135/144] | | | | [ ] OK | |
| 40 | [136/144] | | | | [ ] OK | |
| 41 | [137/144] | | | | [ ] OK | |
| 42 | [138/144] | | | | [ ] OK | |
| 43 | [139/144] | | | | [ ] OK | |
| 44 | [140/144] | | | | [ ] OK | |
| 45 | [141/144] | | | | [ ] OK | |
| 46 | [142/144] | | | | [ ] OK | |
| 47 | [143/144] | | | | [ ] OK | |
| 48 | [144/144] | | | | [ ] OK | |

---

## Pemeriksaan Mutu Data (Hari yang Sama)
Dilakukan paling lambat malam setelah slot, selagi slot cadangan (12 Nov) masih ada.

1. Terdapat **144 kondisi** (3 blok × 8 kombinasi alat × 6 ulangan).
2. Nilai **lux berbeda jelas antar-blok** cahaya ruang.
3. Satu detik pertama tiap kondisi dibuang saat pemotongan jendela (masa peralihan).
4. Tidak ada kondisi dengan tangan, badan, atau bayangan anggota di bingkai (cek kolom gangguan di atas).
5. Seluruh jendela dari satu blok cahaya berada pada lipatan yang sama (data uji dipisah per blok, **bukan per jendela**; hanya ada 3 lipatan).
6. Kelengkapan sensor: hitung baris `imu.csv` dan `daya.csv` per kondisi; IMU di bawah ±350 sampel per detik berarti ada masalah.
7. Kamera: buka beberapa citra dari awal, tengah, dan akhir sesi; periksa tidak gelap, tidak buram, bingkai tidak bergeser, dan tidak ada orang yang tidak semestinya.
8. Kesesuaian label: plot sinyal utama per kondisi (misalnya arus kipas dan pompa) dan warnai menurut label; kondisi berlabel "menyala" tetapi sinyalnya sama dengan "mati" ditandai.
9. Cocokkan lembar sesi dengan `label.csv`, lalu tulis hasilnya di `data/CATATAN-SESI.md`: sesi yang dipakai, kondisi yang dikeluarkan beserta alasannya, dan kejanggalan.
10. Putuskan sebelum pulang: apakah perlu slot cadangan 12 Nov (mis. kondisi terganggu terlalu banyak)?

## Pemeriksaan Pasca Sesi
1. Pastikan skrip menulis log terakhir bertuliskan "Selesai" dan berkas `manifest.json` terbuat.
2. Pengelola meja menyalin seluruh data ke flash disk tim dan ke cadangan meja; tim tidak menyalin sendiri dari laptop meja.
3. Kembalikan meja ke keadaan acuan (matikan alat, rapikan kabel, kembalikan air ke wadah A, kosongkan area objek, tutup pintu kotak).
4. Foto lembar sesi ini dengan kamera HP dan simpan bersama data tim.
5. Masukkan `label.csv`, berkas sensor CSV, dan `manifest.json` ke `data/`, lalu tulis `data/MANIFEST.json` berisi nama sesi dan sidik SHA-256 `label.csv`. Citra kamera yang besar tidak di-commit ke GitHub; simpan di penyimpanan tim dan catat tautannya di papan tim Workbench.

**Kondisi terganggu (isi nomor):** ______________________  
*Data tidak diulang di tempat: kondisi terganggu ditandai lalu dikeluarkan saat pemotongan jendela. Bila gangguan panjang (misalnya kabel tercabut), hentikan dengan Ctrl+C; sesi dapat dilanjutkan pada slot cadangan 12 Nov.*

**Catatan umum sesi:** ______________________________________________
