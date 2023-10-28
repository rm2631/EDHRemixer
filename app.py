import os
from utils.Remixer import Remixer

def add_decks_to_remix(remix, folder_name):
    for file in os.listdir(folder_name):
        if file.endswith(".txt"):
            with open(os.path.join(folder_name, file), "r") as file_data:
                if folder_name == "source":
                    remix.add_deck(file, True, file_data.read())
                else:
                    remix.add_deck(file, False, file_data.read())


def main():
    ## load all files in folder called "source" in a list
    remixer = Remixer()
    remixer.add_deck("source", True)
    remixer.add_deck("target", False)
    remixer.reallocate()

if __name__ == "__main__":
    main()