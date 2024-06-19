#PROJECT ROOT DIRECTORY
DIRECTORY = "C:/Users/danik/Documents/School Files/Algae Research/processor"
riverids = {"st.louis": "04024000",
            "boisbrule": "04025500",
            "badriver": "04027000",
            "pigeonriver": "04010500"}
rivergroups = {1: "st.louis",
               2: "boisbrule",
               3: "badriver",
               4: "pigeonriver"}
rivernames = list(riverids.keys())
buoyids = {1: 'dulm5', 2: 'pngw3', 3: 'sxhw3', 4: 'pilm4'}
blooms = { 1: [[2018, 8, 19], [2021, 7, 17], [2021, 9, 10],
               [2021, 10, 1], [2022, 9, 20]],
           2: [[2012, 14, 7], [2016, 8, 31], [2017, 7, 11],
               [2017, 8, 9], [2018, 8, 13], [2019, 9, 14],
               [2020, 9, 5], [2020, 9, 23], [2021, 7, 18],
               [2023, 8, 7]],
           3: [[2018, 8, 12]],
           4: [[2021, 7, 9], [2023, 7, 25]]}

sets = {1: [563,23], 2: [565,73], 3: [559,119], 4: [661,249]}