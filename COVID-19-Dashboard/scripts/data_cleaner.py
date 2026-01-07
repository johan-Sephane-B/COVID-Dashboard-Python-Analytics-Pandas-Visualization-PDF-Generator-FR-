"""
Module de nettoyage des données COVID-19
Gère le traitement des valeurs manquantes, des doublons et des incohérences
"""

import pandas as pd
import numpy as np
from datetime import datetime


def clean_data(df):
    """
    Nettoie le DataFrame COVID-19
    
    Args:
        df (pd.DataFrame): DataFrame brut à nettoyer
    
    Returns:
        pd.DataFrame: DataFrame nettoyé
    """
    print("🧹 Démarrage du nettoyage des données...")
    df_clean = df.copy()
    
    # Rapport initial
    initial_rows = len(df_clean)
    print(f"   Lignes initiales : {initial_rows}")
    
    # Étape 1 : Suppression des doublons
    df_clean = remove_duplicates(df_clean)
    
    # Étape 2 : Traitement des valeurs manquantes
    df_clean = handle_missing_values(df_clean)
    
    # Étape 3 : Correction des types de données
    df_clean = fix_data_types(df_clean)
    
    # Étape 4 : Validation des valeurs
    df_clean = validate_values(df_clean)
    
    # Étape 5 : Tri des données
    df_clean = sort_data(df_clean)
    
    # Rapport final
    final_rows = len(df_clean)
    rows_removed = initial_rows - final_rows
    pct_removed = (rows_removed / initial_rows) * 100 if initial_rows != 0 else 0
    
    print(f"\n✅ Nettoyage terminé :")
    print(f"   Lignes finales : {final_rows}")
    print(f"   Lignes supprimées : {rows_removed} ({pct_removed:.1f}%)")
    
    return df_clean


def remove_duplicates(df):
    """
    Supprime les lignes dupliquées
    
    Args:
        df (pd.DataFrame): DataFrame à traiter
    
    Returns:
        pd.DataFrame: DataFrame sans doublons
    """
    initial_count = len(df)
    df_dedup = df.drop_duplicates()
    duplicates_removed = initial_count - len(df_dedup)
    
    if duplicates_removed > 0:
        print(f"   ✓ Doublons supprimés : {duplicates_removed}")
    else:
        print("   ✓ Aucun doublon détecté")
    
    return df_dedup


def handle_missing_values(df):
    """
    Gère les valeurs manquantes avec différentes stratégies
    
    Args:
        df (pd.DataFrame): DataFrame à traiter
    
    Returns:
        pd.DataFrame: DataFrame avec valeurs manquantes traitées
    """
    print("\n   📊 Traitement des valeurs manquantes :")
    df_filled = df.copy()
    
    # Analyse des valeurs manquantes
    missing_before = df_filled.isnull().sum().sum()
    
    for column in df_filled.columns:
        missing_count = df_filled[column].isnull().sum()
        
        if missing_count == 0:
            continue
        
        missing_pct = (missing_count / len(df_filled)) * 100
        
        # Stratégie selon le pourcentage de valeurs manquantes
        if missing_pct > 50:
            # Suppression de la colonne si >50% manquant
            df_filled = df_filled.drop(columns=[column])
            print(f"      ✗ Colonne '{column}' supprimée ({missing_pct:.1f}% manquant)")
        
        elif pd.api.types.is_numeric_dtype(df_filled[column]):
            # Pour les colonnes numériques : remplissage avec médiane ou 0
            if missing_pct < 5:
                # Interpolation pour les séries temporelles
                if 'date' in df_filled.columns:
                    df_filled[column] = df_filled.groupby('location')[column].transform(
                        lambda x: x.interpolate(method='linear', limit_direction='both')
                    ) if 'location' in df_filled.columns else df_filled[column].interpolate()
                else:
                    df_filled[column].fillna(df_filled[column].median(), inplace=True)
                print(f"      ✓ '{column}' : interpolation/médiane ({missing_count} valeurs)")
            else:
                # Remplissage avec 0 pour des taux élevés
                df_filled[column].fillna(0, inplace=True)
                print(f"      ✓ '{column}' : remplissage avec 0 ({missing_count} valeurs)")
        
        else:
            # Pour les colonnes catégorielles : mode ou "Unknown"
            if missing_pct < 10:
                mode_value = df_filled[column].mode()[0] if len(df_filled[column].mode()) > 0 else 'Unknown'
                df_filled[column].fillna(mode_value, inplace=True)
                print(f"      ✓ '{column}' : mode '{mode_value}' ({missing_count} valeurs)")
            else:
                df_filled[column].fillna('Unknown', inplace=True)
                print(f"      ✓ '{column}' : 'Unknown' ({missing_count} valeurs)")
    
    missing_after = df_filled.isnull().sum().sum()
    print(f"   → Valeurs manquantes : {missing_before} → {missing_after}")
    
    return df_filled


def fix_data_types(df):
    """
    Corrige et standardise les types de données
    
    Args:
        df (pd.DataFrame): DataFrame à traiter
    
    Returns:
        pd.DataFrame: DataFrame avec types corrigés
    """
    print("\n   🔧 Correction des types de données :")
    df_typed = df.copy()
    
    # Conversion des dates
    date_columns = ['date', 'Date', 'DATE']
    for col in date_columns:
        if col in df_typed.columns:
            try:
                df_typed[col] = pd.to_datetime(df_typed[col], errors='coerce')
                print(f"      ✓ '{col}' converti en datetime")
            except Exception as e:
                print(f"      ⚠️  Erreur conversion '{col}' : {e}")
    
    # Conversion des colonnes numériques
    numeric_keywords = ['cases', 'deaths', 'vaccinations', 'total', 'new', 'rate', 'count']
    for col in df_typed.columns:
        if any(keyword in col.lower() for keyword in numeric_keywords):
            if not pd.api.types.is_numeric_dtype(df_typed[col]):
                try:
                    df_typed[col] = pd.to_numeric(df_typed[col], errors='coerce')
                    print(f"      ✓ '{col}' converti en numérique")
                except:
                    pass
    
    return df_typed


def validate_values(df):
    """
    Valide et corrige les valeurs incohérentes
    
    Args:
        df (pd.DataFrame): DataFrame à valider
    
    Returns:
        pd.DataFrame: DataFrame validé
    """
    print("\n   ✓ Validation des valeurs :")
    df_valid = df.copy()
    
    # Suppression des valeurs négatives dans les colonnes de comptage
    count_columns = [col for col in df_valid.columns 
                     if any(x in col.lower() for x in ['cases', 'deaths', 'tests', 'vaccinations'])]
    
    for col in count_columns:
        if pd.api.types.is_numeric_dtype(df_valid[col]):
            negative_count = (df_valid[col] < 0).sum()
            if negative_count > 0:
                df_valid.loc[df_valid[col] < 0, col] = 0
                print(f"      ✓ '{col}' : {negative_count} valeurs négatives corrigées")
    
    # Suppression des lignes avec dates invalides
    if 'date' in df_valid.columns:
        invalid_dates = df_valid['date'].isnull().sum()
        if invalid_dates > 0:
            df_valid = df_valid[df_valid['date'].notna()]
            print(f"      ✓ {invalid_dates} lignes avec dates invalides supprimées")
    
    return df_valid


def sort_data(df):
    """
    Trie les données par date et/ou localisation
    
    Args:
        df (pd.DataFrame): DataFrame à trier
    
    Returns:
        pd.DataFrame: DataFrame trié
    """
    sort_columns = []
    
    if 'location' in df.columns:
        sort_columns.append('location')
    if 'date' in df.columns:
        sort_columns.append('date')
    
    if sort_columns:
        df_sorted = df.sort_values(by=sort_columns).reset_index(drop=True)
        print(f"   ✓ Données triées par : {', '.join(sort_columns)}")
        return df_sorted
    
    return df


def get_cleaning_summary(df_original, df_cleaned):
    """
    Génère un résumé du nettoyage effectué
    
    Args:
        df_original (pd.DataFrame): DataFrame original
        df_cleaned (pd.DataFrame): DataFrame nettoyé
    
    Returns:
        dict: Dictionnaire avec les statistiques de nettoyage
    """
    summary = {
        'rows_original': len(df_original),
        'rows_cleaned': len(df_cleaned),
        'rows_removed': len(df_original) - len(df_cleaned),
        'columns_original': len(df_original.columns),
        'columns_cleaned': len(df_cleaned.columns),
        'columns_removed': len(df_original.columns) - len(df_cleaned.columns),
        'missing_original': df_original.isnull().sum().sum(),
        'missing_cleaned': df_cleaned.isnull().sum().sum()
    }
    
    return summary


# Test du module
if __name__ == "__main__":
    print("=== Test du module data_cleaner ===\n")
    
    # Création de données de test avec problèmes
    test_data = {
        'date': ['2024-01-01', '2024-01-02', '2024-01-02', None, '2024-01-05'],
        'location': ['France', 'France', 'France', 'Germany', 'Germany'],
        'cases': [100, 150, 150, -50, None],
        'deaths': [10, 15, 15, 5, 20]
    }
    
    df_test = pd.DataFrame(test_data)
    print("Données de test :")
    print(df_test)
    print("\n" + "="*50 + "\n")
    
    df_clean = clean_data(df_test)
    print("\n" + "="*50)
    print("\nDonnées nettoyées :")
    print(df_clean)
    print("\n✅ Module data_cleaner testé avec succès")
