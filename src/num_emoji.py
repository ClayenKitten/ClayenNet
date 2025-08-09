def num_to_emoji_str(num: int) -> str:
    result = ""
    if num == 0:
        return dictionary[0]
    while num != 0:
        num, d = divmod(num, 10)
        result = dictionary[int(d)] + result
    return result


dictionary = {
    0: "0️⃣",
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣",
    6: "6️⃣",
    7: "7️⃣",
    8: "8️⃣",
    9: "9️⃣",
}
