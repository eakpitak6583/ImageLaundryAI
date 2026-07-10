from parsers.model_parser import extract_model

samples = [

    "MODEL : DI225",

    "Flatwork Ironer IM1200X3300X3",

    "MODEL SI275",

    "SL400-3 Steam",

    "XD120 Gas"

]

for s in samples:

    print(s)

    print("→", extract_model(s))

    print("-"*40)