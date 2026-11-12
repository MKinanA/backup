# Test Cases (Linux)

Test cases untuk backup tool ini. ***In development***.

---

## A. Database Initialization

  ### 1. Clone repositori ke local.
  Jalankan `git clone https://github.com/MKinanA/backup.git` untuk meng-clone repositori (pastikan `git` sudah terinstal sebelumnya), lalu masuk ke direktorinya menggunakan `cd backup`.

  ### 2. Pastikan database JSON belum ada.
  Periksa isi direktori dan pastikan tidak ada file `database.json`.

  ### 3. Buat virtual environment python.
  Pastikan python (`python3`) sudah terinstal terlebih dahulu. Buat virtual environment dengan menjalankan `python3 -m venv venv` dan aktifkan dengan menjalankan `source venv/bin/activate`, lalu install dependencies dengan menjalankan `pip install -r requirements.txt`.

  ### 4. Jalankan modul `backup` untuk pertama kalinya.
  Jalankan `python -m backup --help` dan periksa output help menu yang muncul.

  ### 5. Periksa lagi database JSON.
  Sekarang, periksa kembali direktori dan pastikan file `database.json` telah dibuat secara otomatis.

  Jika seluruh langkah berhasil, tes sukses.

---

## B. Backup Profile Creation

  ### 1. Tampilkan daftar profile.
  Jalankan `python -m backup list` untuk menampilkan daftar profile yang ada. Output seharusnya kosong karena belum ada profile yang dibuat.

  ### 2. Buat profile baru.
  Jalankan `python -m backup create <nama>` menggunakan nama bebas, misalnya `backup1`.

  ### 3. Tampilkan daftar profile lagi.
  Jalankan kembali `python -m backup list` dan pastikan nama profile yang baru dibuat sudah muncul.

  Jika seluruh langkah berhasil, tes sukses.

---

## C. Backup Profile Deletion

  ### 1. Pastikan profile yang akan dihapus.
  Jalankan `python -m backup list` dan pastikan ada profile untuk dicoba dihapus. Jika belum ada, lakukan tes B lagi.

  ### 2. Hapus profile yang sudah dibuat.
  Jalankan `python -m backup delete <nama>` menggunakan nama profile yang sudah dibuat sebelumnya, misalnya `backup1`.

  ### 3. Tampilkan daftar profile lagi.
  Jalankan kembali `python -m backup list` dan pastikan nama profile yang dihapus sudah tidak muncul lagi.

  Jika seluruh langkah berhasil, tes sukses.

---

## D. Lorem Ipsum