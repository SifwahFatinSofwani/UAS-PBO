import sys
import subprocess
import importlib
import os

def pastikan_terinstal(package_name, import_name=None):
    if import_name is None:
        import_name = package_name
    try:
        importlib.import_module(import_name)
    except ImportError:
        print(f"[SYSTEM] Modul '{package_name}' tidak ditemukan. Menginstal otomatis...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name, "--quiet"])
        print(f"[SYSTEM] Selesai menginstal '{package_name}'.")

pastikan_terinstal("pandas")
pastikan_terinstal("matplotlib", "matplotlib.pyplot")
pastikan_terinstal("seaborn")

import pandas as pd
import models
import repositories
import preprocessing
import analisis

DataTidakDitemukanError = models.DataTidakDitemukanError
FormatDataTidakValidError = models.FormatDataTidakValidError

PreprocessingPipeline = preprocessing.PreprocessingPipeline
ColumnStandardizer = preprocessing.ColumnStandardizer
MissingValueHandler = preprocessing.MissingValueHandler
DuplicateRowRemover = preprocessing.DuplicateRowRemover
EmployeeRecordConverter = preprocessing.EmployeeRecordConverter

JSONRepository = repositories.JSONRepository
CSVRepository = repositories.CSVRepository

AnalysisFactory = analisis.AnalysisFactory
AnalysisRunner = analisis.AnalysisRunner
AbstractAnalysis = analisis.AbstractAnalysis
VisualizableMixin = analisis.VisualizableMixin
ConsoleLogger = analisis.ConsoleLogger

def setup_directories():
    os.makedirs("output_visualisasi", exist_ok=True)
    os.makedirs("output_laporan", exist_ok=True)

def pause_and_clear():
    input("\nTekan Enter untuk melanjutkan...")
    os.system('cls' if os.name == 'nt' else 'clear')

def run_tests(df_clean, repo_list):
    print("\n=== MENJALANKAN PENGUJIAN ERROR & PRINSIP SOLID ===")
    
    print("\n[TEST 1] Demo LSP: Subclass mengembalikan DataFrame")
    lsp_candidates = ["distribusi", "ringkasan", "usia"]
    for name in lsp_candidates:
        obj = AnalysisFactory.create_analysis(name)  
        result = obj.run_analysis(df_clean)
        assert isinstance(result, pd.DataFrame), f"{name} melanggar LSP!"
        print(f"  {obj.title} -> {result.shape} - LSP OK\n")

    print("\n[TEST 2] Demo ISP: SummaryStatisticsAnalysis tidak memiliki visualize")
    assert not hasattr(AnalysisFactory.create_analysis("ringkasan"), "visualize")
    print("  ISP terbukti: kelas ringkasan murni untuk terminal/report.\n")

    print("\n[TEST 3] Pengujian Error Setter Deskripsi (FormatDataTidakValidError)")
    obj = AnalysisFactory.create_analysis("stres")
    try:
        obj.description = ""
    except FormatDataTidakValidError as e:
        print(f"  Error berhasil ditangkap: {e}\n")

    print("\n[TEST 4] Pengujian Error Validasi AnalysisRunner")
    runner = AnalysisRunner(AnalysisFactory.create_analysis("distribusi"), repo_list)
    try:
        runner.analysis = "bukan_objek"
    except FormatDataTidakValidError as e:
        print(f"  Error berhasil ditangkap: {e}\n")
        
    print("\n[TEST 5] Pengujian Error Key Analisis Tidak Ditemukan")
    try:
        AnalysisFactory.create_analysis("key_acak_tidak_valid")
    except FormatDataTidakValidError as e:
        print(f"  Error berhasil ditangkap: {e}\n")

    print("\n[TEST 6] Pengujian Error Validasi Model Data")
    try:
        models.EmployeeRecord(
            employee_id="ERR01", work_location="Remote", stress_level="Extreme",
            mental_health="Good", social_isolation="Low", physical_activity="High",
            age=-5, gender="Male", hours_worked=-10, resource_access="Yes", sleep_quality="Good"
        )
    except FormatDataTidakValidError as e:
        print(f"  Error data tidak valid berhasil ditangkap: {e}\n")

    print("\n=== PENGUJIAN SELESAI ===")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    setup_directories()
    
    print("============================================================")
    print("Sistem Analisis Digital (SiDigital) - Kesehatan Mental Karyawan")
    print("============================================================")
    
    try:
        raw_df = pd.read_csv("Impact_of_Remote_Work_on_Mental_Health.csv")
    except Exception as e:
        print(f"[ERROR] Gagal memuat data: {e}")
        return

    print("\n--- Memulai Preprocessing Pipeline ---")
    pipeline = PreprocessingPipeline()
    pipeline.add_step(ColumnStandardizer())
    pipeline.add_step(MissingValueHandler())
    pipeline.add_step(DuplicateRowRemover())      
    pipeline.add_step(EmployeeRecordConverter())  
    
    try:
        df_clean = pipeline.execute(raw_df)
        print(f"\nPipeline selesai. Baris siap dianalisis : {df_clean.shape[0]}\n")
        pause_and_clear()
    except Exception as e:
        print(f"[ERROR] Pipeline gagal: {e}")
        return

    repo_list = [JSONRepository(), CSVRepository()]
    logger = ConsoleLogger()
    
    menu_items = [
        ("distribusi", "Distribusi Mental Health"),
        ("lokasi", "Kondisi Mental berdasarkan Lokasi Kerja"),
        ("stres", "Korelasi Tingkat Stres dan Kondisi Mental"),
        ("usia", "Kondisi Mental berdasarkan Kelompok Usia"),
        ("jam_kerja", "Pengaruh Jam Kerja terhadap Kondisi Mental"),
        ("tabel_statistik", "Tabel Visual Statistik Numerik")
    ]

    total_menu = len(menu_items)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("============================================================")
        print("               MENU UTAMA ANALISIS DATA                     ")
        print("============================================================")
        print("1. Visualisasi")
        print("2. Report")
        print("3. Run all test")
        print("0. Exit")
        print("============================================================")
        
        pilihan = input("Masukkan pilihan Anda (0-3): ").strip()
        
        if pilihan == '1':
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("--- Menu Visualisasi ---")
                for i, (key, label) in enumerate(menu_items, 1):
                    print(f"{i}. {label}")
                print("0. Kembali")
                
                sub = input(f"\nPilih visualisasi (0-{total_menu}): ").strip()
                if sub == '0':
                    break
                elif sub.isdigit() and 1 <= int(sub) <= total_menu:
                    key = menu_items[int(sub)-1][0]
                    try:
                        analisis_obj = AnalysisFactory.create_analysis(key)
                        hasil = analisis_obj.run_analysis(df_clean)
                        if isinstance(analisis_obj, VisualizableMixin):
                            analisis_obj.visualize(hasil)
                            pause_and_clear()
                        else:
                            print(f"\n{key} tidak mendukung visualisasi.\n")
                            pause_and_clear()
                    except Exception as e:
                        print(f"[ERROR] Gagal visualisasi: {e}")
                        pause_and_clear()
                else:
                    print("[WARNING] Pilihan tidak valid.")
                    pause_and_clear()
                    
        elif pilihan == '2':
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("--- Menu Report ---")
                for i, (key, label) in enumerate(menu_items, 1):
                    print(f"{i}. {label}")
                print("0. Kembali")
                
                sub = input(f"\nPilih report (0-{total_menu}): ").strip()
                if sub == '0':
                    break
                elif sub.isdigit() and 1 <= int(sub) <= total_menu:
                    key = menu_items[int(sub)-1][0]
                    try:
                        analisis_obj = AnalysisFactory.create_analysis(key)
                        runner = AnalysisRunner(analisis_obj, repositories=repo_list, logger=logger)
                        
                        save_path = os.path.join("output_laporan", f"hasil_{key}")
                        hasil = runner.run_and_save(df_clean, save_path)
                        
                        print("\n[REPORT PREVIEW]")
                        print(hasil.to_string())
                        pause_and_clear()
                    except Exception as e:
                        print(f"[ERROR] Gagal generate report: {e}")
                        pause_and_clear()
                else:
                    print("[WARNING] Pilihan tidak valid.")
                    pause_and_clear()
                    
        elif pilihan == '3':
            run_tests(df_clean, repo_list)
            pause_and_clear()
                    
        elif pilihan == '0':
            print("\nSelesai Eksekusi.")
            break
            
        else:
            print("[WARNING] Pilihan tidak valid.")

if __name__ == "__main__":
    main()