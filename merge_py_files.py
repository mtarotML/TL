import os

# --- Paramètres ---
OUTPUT_FILE = "all_text_files_merged.txt"
INCLUDE_SUBFOLDERS = True  # Mets False si tu veux ignorer les sous-dossiers
INCLUDED_EXTENSIONS = {".py", ".txt", ".md", ".html", ".js"}


def is_hidden(path):
    """Retourne True si le fichier ou dossier est caché (commence par un point)."""
    return any(part.startswith('.') for part in path.split(os.sep))


def collect_text_files(root_path, include_subfolders=True):
    text_files = []
    for root, dirs, files in os.walk(root_path):
        # On ignore les dossiers cachés
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.startswith('.'):
                continue  # Ignore fichiers cachés (.gitignore, etc.)
            ext = os.path.splitext(file)[1].lower()
            if ext in INCLUDED_EXTENSIONS:
                full_path = os.path.join(root, file)
                if not is_hidden(full_path):
                    text_files.append(full_path)
        if not include_subfolders:
            break
    return text_files


def merge_files(file_list, output_path):
    with open(output_path, "w", encoding="utf-8") as outfile:
        for path in sorted(file_list):
            outfile.write(f"\n\n# ===== Fichier : {path} =====\n\n")
            try:
                with open(path, "r", encoding="utf-8") as infile:
                    outfile.write(infile.read())
            except Exception as e:
                outfile.write(f"[Erreur de lecture : {e}]\n")


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, OUTPUT_FILE)

    all_files = collect_text_files(current_dir, INCLUDE_SUBFOLDERS)

    # On évite d'inclure le fichier de sortie lui-même
    all_files = [f for f in all_files if os.path.abspath(f) != os.path.abspath(output_path)]

    merge_files(all_files, output_path)
    print(f"✅ Fusion terminée ({len(all_files)} fichiers) → {OUTPUT_FILE}")
