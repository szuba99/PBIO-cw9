# CEL PROGRAMU:
# Program generuje losową sekwencję DNA o długości zadanej przez użytkownika, zapisuje ją w formacie FASTA
# oraz oblicza statystyki procentowej zawartości nukleotydów i stosunek CG/AT.
# Imię użytkownika wstawiane jest w losowym miejscu sekwencji (bez wpływu na statystyki biologiczne).
# KONTEKST ZASTOSOWANIA: Użyteczny w nauce bioinformatyki i pracy z formatem FASTA.

import random

# Funkcja generująca losową sekwencję DNA
def generate_dna_sequence(length):
    nucleotides = ['A', 'C', 'G', 'T']
    return ''.join(random.choices(nucleotides, k=length))

# Funkcja wstawiająca imię do sekwencji (nie liczy się do statystyk)
def insert_name(sequence, name):
    position = random.randint(0, len(sequence))
    return sequence[:position] + name + sequence[position:]

# Funkcja licząca statystyki zawartości nukleotydów
def calculate_stats(sequence):
    stats = {}
    total = len(sequence)
    for nucleotide in ['A', 'C', 'G', 'T']:
        stats[nucleotide] = round((sequence.count(nucleotide) / total) * 100, 1)
    cg = sequence.count('C') + sequence.count('G')
    at = sequence.count('A') + sequence.count('T')
    cg_at_ratio = round((cg / at), 1) if at != 0 else 0
    return stats, cg_at_ratio

# ----------------------------------------------
# Pobieranie danych od użytkownika z walidacją
# ----------------------------------------------

# ORIGINAL:
# length = int(input("Podaj długość sekwencji: "))
# MODIFIED (dodano walidację długości: tylko liczby całkowite > 0)
while True:
    try:
        length = int(input("Podaj długość sekwencji: "))
        if length > 0:
            break
        else:
            print("Długość musi być większa od zera.")
    except ValueError:
        print("Błąd: podaj liczbę całkowitą.")

sequence_id = input("Podaj ID sekwencji: ")
description = input("Podaj opis sekwencji: ")

# ORIGINAL:
# name = input("Podaj imię: ")
# MODIFIED (dodano walidację: tylko litery, bez cyfr/znaków specjalnych)
while True:
    name = input("Podaj imię: ")
    if name.isalpha():
        break
    else:
        print("Imię może zawierać tylko litery (bez cyfr i znaków specjalnych).")

# Generowanie i modyfikacja sekwencji
original_sequence = generate_dna_sequence(length)
sequence_with_name = insert_name(original_sequence, name)

# Zapis do pliku FASTA z obsługą błędów
# ORIGINAL:
# filename = f"{sequence_id}.fasta"
# with open(filename, 'w') as fasta_file:
#     fasta_file.write(f">{sequence_id} {description}\n")
#     fasta_file.write(sequence_with_name + '\n')
# print(f"Sekwencja została zapisana do pliku {filename}")

# MODIFIED (dodano obsługę IOError przy zapisie pliku)
filename = f"{sequence_id}.fasta"
try:
    with open(filename, 'w') as fasta_file:
        fasta_file.write(f">{sequence_id} {description}\n")
        fasta_file.write(sequence_with_name + '\n')
    print(f"Sekwencja została zapisana do pliku {filename}")
except IOError:
    print(f"Błąd: Nie udało się zapisać pliku {filename}.")

# Obliczanie i wypisywanie statystyk
stats, cg_at_ratio = calculate_stats(original_sequence)
print("Statystyki sekwencji:")
for nucleotide, percentage in stats.items():
    count = original_sequence.count(nucleotide)
    print(f"{nucleotide}: {percentage}% ({count} razy)")
print(f"Stosunek CG/AT: {cg_at_ratio}")
