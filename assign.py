import csv
import math


def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude to spherical coordinates in radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula to calculate the great-circle distance between two points on a sphere
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r * 1000  # Return distance in meters


def edit_distance(string1, string2):
    # Calculate the edit distance between two strings
    m, n = len(string1), len(string2)
    dp = [[0 for _ in range(n + 1)] for __ in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif string1[i-1] == string2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])
    return dp[m][n]


def is_similar(entry1, entry2):
    # Check if two entries are similar
    lat1, lon1, name1 = entry1
    lat2, lon2, name2 = entry2
    return haversine(lat1, lon1, lat2, lon2) <= 200 and edit_distance(name1, name2) <= 5


def process_dataset(dataset):
    # Process the dataset and return the similar entries
    n = len(dataset)
    results = []
    for i in range(n):
        for j in range(i + 1, n):
            if is_similar(dataset[i], dataset[j]):
                results.append([dataset[i], dataset[j]])
    return results


def read_dataset(filename):
    # Read the dataset from a csv file
    dataset = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip the header row
        for row in reader:
            name, lon, lat = row[0], float(row[1]), float(row[2])
            dataset.append((lat, lon, name))
    return dataset


def write_results(filename, results):
    # Write the results to a csv file
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['lat1', 'lon1', 'name1', 'lat2',
                        'lon2', 'name2', 'is_similar'])
        for result in results:
            lat1, lon1, name1 = result[0]
            lat2, lon2, name2 = result[1]
            writer.writerow([lat1, lon1, name1, lat2, lon2, name2, 1])


if __name__ == '__main__':
    dataset = read_dataset('dataset.csv')
    results = process_dataset(dataset)
    write_results('output.csv', results)
