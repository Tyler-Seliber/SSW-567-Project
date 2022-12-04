MAX_LINE_CHARACTERS = 44
# Dictionary to map digits to numeric values for check digit calculation
digit_map = {
    '<': 0,
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'A': 10,
    'B': 11,
    'C': 12,
    'D': 13,
    'E': 14,
    'F': 15,
    'G': 16,
    'H': 17,
    'I': 18,
    'J': 19,
    'K': 20,
    'L': 21,
    'M': 22,
    'N': 23,
    'O': 24,
    'P': 25,
    'Q': 26,
    'R': 27,
    'S': 28,
    'T': 29,
    'U': 30,
    'V': 31,
    'W': 32,
    'X': 33,
    'Y': 34,
    'Z': 35
}
# Weighting for the check digit calculation
weightings = [7, 3, 1]

# Helper function to check fields and check digits
def checkField(field, provided_digit):
    '''Checks the field and returns True if it is valid and False otherwise'''
    field_splice = list(field)
    # Assign numeric values to each character in the field
    numeric_values = list(map(lambda x: digit_map[x], field_splice))

    # Assign weights to the digits
    for i in range(len(numeric_values)):
        numeric_values[i] *= weightings[i % len(weightings)]

    # Sum the weighted digits
    numeric_sum = sum(numeric_values)

    # Calculate the check digit
    calculated_digit = numeric_sum % 10

    # Check if the calculated digit matches the provided digit
    if calculated_digit == provided_digit:
        return 'Passed'
    else:
        return 'Failed'
     
def query_db(personal_number):
    '''Queries the database and returns the result'''
    pass

# Requirement 1
def scanMRZ(doc):
    '''Scans the MRZ of a travel document and returns the two lines as strings'''
    pass

# Requirement 2
def decodeMRZ(line1, line2):
    '''Decodes the MRZ and returns a dictionary with the following keys'''
    # Decode line1
    list1 = line1.split('<') # Split the line into a list of strings with '<' as the delimiter
    list1[:] = [value for value in list1 if value != ''] # Remove empty strings from the list
    # Separate country code from last name
    country_code = list1[1][0:3]
    last_name = list1[1][3:]
    del list1[1] # Remove the country code and last name combo from the list
    list1.insert(1, country_code)
    list1.insert(2, last_name)

    # Re-insert empty string if person does not have a middle name
    if len(list1) == 4:
        list1.append('')

    # Decode line2
    # Split the line into a list of strings
    list2 = []
    list2.append(line2[0:9]) # Passport number
    list2.append(line2[9:10]) # Check digit for passport number
    list2.append(line2[10:13]) # Country Code
    list2.append(line2[13:19]) # Birth date (YYMMDD)
    list2.append(line2[19:20]) # Check digit for birth date
    list2.append(line2[20:21]) # Sex (M/F)
    list2.append(line2[21:27]) # Expiration date (YYMMDD)
    list2.append(line2[27:28]) # Check digit for expiration date
    list2.append(line2[28:-1]) # Personal number
    list2.append(line2[-1:]) # Check digit for personal number

    # Combine the two lists into a dictionary
    traveler_info = {
        'document_type': list1[0],
        'issuing_country': list1[1],
        'last_name': list1[2],
        'first_name': list1[3],
        'middle_name': list1[4],
        'passport_number': list2[0],
        'passport_number_check_digit': list2[1],
        'country_code': list2[2],
        'birth_date': list2[3],
        'birth_date_check_digit': list2[4],
        'sex': list2[5],
        'expiration_date': list2[6],
        'expiration_date_check_digit': list2[7],
        'personal_number': list2[8],
        'personal_number_check_digit': list2[9]
    }
    return traveler_info

# Requirement 3
def encodeTravelInfo(personal_number):
    '''Encodes the travel information from a database entry into the two lines of the MRZ'''
    # Query the database for the traveler's information
    traveler_info = query_db(personal_number)

    # Encode the first line
    line1 = traveler_info['document_type'] + '<' + traveler_info['issuing_country'] + traveler_info['last_name'] + '<<' + traveler_info['first_name'] + '<<' + traveler_info['middle_name']
    x = len(line1)
    line1 += '<' * (MAX_LINE_CHARACTERS - x)

    # Encode the second line
    line2 = traveler_info['passport_number'] + traveler_info['passport_number_check_digit'] + traveler_info['country_code'] + traveler_info['birth_date'] + traveler_info['birth_date_check_digit'] + traveler_info['sex'] + traveler_info['expiration_date'] + traveler_info['expiration_date_check_digit'] + traveler_info['personal_number']
    x = len(line2)
    line2 += '<' * (MAX_LINE_CHARACTERS - x - 1)
    line2 += traveler_info['personal_number_check_digit']

    return [line1, line2]

# Requirement 4
def checkMRZ(traveler_info):
    '''Checks the MRZ and returns True if it is valid and False otherwise'''
    failed_checks = {
        'Passport Number': checkField(traveler_info['passport_number'], int(traveler_info['passport_number_check_digit'])),
        'Birth Date': checkField(traveler_info['birth_date'], int(traveler_info['birth_date_check_digit'])),
        'Expiration Date': checkField(traveler_info['expiration_date'], int(traveler_info['expiration_date_check_digit'])),
        'Personal Number': checkField(traveler_info['personal_number'], int(traveler_info['personal_number_check_digit']))
    }
    return failed_checks

def main():
    line1 = 'P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<'
    line2 = 'L898902C36UT07408122F1204159ZE184226B<<<<<<1'

    info = decodeMRZ(line1, line2)
    print('Traveler info: ' + str(info))
    print('Check results: ' + str(checkMRZ(info)))


if __name__ == '__main__':
    main()