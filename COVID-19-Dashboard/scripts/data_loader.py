"""
Module de chargement des données COVID-19
Gère l'importation et l'exploration initiale des données CSV
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_covid_data(filepath, encoding='utf-8'):
    """
    Charge les données COVID-19 depuis un fichier CSV
    
    Args:
        filepath (str): Chemin vers le fichier CSV
        encoding (str): Encodage du fichier (défaut: utf-8)
    
    Returns:
        pd.DataFrame: DataFrame contenant les données chargées
    
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        pd.errors.EmptyDataError: Si le fichier est vide
    """
    print(f"🔄 Chargement du fichier : {filepath}")
    
    # Vérification de l'existence du fichier
    if not Path(filepath).exists():
        raise FileNotFoundError(f"Le fichier {filepath} n'existe pas")
    
    try:
        # Chargement du CSV avec gestion des dates
        df = pd.read_csv(
            filepath,
            encoding=encoding,
            parse_dates=['date'] if 'date' in pd.read_csv(filepath, nrows=0).columns else False,
            low_memory=False
        )
        
        print(f"✅ Chargement réussi : {len(df)} lignes, {len(df.columns)} colonnes")
        
        # Affichage des informations de base
        display_data_info(df)
        
        return df
        
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError(f"Le fichier {filepath} est vide")
    except Exception as e:
        raise Exception(f"Erreur lors du chargement : {str(e)}")


def display_data_info(df):
    """
    Affiche un résumé des informations du DataFrame
    
    Args:
        df (pd.DataFrame): DataFrame à analyser
    """
    print("\n📋 Aperçu des données :")
    print("-" * 50)
    
    # Dimensions
    print(f"   Dimensions : {df.shape[0]} lignes × {df.shape[1]} colonnes")
    
    # Types de données
    print(f"\n   Types de données :")
    type_counts = df.dtypes.value_counts()
    for dtype, count in type_counts.items():
        print(f"      - {dtype}: {count} colonnes")
    
    # Valeurs manquantes
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    cols_with_missing = missing[missing > 0].sort_values(ascending=False)
    
    if len(cols_with_missing) > 0:
        print(f"\n   ⚠️  Colonnes avec valeurs manquantes :")
        for col in cols_with_missing.head(5).index:
            pct = missing_pct[col]
            print(f"      - {col}: {missing[col]} ({pct:.1f}%)")
        if len(cols_with_missing) > 5:
            print(f"      ... et {len(cols_with_missing) - 5} autres colonnes")
    else:
        print("\n   ✅ Aucune valeur manquante détectée")
    
    # Plage de dates (si colonne date existe)
    if 'date' in df.columns:
        try:
            df['date'] = pd.to_datetime(df['date'])
            print(f"\n   📅 Plage temporelle :")
            print(f"      De {df['date'].min().date()} à {df['date'].max().date()}")
        except:
            pass
    
    # Aperçu des premières lignes
    print(f"\n   Premières lignes du dataset :")
    print(df.head(3).to_string(max_cols=6))
    print("-" * 50)


def get_column_statistics(df, column):
    """
    Calcule les statistiques descriptives pour une colonne
    
    Args:
        df (pd.DataFrame): DataFrame source
        column (str): Nom de la colonne
    
    Returns:
        dict: Dictionnaire contenant les statistiques
    """
    if column not in df.columns:
        raise ValueError(f"La colonne '{column}' n'existe pas")
    
    stats = {}
    
    if pd.api.types.is_numeric_dtype(df[column]):
        stats['count'] = df[column].count()
        stats['mean'] = df[column].mean()
        stats['median'] = df[column].median()
        stats['std'] = df[column].std()
        stats['min'] = df[column].min()
        stats['max'] = df[column].max()
        stats['missing'] = df[column].isnull().sum()
    else:
        stats['count'] = df[column].count()
        stats['unique'] = df[column].nunique()
        stats['top'] = df[column].mode()[0] if len(df[column].mode()) > 0 else None
        stats['missing'] = df[column].isnull().sum()
    
    return stats


def load_multiple_sources(filepaths):
    """
    Charge et fusionne plusieurs fichiers de données
    
    Args:
        filepaths (list): Liste des chemins vers les fichiers
    
    Returns:
        pd.DataFrame: DataFrame fusionné
    """
    dfs = []
    
    for filepath in filepaths:
        try:
            df = load_covid_data(filepath)
            dfs.append(df)
            print(f"✅ Ajouté : {filepath}")
        except Exception as e:
            print(f"⚠️  Ignoré {filepath} : {e}")
    
    if not dfs:
        raise ValueError("Aucun fichier n'a pu être chargé")
    
    # Fusion des DataFrames
    combined_df = pd.concat(dfs, ignore_index=True)
    print(f"\n✅ Fusion complétée : {len(combined_df)} lignes au total")
    
    return combined_df


# Fonction de test du module
if __name__ == "__main__":
    print("=== Test du module data_loader ===\n")
    
    # Test avec un fichier exemple
    test_file = "data/raw/covid_data.csv"
    
    try:
        df = load_covid_data(test_file)
        print("\n✅ Module data_loader testé avec succès")
    except FileNotFoundError:
        print(f"\n⚠️  Fichier de test non trouvé : {test_file}")
        print("   Créez ce fichier pour tester le module")
    except Exception as e:
        print(f"\n❌ Erreur lors du test : {e}")
