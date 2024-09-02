from fire import Fire

from rpyt.l10n import (
    make_src_files,
    make_tl_files,
)


class Rpytl10n:
    mksrc = staticmethod(make_src_files)
    mktl = staticmethod(make_tl_files)


class Rpyt:
    l10n = Rpytl10n()


def main():
    Fire(Rpyt())


if __name__ == "__main__":
    main()
