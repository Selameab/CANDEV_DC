from tinydb import TinyDB, Query
import random

ABBR_TO_DB = {
    'ON': 'scrapers/ontario/ontario.json',
    'AB': 'scrapers/alberta/alberta.json',
    'NS': 'scrapers/nova_scotia/NS.json'
}

ABBR_TO_FULL = {
    'ON': 'Ontario',
    # 'QC': 'Quebec',
    'NS': 'Nova Scotia',
    'NB': 'New Brunswick',
    # 'MB': 'Manitoba',
    # 'BC': 'British Columbia',
    # 'PE': 'Prince Edward Island',
    # 'SK': 'Saskatchewan',
    'AB': 'Alberta',
    'NL': 'Newfoundland and Labrador'
}

ABBR_TO_MEAN = {
    'QC': 18000,
    'MB': 3000,
    'BC': 7000,
    'PE': 1500,
    'SK': 2500,
    'NL': 1500,
    'NS': 3000,
    'NB': 4000
}

ABBRS = list(ABBR_TO_FULL.keys())
PROVINCES = [v for _, v in ABBR_TO_FULL.items()]


def get_simulated_data(abbr):
    mean = ABBR_TO_MEAN[abbr]
    return [{'Time': '-', 'Demand': mean + random.uniform(-0.1 * mean, 0.1 * mean)}]


# Returns historic data of one province
def get_historic_data(abbr):
    # Fetch value from db if it exists
    if abbr in ABBR_TO_DB:
        db = TinyDB(ABBR_TO_DB[abbr])
        data = sorted(db.all(), key=lambda record: record['Time'])
        return data
    else:  # Simulate
        return get_simulated_data(abbr)


# Returns the most recent power demand for all provinces as a dict
def get_current_data():
    data = {}
    for abbr in ABBRS:
        x = get_historic_data(abbr)[-1]
        data[abbr] = {'Time': x['Time'], 'Demand': round(x['Demand'], 2)}
    return data


def main():
    print(get_historic_data('NS'))
    # print(get_historic_data('ON')[-1])
    # print(get_demand('AB')[-1])
    # a = get_current_data()
    # print(get_current_data())


if __name__ == '__main__':
    main()
