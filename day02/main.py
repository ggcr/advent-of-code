from collections import defaultdict
import os


def parse(filename: str) -> list[str]:
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), filename), "r+"
    ) as fd:
        data = fd.read().strip()
        return data.split(",")


def isTwice(id: int) -> bool:
    sid = str(id)
    if len(sid) % 2 != 0:
        return False
    M = len(sid) // 2
    L, R = sid[:M], sid[M:]
    return L == R

def freq(id: int) -> dict[str, int]:
    d = defaultdict(int)
    for ch in str(id):
        d[ch] += 1
    return d

def solve_part1(ids: list[str]) -> int:
    res = 0
    for id in ids:
        assert len(id.split("-")) == 2
        firstId, lastId = id.split("-")

        # None of the numbers have leading zeroes; 0101 isn't an ID at all
        # hmmm this can only happen on the first or last

        firstIdInt = int(firstId)
        if len(str(firstIdInt)) != len(firstId):
            print(f"Invalid id: {firstId}")
            res += firstIdInt

        lastIdInt = int(lastId)
        if len(str(lastIdInt)) != len(lastId):
            print(f"Invalid id: {lastId}")
            res += lastIdInt

        for currentId in range(firstIdInt, lastIdInt + 1):
            # any ID which is made only of some sequence of digits repeated twice
            if isTwice(currentId):
                print(f"Invalid id: {currentId}")
                res += currentId
                continue

    return res


def isRepeated(currentId) -> bool:
    sid = str(currentId)
    lsid = len(str(currentId))
    for i in range(2, lsid):
        if lsid % i != 0:
            continue
        # try to form X groups of all the substrings of len (i) and see if there is any repeated
        n = lsid // i
        cache = set()
        for j in range(0, lsid, n):
            c = int(sid[j:j+n])
            cache.add(c)
        if len(cache) == 1:
            return True
    return False


def solve_part2(ids: list[str]) -> int:
    res = 0
    for id in ids:
        assert len(id.split("-")) == 2
        firstId, lastId = id.split("-")

        # None of the numbers have leading zeroes; 0101 isn't an ID at all
        # hmmm this can only happen on the first or last
        firstIdInt = int(firstId)
        if len(str(firstIdInt)) != len(firstId):
            print(f"Invalid id: {firstId}")
            res += firstIdInt
        lastIdInt = int(lastId)
        if len(str(lastIdInt)) != len(lastId):
            print(f"Invalid id: {lastId}")
            res += lastIdInt

        for currentId in range(firstIdInt, lastIdInt + 1):
            # any ID which is made only of some sequence of digits repeated (at least) twice
            f = freq(currentId).values()
            if min(f) < 2:
                continue
            if len(set(f)) == 1 and list(f)[0] == len(str(currentId)):
                print(f"Invalid id: {currentId}")
                res += currentId
                continue
            if isRepeated(currentId):
                print(f"Invalid id: {currentId}")
                res += currentId

    return res


if __name__ == "__main__":
    assert solve_part1(parse("example.txt")) == 1227775554
    print(solve_part1(parse("input.txt")))
    assert solve_part2(parse("example.txt")) == 4174379265
    print(solve_part2(parse("input.txt")))
