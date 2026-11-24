"""Write the entrant's own make.fun handle to /output/entry.txt."""

ENTRY = "daring-lark-71"


def main():
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(ENTRY)


if __name__ == "__main__":
    main()
