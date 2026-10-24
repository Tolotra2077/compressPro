import argparse
import bz2
import lzma
import os
import time
import zipfile


def compress_bz2(input_path, output_path=None):
    if not output_path:
        output_path = input_path + ".bz2"
    start = time.time()
    with open(input_path, "rb") as f_in, bz2.open(output_path, "wb") as f_out:
        f_out.writelines(f_in)
    duration = time.time() - start
    print(f"[BZIP2] Compressé : {output_path} ({duration:.4f}s)")
    return output_path


def decompress_bz2(input_path, output_path=None):
    if not output_path:
        output_path = input_path[:-4] if input_path.endswith(".bz2") else input_path + ".out"
    with bz2.open(input_path, "rb") as f_in, open(output_path, "wb") as f_out:
        f_out.writelines(f_in)
    print(f"[BZIP2] Décompressé : {output_path}")


def compress_lzma(input_path, output_path=None):
    if not output_path:
        output_path = input_path + ".xz"
    start = time.time()
    with open(input_path, "rb") as f_in, lzma.open(output_path, "wb") as f_out:
        f_out.writelines(f_in)
    duration = time.time() - start
    print(f"[LZMA] Compressé : {output_path} ({duration:.4f}s)")
    return output_path


def decompress_lzma(input_path, output_path=None):
    if not output_path:
        output_path = input_path[:-3] if input_path.endswith(".xz") else input_path + ".out"
    with lzma.open(input_path, "rb") as f_in, open(output_path, "wb") as f_out:
        f_out.writelines(f_in)
    print(f"[LZMA] Décompressé : {output_path}")


def compress_zip7(input_path, output_path=None):
    # Utilisation du format Zip (similaire aux standards de compression de 7-Zip avec la compression Deflate/LZMA)
    if not output_path:
        output_path = input_path + ".zip"
    start = time.time()
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(input_path, os.path.basename(input_path))
    duration = time.time() - start
    print(f"[7-ZIP/ZIP] Compressé : {output_path} ({duration:.4f}s)")
    return output_path


def run_benchmark(files):
    print("\n" + "="*50)
    print("      RAPPORT DE BENCHMARK (EFFICACITÉ)")
    print("="*50)
    
    for file_path in files:
        if not os.path.exists(file_path):
            print(f"\n[Attention] Fichier introuvable : {file_path}")
            continue
            
        orig_size = os.path.getsize(file_path)
        print(f"\nFichier analysé : {file_path}")
        print(f"Taille originale : {orig_size / 1024:.2f} Ko")
        
        # Test Bzip2
        out_bz2 = compress_bz2(file_path)
        size_bz2 = os.path.getsize(out_bz2)
        ratio_bz2 = (1 - size_bz2 / orig_size) * 100
        print(f" -> Bzip2 -> Taille : {size_bz2 / 1024:.2f} Ko | Réduction : {ratio_bz2:.2f}%")
        
        # Test LZMA
        out_lzma = compress_lzma(file_path)
        size_lzma = os.path.getsize(out_lzma)
        ratio_lzma = (1 - size_lzma / orig_size) * 100
        print(f" -> LZMA  -> Taille : {size_lzma / 1024:.2f} Ko | Réduction : {ratio_lzma:.2f}%")
        
        # Test 7-Zip / ZIP
        out_zip = compress_zip7(file_path)
        size_zip = os.path.getsize(out_zip)
        ratio_zip = (1 - size_zip / orig_size) * 100
        print(f" -> 7-Zip -> Taille : {size_zip / 1024:.2f} Ko | Réduction : {ratio_zip:.2f}%")
        print("-" * 50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Outil de compression")
    subparsers = parser.add_subparsers(dest="command", help="Commande à exécuter")

    # Commandes individuelles
    for algo in ["bz2", "lzma", "zip7"]:
        p_comp = subparsers.add_parser(f"compress-{algo}", help=f"Compresser avec {algo}")
        p_comp.add_argument("file", help="Fichier cible")

    # Commande Benchmark pour le PDF
    p_bench = subparsers.add_parser("benchmark", help="Lancer le benchmark sur les 4 types de fichiers")
    p_bench.add_argument("files", nargs="+", help="Liste des 4 fichiers (texte, audio, image, vidéo)")

    args = parser.parse_args()

    if args.command == "compress-bz2":
        compress_bz2(args.file)
    elif args.command == "compress-lzma":
        compress_lzma(args.file)
    elif args.command == "compress-zip7":
        compress_zip7(args.file)
    elif args.command == "benchmark":
        run_benchmark(args.files)
    else:
        parser.print_help()