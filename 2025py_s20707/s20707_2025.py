# CEL PROGRAMU:
# Program generuje losową sekwencję DNA o długości zadanej przez użytkownika, zapisuje ją w formacie FASTA
# oraz oblicza statystyki procentowej zawartości nukleotydów i stosunek CG/AT.
# Imię użytkownika wstawiane jest w losowym miejscu sekwencji (bez wpływu na statystyki biologiczne).
# KONTEKST ZASTOSOWANIA: Użyteczny w nauce bioinformatyki i pracy z formatem FASTA.

import random  # Import modułu random do losowego generowania danych

# Funkcja generująca losową sekwencję DNA
def generate_dna_sequence(length):
    nucleotides = ['A', 'C', 'G', 'T']  # Lista dostępnych nukleotydów
    return ''.join(random.choices(nucleotides, k=length))  # Zwraca ciąg losowych nukleotydów o zadanej długości

# Funkcja wstawiająca imię do sekwencji (nie liczy się do statystyk)
def insert_name(sequence, name):
    position = random.randint(0, len(sequence))  # Wybiera losową pozycję w sekwencji
    return sequence[:position] + name + sequence[position:]  # Wstawia imię w wybrane miejsce

# Funkcja licząca statystyki zawartości nukleotydów
def calculate_stats(sequence):
    stats = {}  # Słownik na statystyki
    total = len(sequence)  # Długość sekwencji
    for nucleotide in ['A', 'C', 'G', 'T']:  # Dla każdego nukleotydu
        stats[nucleotide] = round((sequence.count(nucleotide) / total) * 100, 1)  # Oblicz procentową zawartość
    cg = sequence.count('C') + sequence.count('G')  # Liczba C i G
    at = sequence.count('A') + sequence.count('T')  # Liczba A i T
    cg_at_ratio = round((cg / at), 1) if at != 0 else 0  # Oblicz stosunek CG/AT (z zabezpieczeniem przed dzieleniem przez 0)
    return stats, cg_at_ratio  # Zwraca statystyki i stosunek

# ----------------------------------------------
# Pobieranie danych od użytkownika z walidacją
# ----------------------------------------------

# ORIGINAL:
# length = int(input("Podaj długość sekwencji: "))
# MODIFIED (dodano walidację długości: tylko liczby całkowite > 0)
while True:  # Pętla do momentu poprawnego wprowadzenia długości
    try:
        length = int(input("Podaj długość sekwencji: "))  # Wczytaj długość
        if length > 0:  # Sprawdź, czy jest większa od 0
            break  # Jeśli tak, przerwij pętlę
        else:
            print("Długość musi być większa od zera.")  # Komunikat o błędzie
    except ValueError:
        print("Błąd: podaj liczbę całkowitą.")  # Komunikat o błędzie przy niecałkowitej wartości

sequence_id = input("Podaj ID sekwencji: ")  # Pobierz ID sekwencji
description = input("Podaj opis sekwencji: ")  # Pobierz opis sekwencji

# ORIGINAL:
# name = input("Podaj imię: ")
# MODIFIED (dodano walidację: tylko litery, bez cyfr/znaków specjalnych)
while True:  # Pętla do momentu poprawnego wprowadzenia imienia
    name = input("Podaj imię: ")  # Pobierz imię
    if name.isalpha():  # Sprawdź, czy imię zawiera tylko litery
        break  # Jeśli tak, zakończ pętlę
    else:
        print("Imię może zawierać tylko litery (bez cyfr i znaków specjalnych).")  # Komunikat o błędzie

# Generowanie i modyfikacja sekwencji
original_sequence = generate_dna_sequence(length)  # Generuj losową sekwencję DNA
sequence_with_name = insert_name(original_sequence, name)  # Wstaw imię do sekwencji (tylko do zapisu)

# Zapis do pliku FASTA z obsługą błędów
# ORIGINAL:
# filename = f"{sequence_id}.fasta"
# with open(filename, 'w') as fasta_file:
#     fasta_file.write(f">{sequence_id} {description}\n")
#     fasta_file.write(sequence_with_name + '\n')
# print(f"Sekwencja została zapisana do pliku {filename}")

# MODIFIED (dodano obsługę IOError przy zapisie pliku)
filename = f"{sequence_id}.fasta"  # Ustaw nazwę pliku
try:
    with open(filename, 'w') as fasta_file:  # Otwórz plik do zapisu
        fasta_file.write(f">{sequence_id} {description}\n")  # Zapisz nagłówek FASTA
        fasta_file.write(sequence_with_name + '\n')  # Zapisz sekwencję z imieniem
    print(f"Sekwencja została zapisana do pliku {filename}")  # Potwierdzenie sukcesu
except IOError:  # Obsługa błędu zapisu
    print(f"Błąd: Nie udało się zapisać pliku {filename}.")  # Komunikat o błędzie

# Obliczanie i wypisywanie statystyk
stats, cg_at_ratio = calculate_stats(original_sequence)  # Oblicz statystyki (na podstawie oryginalnej sekwencji)
print("Statystyki sekwencji:")  # Nagłówek
for nucleotide, percentage in stats.items():  # Dla każdego nukleotydu
    count = original_sequence.count(nucleotide)  # Liczba wystąpień
    print(f"{nucleotide}: {percentage}% ({count} razy)")  # Wyświetl statystyki
print(f"Stosunek CG/AT: {cg_at_ratio}")  # Wyświetl stosunek CG do AT
