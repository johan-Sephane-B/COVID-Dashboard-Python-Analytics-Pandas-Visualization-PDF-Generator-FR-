"""
Utilitaire de Gestion des Fichiers
Gère les problèmes de permissions et de verrouillage
"""

import os
import time
import shutil
from pathlib import Path


def safe_read_file(file_path, max_retries=3, retry_delay=1):
    """
    Lit un fichier de manière sécurisée avec gestion des erreurs
    
    Args:
        file_path (str): Chemin du fichier
        max_retries (int): Nombre maximum de tentatives
        retry_delay (int): Délai entre les tentatives (secondes)
    
    Returns:
        bytes: Contenu du fichier ou None si échec
    """
    for attempt in range(max_retries):
        try:
            with open(file_path, 'rb') as f:
                return f.read()
        except PermissionError:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            else:
                return None
        except Exception as e:
            print(f"Erreur lors de la lecture de {file_path}: {e}")
            return None
    
    return None


def is_file_locked(file_path):
    """
    Vérifie si un fichier est verrouillé
    
    Args:
        file_path (str): Chemin du fichier
    
    Returns:
        bool: True si verrouillé, False sinon
    """
    try:
        # Essayer d'ouvrir en mode exclusif
        with open(file_path, 'r+b') as f:
            return False
    except PermissionError:
        return True
    except Exception:
        return True


def safe_delete_file(file_path, max_retries=3, retry_delay=1):
    """
    Supprime un fichier de manière sécurisée
    
    Args:
        file_path (str): Chemin du fichier
        max_retries (int): Nombre maximum de tentatives
        retry_delay (int): Délai entre les tentatives
    
    Returns:
        bool: True si succès, False sinon
    """
    for attempt in range(max_retries):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        except PermissionError:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            else:
                return False
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            return False
    
    return False


def safe_write_file(file_path, data, mode='wb'):
    """
    Écrit dans un fichier de manière sécurisée
    
    Args:
        file_path (str): Chemin du fichier
        data: Données à écrire
        mode (str): Mode d'ouverture
    
    Returns:
        bool: True si succès, False sinon
    """
    try:
        # Créer le répertoire si nécessaire
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Écrire dans un fichier temporaire d'abord
        temp_path = f"{file_path}.tmp"
        
        with open(temp_path, mode) as f:
            f.write(data)
        
        # Déplacer le fichier temporaire vers la destination
        if os.path.exists(file_path):
            safe_delete_file(file_path)
        
        shutil.move(temp_path, file_path)
        return True
        
    except Exception as e:
        print(f"Erreur lors de l'écriture: {e}")
        # Nettoyer le fichier temporaire
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
        return False


def get_unique_filename(file_path):
    """
    Génère un nom de fichier unique si le fichier existe déjà
    
    Args:
        file_path (str): Chemin du fichier
    
    Returns:
        str: Nouveau chemin avec un suffixe unique
    """
    if not os.path.exists(file_path):
        return file_path
    
    path = Path(file_path)
    base = path.stem
    ext = path.suffix
    directory = path.parent
    
    counter = 1
    while True:
        new_path = directory / f"{base}_{counter}{ext}"
        if not os.path.exists(new_path):
            return str(new_path)
        counter += 1


def cleanup_old_files(directory, pattern='*.pdf', max_age_days=30, max_count=50):
    """
    Nettoie les vieux fichiers
    
    Args:
        directory (str): Répertoire à nettoyer
        pattern (str): Pattern des fichiers (ex: *.pdf)
        max_age_days (int): Age maximum en jours
        max_count (int): Nombre maximum de fichiers à garder
    
    Returns:
        int: Nombre de fichiers supprimés
    """
    if not os.path.exists(directory):
        return 0
    
    directory = Path(directory)
    files = list(directory.glob(pattern))
    
    # Trier par date de modification (plus récent en premier)
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    deleted = 0
    current_time = time.time()
    max_age_seconds = max_age_days * 24 * 3600
    
    for i, file_path in enumerate(files):
        # Garder les max_count plus récents
        if i < max_count:
            # Mais supprimer si trop vieux
            file_age = current_time - file_path.stat().st_mtime
            if file_age > max_age_seconds:
                if safe_delete_file(str(file_path)):
                    deleted += 1
        else:
            # Supprimer les fichiers au-delà de max_count
            if safe_delete_file(str(file_path)):
                deleted += 1
    
    return deleted


def get_file_info(file_path):
    """
    Récupère les informations sur un fichier
    
    Args:
        file_path (str): Chemin du fichier
    
    Returns:
        dict: Informations sur le fichier
    """
    try:
        if not os.path.exists(file_path):
            return None
        
        stat = os.stat(file_path)
        
        return {
            'path': file_path,
            'name': os.path.basename(file_path),
            'size': stat.st_size,
            'size_kb': stat.st_size / 1024,
            'size_mb': stat.st_size / (1024 * 1024),
            'created': time.ctime(stat.st_ctime),
            'modified': time.ctime(stat.st_mtime),
            'is_locked': is_file_locked(file_path),
            'extension': os.path.splitext(file_path)[1]
        }
    except Exception as e:
        return {'error': str(e)}


def open_file_location(file_path):
    """
    Ouvre l'emplacement du fichier dans l'explorateur
    
    Args:
        file_path (str): Chemin du fichier
    
    Returns:
        bool: True si succès
    """
    try:
        import platform
        directory = os.path.dirname(os.path.abspath(file_path))
        
        if platform.system() == "Windows":
            os.startfile(directory)
        elif platform.system() == "Darwin":  # macOS
            os.system(f'open "{directory}"')
        else:  # Linux
            os.system(f'xdg-open "{directory}"')
        
        return True
    except Exception as e:
        print(f"Erreur lors de l'ouverture: {e}")
        return False


def create_backup(file_path, backup_dir=None):
    """
    Crée une sauvegarde d'un fichier
    
    Args:
        file_path (str): Fichier à sauvegarder
        backup_dir (str): Répertoire de sauvegarde (optionnel)
    
    Returns:
        str: Chemin du fichier de sauvegarde ou None
    """
    try:
        if not os.path.exists(file_path):
            return None
        
        # Définir le répertoire de sauvegarde
        if backup_dir is None:
            backup_dir = os.path.join(os.path.dirname(file_path), 'backups')
        
        os.makedirs(backup_dir, exist_ok=True)
        
        # Nom du fichier de sauvegarde avec timestamp
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        base_name = os.path.basename(file_path)
        backup_name = f"{os.path.splitext(base_name)[0]}_{timestamp}{os.path.splitext(base_name)[1]}"
        backup_path = os.path.join(backup_dir, backup_name)
        
        # Copier le fichier
        shutil.copy2(file_path, backup_path)
        
        return backup_path
    except Exception as e:
        print(f"Erreur lors de la sauvegarde: {e}")
        return None


# Exemple d'utilisation
if __name__ == "__main__":
    # Test des fonctions
    test_file = "test.txt"
    
    # Écrire
    print("Test d'écriture...")
    if safe_write_file(test_file, b"Test data", mode='wb'):
        print("✅ Écriture réussie")
    
    # Lire
    print("\nTest de lecture...")
    data = safe_read_file(test_file)
    if data:
        print(f"✅ Lecture réussie: {data}")
    
    # Infos
    print("\nInformations sur le fichier:")
    info = get_file_info(test_file)
    if info:
        for key, value in info.items():
            print(f"  {key}: {value}")
    
    # Nettoyer
    print("\nNettoyage...")
    if safe_delete_file(test_file):
        print("✅ Fichier supprimé")
    
    print("\n✅ Tests terminés")