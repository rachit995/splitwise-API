data = {
    "spender": [
        {
            "user_id": "A",
            "share": 30
        },
        {
            "user_id": "B",
            "share": 70
        },
        {
            "user_id": "C",
            "share": 0
        }
    ],
    "splits": [
        {
            "user_id": "A",
            "share": 0
        },
        {
            "user_id": "B",
            "share": 50
        },
        {
            "user_id": "C",
            "share": 50
        }
    ]
}
total_spender_amount = 0
spender = {}
splits = {}
for sp in data["spender"]:
    total_spender_amount += sp["share"]
    spender[sp["user_id"]] = sp["share"]
total_splits_amount = 0
for sp in data["splits"]:
    total_splits_amount += sp["share"]
    splits[sp["user_id"]] = sp["share"]
transactions = []
for spend in spender:
    if spender[spend] != 0:
        for split in splits:
            if split != spend and splits[split] != 0 and spender[spend] != 0:
                t = {}
                if splits[split] > spender[spend]:
                    t["payee"] = split
                    t["amount"] = spender[spend]
                    t["payer"] = spend
                    spender[spend] = 0
                    splits[split] -= spender[spend]
                else:
                    t["payee"] = split
                    t["amount"] = splits[split]
                    t["payer"] = spend
                    spender[spend] -= splits[split]
                    splits[split] = 0
                transactions.append(t)
print(spender, splits, transactions)
