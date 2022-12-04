# # Helper function to check fields and check digits
# def checkField(field, digits):
#     '''Checks the field and returns True if it is valid and False otherwise'''
#     pass

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
    print(list1)

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

    print(list2)

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
def encodeTravelInfo(dbEntry):
    '''Encodes the travel information from a database entry into the two lines of the MRZ'''
    pass

# Requirement 4
def checkMRZ(line1, line2):
    '''Checks the MRZ and returns True if it is valid and False otherwise'''
    pass

def main():
    line1 = 'P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<'
    line2 = 'L898902036UT07408122F1204159ZE184226B<<<<<<1'
    print(decodeMRZ(line1, line2))

if __name__ == '__main__':
    main()