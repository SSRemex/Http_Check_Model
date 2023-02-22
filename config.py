from package_sequence import Package2Sequence
import pickle
import torch

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

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

ps: Package2Sequence = pickle.load(open("model/ps.pkl", "rb"))
