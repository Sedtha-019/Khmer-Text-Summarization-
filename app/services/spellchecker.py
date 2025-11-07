from akara_custom import SpellChecker

checker = SpellChecker()

def correct_word(word: str) -> str:
    """Return the best spelling suggestion for a single token."""
    suggestions = checker.suggest(word)
    if (not suggestions) or suggestions == ['ក', 'ខ', 'គ']:
        return word  # if no suggestion, keep original
    return suggestions[0]  # take the top suggestion