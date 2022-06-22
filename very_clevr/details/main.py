def normalize(input_data):
    return input_data


def compare(exemplar, input_data):
    comparable_data = normalize(input_data)
    result = exemplar - comparable_data
    return result
