from package_sequence import Package2Sequence
import pickle

SPECIAL_CHAR = {
        "~",
        "!",
        "@",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*",
        "(",
        ")",
        "_",
        "+",
        "-",
        "=",
        ".",
        "[",
        "]",
        "{",
        "}",
        ";",
        "'",
        ":",
        "\"",
        "/",
        "\\",
        "|",
        "?",
        ",",
        ">",
        "<",
    }


MAX_LEN = 1000

BATCH_SIZE = 128

HIDDEN_SIZE = 128
NUM_LAYERS = 2

ps: Package2Sequence = pickle.load(open("ps.pkl", "rb"))
