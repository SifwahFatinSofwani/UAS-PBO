# 🧠 Pipeline Analisis Data: Remote Work Mental Health

Proyek ini merupakan implementasi pipeline analisis data menggunakan **Python** dengan pendekatan **Pemrograman Berorientasi Objek (OOP)** murni. Desain arsitektur kode dibangun secara modular dengan mematuhi prinsip **SOLID** dan *Design Patterns* seperti Factory dan Decorator, memastikan kode mudah di-maintain, diuji, dan dikembangkan.

---

## 🚀 Penerapan Konsep OOP

Kode ini tidak hanya memproses data secara prosedural, tetapi menerapkan pilar utama OOP secara terstruktur:

### 1. Enkapsulasi (Encapsulation)
- **`@dataclass` & Validasi:** Data tiap baris dibungkus dalam objek `EmployeeRecord` (bersifat `frozen=True`). Validasi ketat dilakukan secara otomatis di dalam `__post_init__` (misal: memastikan atribut usia dan jam kerja tidak memiliki nilai negatif).
- **Getter/Setter dengan `@property`:** Kelas `BaseAnalysis` melindungi atribut `_description` (sebagai atribut *protected*) agar tidak bisa diubah sembarangan. Perubahan hanya bisa dilakukan melalui setter yang dilengkapi logika validasi string kosong. Kelas `AnalysisRunner` juga memproteksi atribut analisis aktifnya.

### 2. Abstraksi (Abstraction)
- Sistem menggunakan **Abstract Base Class (ABC)** pada `PersistenceRepository`, `PreprocessingStep`, dan `AbstractAnalysis`. Kelas-kelas ini bertindak sebagai kontrak antarmuka wajib yang harus dipatuhi oleh setiap subclass-nya, menyembunyikan kompleksitas dari pengguna kelas (client).
- **Mixin Pattern:** Terdapat kelas `VisualizableMixin` yang menyediakan abstraksi khusus untuk fungsionalitas visualisasi grafik. 

### 3. Pewarisan (Inheritance)
- Pada layer penyimpanan, kelas `JSONRepository` dan `CSVRepository` mewarisi dan merealisasikan kerangka dari `PersistenceRepository`.
- Pada layer analisis, semua modul analisis spesifik (seperti `MentalHealthDistribution`) mewarisi fungsionalitas dasar seperti pemanggilan deskripsi dari `BaseAnalysis`. Kelas `MentalHealthByAgeGroup` mendemonstrasikan pewarisan yang lebih kompleks dengan menambahkan atribut inisialisasi kustom (`bins`).

### 4. Polimorfisme (Polymorphism)
- **Method Overriding:** Setiap subclass analisis wajib memberikan implementasi algoritmanya sendiri pada method `run_analysis()` untuk mengolah DataFrame secara berbeda.
- **Duck Typing:** Sistem (dalam hal ini `AnalysisRunner`) dapat mengeksekusi analisis apa pun dan memanggil method `run_analysis()` asalkan objek tersebut mematuhi antarmuka `AbstractAnalysis`, tanpa perlu mengetahui tipe kelas aslinya.

---

## 🏗️ Struktur dan Daftar Kelas

Sistem ini dibagi ke dalam beberapa lapisan tanggung jawab (*Separation of Concerns*):

### 📦 Layer Model Data
* `EmployeeRecord`: Representasi data tunggal. Menggunakan fitur modern `slots=True` untuk efisiensi alokasi memori.

### 💾 Layer Repositori (Persistence)
* `PersistenceRepository` *(Abstract)*: Kontrak dasar mekanisme penyimpanan dan pemuatan data.
* `JSONRepository` & `CSVRepository`: Implementasi format spesifik repositori.

### ⚙️ Layer Preprocessing
* `PreprocessingPipeline`: Manajer utama yang mengeksekusi tahapan pembersihan data secara berantai.
* `PreprocessingStep` *(Abstract)*: Standar langkah pembersihan.
* **Langkah Konkret:** * `MissingValueHandler` (Imputasi nilai kosong).
  * `ColumnStandardizer` (Standardisasi nama kolom).
  * `DuplicateRowRemover` (Pembersihan duplikasi).
  * `EmployeeRecordConverter` (Konversi DataFrame ke array objek untuk validasi, lalu dikembalikan menjadi DataFrame).

### 📊 Layer Analisis & Visualisasi
* `AbstractAnalysis` *(Abstract)* & `BaseAnalysis`: Induk modul analisis.
* `VisualizableMixin` *(Abstract)*: Komponen opsional penambah fitur visualisasi.
* **Kelas Analisis Konkret dengan Visualisasi:**
  * `MentalHealthDistribution`
  * `MentalHealthByLocation`
  * `MentalHealthByStressHeatmap`
  * `MentalHealthByIsolationBoxplot`
  * `MentalHealthByPhysicalActivity`
  * `MentalHealthByAgeGroup`
  * `MentalHealthByGender`
  * `MentalHealthByWorkingHours`
  * `MentalHealthByResourcesAccess`
  * `MentalHealthBySleepQuality`
* **Kelas Analisis Tanpa Visualisasi:**
  * `SummaryStatisticsAnalysis` (Hanya menghasilkan tabel ringkasan).

### 🏭 Layer Core & Eksekusi
* `AnalysisFactory`: Pembuat objek dinamis (*Factory Pattern*).
* `AnalysisRunner`: Eksekutor utama yang menghubungkan objek analisis dengan repositori persisten.

---

## 💎 Kepatuhan pada Prinsip SOLID

* **Single Responsibility Principle (SRP):** Tiap kelas memiliki satu tanggung jawab mutlak. Contohnya `DuplicateRowRemover` hanya menangani baris ganda tanpa memedulikan logika imputasi atau format kolom.
* **Open/Closed Principle (OCP):** Menggunakan fitur *decorator* `@register_analysis("nama")`. Menambah jenis analisis baru cukup dengan membuat kelas baru di bawah decorator tersebut tanpa menyentuh kode inti di dalam `AnalysisFactory`.
* **Liskov Substitution Principle (LSP):** Script eksekusi membuktikan bahwa seluruh subclass `BaseAnalysis` dapat saling ditukar dan digunakan melalui tipe induknya tanpa memicu error atau mematahkan ekspektasi pengembalian tipe (`pd.DataFrame`).
* **Interface Segregation Principle (ISP):** Dipisahkannya antarmuka visualisasi ke dalam `VisualizableMixin` memastikan bahwa kelas yang hanya perlu mengeluarkan teks tabel (`SummaryStatisticsAnalysis`) tidak diwajibkan menyertakan method `visualize()`.
* **Dependency Inversion Principle (DIP):** Modul tingkat tinggi seperti `AnalysisRunner` menerima parameter berbasis abstraksi (`AbstractAnalysis` dan List dari `PersistenceRepository`), sehingga sama sekali tidak bergantung pada implementasi kelas tingkat rendahnya.

---

## 🛠️ Penggunaan
Cukup muat dataset mentah (`.csv`), lalu masukkan ke dalam objek `PreprocessingPipeline`. Setelah data bersih, analisis dapat dikontrol dengan memanggil *identifier* string spesifik pada `AnalysisFactory`, dan diserahkan ke `AnalysisRunner` untuk diekspor secara otomatis.
