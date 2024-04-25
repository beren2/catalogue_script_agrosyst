#!/bin/bash
# script pour creer les data set d'exemples pour les scripts de pre traitement.
# On ne veux selectionner que une partie des lignes des data entiers

# 1 isole dans id.txt les identifiants voulus , pour lit le fichier et avec grep , ne selectionne que celles voulu
# Si on veux les id dans metadata test, on peut les copier coller dans id.txt et ne executer que les lignes de grep


# Cas 1 : on passe de fichier en fichier vers le bas , ex : zone -> noeuds_realise #
#---------------------------------------------------#

<<comment
f_echelle_sup='synthetise.csv'

nom_fichier_atrier='plantation_perenne_synthetise'
fichier_atrier=$nom_fichier_atrier'.csv'


awk  'BEGIN {FS = ","} {if (NR == 1) {
                                for(i=1; i<=NF; i++){
                                    search = match($i, /'^id$'/)
                                        if(search) {champ = i} 
                                    }
                                    } if(NR > 1){
            print $champ}}' $f_echelle_sup > $repertoire_data_ex"id.txt"
comment

# Cas 2 : on passe de fichier en fichier vers le haut , ex : zone -> parcelle 
#---------------------------------------------------#


f_echelle_inf='parcelle.csv'
nom_fichier_atrier='sdc'
fichier_atrier=$nom_fichier_atrier'.csv'
<<comment
awk  'BEGIN {FS = ","} {if (NR == 1) {
                                for(i=1; i<=NF; i++){
                                    search = match($i, /'$nom_fichier_atrier'_id/)
                                        if(search) {champ = i} 
                                    }
                                    } if(NR > 1){
            print $champ}}' $f_echelle_inf > $repertoire_data_ex"id.txt"
comment

# Pour les deux cas : 
# -------------------
repertoire_data_complet="../../../scripts/pz0/data/"
repertoire_data_ex="./"

head -n1 $repertoire_data_complet$fichier_atrier > $repertoire_data_ex$fichier_atrier
grep -f $repertoire_data_ex"id.txt" $repertoire_data_complet$fichier_atrier >> $repertoire_data_ex$fichier_atrier
