# 🧠 Pipeline Analisis Data: Remote Work Mental Health

Proyek ini merupakan implementasi pipeline analisis data menggunakan **Python** dengan pendekatan **Pemrograman Berorientasi Objek (OOP)** murni. Desain arsitektur kode dibangun secara modular dengan mematuhi prinsip **SOLID** dan *Design Patterns* seperti Factory dan Decorator untuk memastikan kode mudah dirawat, diuji, dan dikembangkan.

---

## 🚀 Penerapan Konsep OOP

### 1. Enkapsulasi (Encapsulation)
- **`@dataclass` & Validasi:** Objek `EmployeeRecord` membungkus data tiap baris secara aman menggunakan properti `frozen=True` (immutable). Validasi integritas data ditempatkan di dalam `__post_init__` untuk mencegah atribut kritis seperti usia dan jam kerja bernilai negatif.
- **Getter/Setter via `@property`:** Atribut internal `_description` pada kelas `BaseAnalysis` dilindungi agar tidak dapat diubah secara langsung dari luar. Perubahan nilai wajib melalui setter properti yang dilengkapi logika penanganan string kosong. Atribut analisis aktif pada `AnalysisRunner` juga diproteksi dengan mekanisme serupa.

### 2. Abstraksi (Abstraction)
- Kerangka kerja sistem didefinisikan menggunakan **Abstract Base Class (ABC)** melalui kelas `PersistenceRepository`, `PreprocessingStep`, `AbstractAnalysis`, dan `AnalysisLogger`. Kelas-kelas abstrak ini menetapkan kontrak antarmuka yang wajib dipenuhi oleh setiap subclass.
- **Mixin Pattern:** Kelas `VisualizableMixin` berperan sebagai komponen abstraksi khusus yang memisahkan fungsionalitas rendering grafik dari logika pemrosesan data inti.

### 3. Pewarisan (Inheritance)
- **Layer Penyimpanan:** Kelas `JSONRepository` dan `CSVRepository` mewarisi struktur dari `PersistenceRepository` untuk mengimplementasikan mekanisme penulisan format file yang spesifik.
- **Layer Analisis:** Seluruh modul analisis konkret diturunkan dari kelas induk `BaseAnalysis` untuk mewarisi fitur dasar pengolahan deskripsi dan ringkasan sistem.
- **Layer Logging:** Kelas `ConsoleLogger` memperluas abstraksi `AnalysisLogger` untuk menangani keluaran informasi ke terminal.

### 4. Polimorfisme (Polymorphism)
- **Method Overriding:** Setiap subclass analisis melakukan override terhadap method `run_analysis()` untuk menerapkan algoritma manipulasi DataFrame yang berbeda-beda sesuai tujuan spesifiknya. Kelas yang mengimplementasikan `VisualizableMixin` juga melakukan override pada method `visualize()`.
- **Interface Implementation:** Kelas runtime seperti `AnalysisRunner` memanfaatkan polimorfisme untuk mengeksekusi analisis dan menyimpan data tanpa perlu mengetahui tipe spesifik dari objek repositori atau modul analisis yang sedang berjalan, selama objek tersebut mematuhi kontrak antarmuka tipe induknya.

---

## 🏗️ Struktur dan Daftar Kelas

### 📦 Layer Model Data
* `EmployeeRecord`: Representasi data tunggal. Menggunakan fitur `slots=True` untuk optimasi alokasi memori objek.

### 💾 Layer Repositori (Persistence)
* `PersistenceRepository` *(Abstract)*: Kontrak dasar mekanisme penyimpanan dan pemuatan data.
* `JSONRepository` & `CSVRepository`: Implementasi konkret penyimpanan data ke format `.json` dan `.csv`.

### ⚙️ Layer Preprocessing
* `PreprocessingPipeline`: Kelas manajer yang mengatur dan mengeksekusi tahapan transformasi data secara berantai (*pipeline*).
* `PreprocessingStep` *(Abstract)*: Standar langkah pembersihan data.
* **Langkah Konkret:**
  * `ColumnStandardizer`: Menyeragamkan format penamaan kolom menjadi huruf kecil.
  * `MissingValueHandler`: Melakukan imputasi nilai kosong pada data kategorikal dan numerik.
  * `DuplicateRowRemover`: Mendeteksi dan menghapus baris data yang ganda.
  * `EmployeeRecordConverter`: Mengonversi DataFrame ke array objek `EmployeeRecord` untuk proses validasi aturan bisnis, lalu mengembalikannya kembali menjadi DataFrame bersih.

### 📊 Layer Analisis & Visualisasi
* `AbstractAnalysis` *(Abstract)* & `BaseAnalysis`: Fondasi utama seluruh modul analisis data.
* `VisualizableMixin` *(Abstract)*: Antarmuka opsional untuk kelas yang membutuhkan kemampuan visualisasi grafik.
* **6 Modul Analisis Aktif pada Sistem:**
  1. `MentalHealthDistribution`: Menghitung dan memvisualisasikan grafik batang distribusi frekuensi kondisi mental karyawan.
  2. `MentalHealthByLocation`: Menganalisis dan menampilkan diagram batang kondisi mental berdasarkan lokasi kerja (*Remote*, *Hybrid*, *Onsite*).
  3. `MentalHealthByStressHeatmap`: Membuat matriks tabulasi silang antara tingkat stres dan kondisi mental dalam bentuk heatmap.
  4. `MentalHealthByAgeGroup`: Mengelompokkan karyawan ke dalam klaster usia tertentu untuk melihat tren kondisi mentalnya.
  5. `MentalHealthByWorkingHours`: Menghitung rata-rata jam kerja mingguan karyawan dan menyajikannya dalam grafik batang beranotasi nilai.
  6. `DescriptiveStatsTable`: Menghitung parameter statistik deskriptif numerik dan merendernya ke dalam bentuk visual tabel grafis.

### 🏭 Layer Core & Eksekusi
* `AnalysisFactory`: Mengimplementasikan *Factory Pattern* untuk membuat objek analisis secara dinamis melalui *registry table*.
* `AnalysisLogger` *(Abstract)* & `ConsoleLogger`: Komponen pencatatan log eksekusi sistem.
* `AnalysisRunner`: Pengendali utama (*coordinator*) yang menghubungkan modul analisis dengan layer penyimpanan untuk memproses dan mengekspor laporan.

---

## 💎 Kepatuhan pada Prinsip SOLID

* **Single Responsibility Principle (SRP):** Setiap kelas berfokus pada satu tanggung jawab tunggal. Kelas `DuplicateRowRemover` hanya bertanggung jawab membuang baris duplikat tanpa mencampuri urusan konversi tipe data atau validasi objek.
* **Open/Closed Principle (OCP):** Arsitektur sistem menggunakan fungsi dekorator `@register_analysis(name)`. Menambahkan jenis analisis baru dapat dilakukan cukup dengan membuat kelas baru di bawah dekorator tersebut tanpa perlu memodifikasi kode internal pada kelas `AnalysisFactory`.
* **Liskov Substitution Principle (LSP):** Seluruh subclass yang diturunkan dari `BaseAnalysis` dijamin dapat saling menggantikan ketika dieksekusi oleh runtime melalui metode `run_analysis()` dengan konsistensi pengembalian objek berupa `pd.DataFrame`.
* **Interface Segregation Principle (ISP):** Pemisahan kemampuan rendering grafik ke dalam `VisualizableMixin` memastikan kelas analisis murni tekstual (seperti `SummaryStatisticsAnalysis`) tidak dipaksa untuk mengimplementasikan metode `visualize()` yang tidak diperlukannya.
* **Dependency Inversion Principle (DIP):** Kelas tingkat tinggi seperti `AnalysisRunner` tidak bergantung secara langsung pada kelas tingkat rendah seperti `CSVRepository` atau `JSONRepository`. Kelas tersebut bergantung sepenuhnya pada abstraksi berupa antarmuka `PersistenceRepository` dan `AbstractAnalysis`.

---

## 🛠️ Penggunaan
Jalankan file eksekusi utama sistem:
```bash
python main.py
