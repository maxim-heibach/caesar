import sys

# Aufgabenteil a) Verschlüsselung des übergebenen Texts
def encode_text(text, key):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char = char.lower()
            # Um den verschobenen Buchstaben zu erhalten, wird zunächst der Wert, der den Buchstaben "a" 
            # repräsentiert (ord('a'), Wert: 97) vom Ausgangsbuchstaben abgezogen, um sicherzustellen, dass 
            # das Alphabet nach dem Buchstaben "z" wieder von vorne durchlaufen wird. Dank des dividierens von 
            # (ord(char) - ord('a') + key) durch Modulo 26 erhält man stets einen Wert zwischen 0 und 25, 
            # welcher nach Addition von ord('a') einen Wert ergibt, der einen verschobenen Buchstaben im 
            # Bereich "a-z" repräsentiert.
            shifted_char = chr(((ord(char) - ord('a') + key) % 26) + ord('a'))
            if is_upper:
                shifted_char = shifted_char.upper()
            encrypted_text += shifted_char
        else:
            encrypted_text += char
    return encrypted_text

# Aufgabenteil b) Häufigkeit der vorkommenden Buchstaben im Ausgangstext
def string_histogram(text):
    histogram = {}
    for char in text:
        if char.isalpha():
            char = char.lower()
            if char in histogram:
                histogram[char] += 1
            else:
                histogram[char] = 1
    return histogram

# Aufgabenteil c) Wahrscheinlichkeit der vorkommenden Buchstaben im Text
def frequencies(histogram):
    sum_letters = sum(histogram.values())
    probabilities = [histogram.get(char, 0) / sum_letters for char in 'abcdefghijklmnopqrstuvwxyz']
    return probabilities

# Aufgabenteil d) Entschlüsselung eines Cäsar-verschlüsselten Textes
def chi_squared(observed, expected):
    # Chi-squared berechnet Wahrscheinlichkeitsvektoren für jeden möglichen Schlüssel
    # range(26) da ab 0 gezählt wird und das obere Ende der Summennotation nicht inklusive ist -> 25+1
    chi_squared_value = sum([(observed[i] - expected[i]) ** 2 / expected[i] for i in range(26)])
    return chi_squared_value

def crack_caesar(exampletext, text):
    example_histogram = string_histogram(exampletext)
    example_freq = frequencies(example_histogram)
    best_key = 0
    best_chi_squared = float("inf")
    for key in range(26):
        encrypted_histogram = string_histogram(encode_text(text, -key))
        encrypted_freq = frequencies(encrypted_histogram)
        chi_squared_value = chi_squared(encrypted_freq, example_freq)

        if chi_squared_value < best_chi_squared:
            best_chi_squared = chi_squared_value
            best_key = key

    decrypted_text = encode_text(text, -best_key)
    return decrypted_text

if __name__ == "__main__":
    l = len(sys.argv)
    print(l)
    
    if len(sys.argv) < 2:
        print("\nFehler: Weniger als 2 Parameter eingegeben. \nVerschlüsselung auf Konsole wie folgt aufrufen: python caesar.py \"Text\" Schlüssel")
        sys.exit(1)

    text = sys.argv[1]
    key = int(sys.argv[2])

    encrypted_text = encode_text(text, key)
    print("\nVerschlüsselter Text:")
    print(encrypted_text)
    
    histogram = string_histogram(text)
    print("\nHäufigkeit eines Buchstabens im Text:")
    print(histogram)

    freq = frequencies(histogram)
    print("\nWahrscheinlichkeit mit der ein Buchstabe im Text vorkommt:")
    print(freq)

    exampletext = "qx I know that virtue to be in you, Brutus, As well as I do know your outward favor. Well, honor is the subject of my story. I cannot tell what you and other men Think of this life; but, for my single self, I had not as lief live to be In awe of such a thing as I myself. I was born free as Caesar; so were you: We both have fed as well, and we can both Endure the winter's cold as well as he: For once, upon a raw and gusty day, The troubled Tiber chafing with her shores, Caesar said to me 'Darest thou, Cassius, now Leap in with me into this angry flood, And swim to yonder point?' Upon the word, Accoutred as I was, I plunged in And bathed him follow; so indeed he did. The torrent roar'd, and we did buffet it With lusty sinews, throwing it aside And stemming it with hearts of controversy; But ere we could arrive the point proposed, Caesar cried 'Help me, Cassius, or I sink!' I, as Aeneas, our great ancestor, Did from the flames of Troy upon his shoulder The old Anchises bear, so from the waves of Tiber Did I the tired Caesar. And this man Is now become a god, and Cassius is A wretched creature and must bend his body, If Caesar carelessly but nod on him. He had a fever when he was in Spain, And when the fit was on him, I did mark How he did shake: 'tis true, this god did shake; His coward lips did from their color fly, And that same eye whose bend doth awe the world Did lose his lustre: I did hear him groan: Ay, and that tongue of his that bade the Romans Mark him and write his speeches in their books, Alas, it cried 'Give me some drink, Titinius,' As a sick girl. Ye gods, it doth amaze me A man of such a feeble temper should So get the start of the majestic world And bear the palm alone."
    text = encrypted_text
    decrypted_text = crack_caesar(exampletext, text)
    print("\nEntschlüsselter Text:")
    print(decrypted_text)