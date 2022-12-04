import unittest
import MRTD
from unittest.mock import MagicMock, patch

class TestMRTD(unittest.TestCase):

    @patch('MRTD.scanMRZ')
    def test_scanMRZ(self, mockedDocument):
        # Test the scanMRZ function
        # NOTE: 'doc' is set to None as a placeholder for the document object
        # Test 1
        mockedDocument.return_value = ['P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<', 'L898902C36UT07408122F1204159ZE184226B<<<<<<1']
        doc = None
        output = MRTD.scanMRZ(doc)
        self.assertEqual(['P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<', 'L898902C36UT07408122F1204159ZE184226B<<<<<<1'], output)

        # Test 2
        mockedDocument.return_value = ['P<ITAPEPPERONI<<JOHNNY<DONNY<<<<<<<<<<<<<<<<<<<', '067FIKKXO7ITA8401186M9211041T8W3UK289<<<<<<<<<7']
        doc = None
        output = MRTD.scanMRZ(doc)
        self.assertEqual(['P<ITAPEPPERONI<<JOHNNY<DONNY<<<<<<<<<<<<<<<<<<<', '067FIKKXO7ITA8401186M9211041T8W3UK289<<<<<<<<<7'], output)

        # Test 3
        mockedDocument.return_value = ['P<FRABAGUETTE<<OUI<<<<<<<<<<<<<<<<<<<<<<<<<<<<<', '4J5S0UCIU4FRA1506303F370808664U4CO5DC<<<<<<<<<8']
        doc = None
        output = MRTD.scanMRZ(doc)
        self.assertEqual(['P<FRABAGUETTE<<OUI<<<<<<<<<<<<<<<<<<<<<<<<<<<<<', '4J5S0UCIU4FRA1506303F370808664U4CO5DC<<<<<<<<<8'], output)

        # Test 4
        mockedDocument.return_value = ['P<ALBFRANKLIN<<ARNOLD<SWOLE<<<<<<<<<<<<<<<<<<<<', 'MN6JC8BV39ALB4912251M09103184UR757JNNONF8FLF3C1']
        doc = None
        output = MRTD.scanMRZ(doc)
        self.assertEqual(['P<ALBFRANKLIN<<ARNOLD<SWOLE<<<<<<<<<<<<<<<<<<<<', 'MN6JC8BV39ALB4912251M09103184UR757JNNONF8FLF3C1'], output)

    def test_decodeMRZ(self):
        # Test the decodeMRZ function
        # Test 1
        line1 = 'P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<'
        line2 = 'L898902C36UT07408122F1204159ZE184226B<<<<<<1'
        expected = {'document_type': 'P', 'issuing_country': 'UTO', 'last_name': 'ERIKSSON', 'first_name': 'ANNA', 'middle_name': 'MARIA', 'passport_number': 'L898902C3', 'passport_number_check_digit': '6', 'country_code': 'UT0', 'birth_date': '740812', 'birth_date_check_digit': '2', 'sex': 'F', 'expiration_date': '120415', 'expiration_date_check_digit': '9', 'personal_number': 'ZE184226B<<<<<<', 'personal_number_check_digit': '1'}
        actual = MRTD.decodeMRZ(line1, line2)
        self.assertEqual(expected, actual)

        # Test 2
        line1 = 'P<ITAPEPPERONI<<JOHNNY<DONNY<<<<<<<<<<<<<<<<<<<'
        line2 = '067FIKKXO7ITA8401186M9211041T8W3UK289<<<<<<<<<7'
        expected = {'document_type': 'P', 'issuing_country': 'ITA', 'last_name': 'PEPPERONI', 'first_name': 'JOHNNY', 'middle_name': 'DONNY', 'passport_number': '067FIKKXO', 'passport_number_check_digit': '7', 'country_code': 'ITA', 'birth_date': '840118', 'birth_date_check_digit': '6', 'sex': 'M', 'expiration_date': '921104', 'expiration_date_check_digit': '1', 'personal_number': 'T8W3UK289<<<<<<<<<', 'personal_number_check_digit': '7'}
        actual = MRTD.decodeMRZ(line1, line2)
        self.assertEqual(expected, actual)

        # Test 3 - No middle name
        line1 = 'P<FRABAGUETTE<<OUI<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
        line2 = '4J5S0UCIU4FRA1506303F370808664U4CO5DC<<<<<<<<<8'
        expected = {'document_type': 'P', 'issuing_country': 'FRA', 'last_name': 'BAGUETTE', 'first_name': 'OUI', 'middle_name': '', 'passport_number': '4J5S0UCIU', 'passport_number_check_digit': '4', 'country_code': 'FRA', 'birth_date': '150630', 'birth_date_check_digit': '3', 'sex': 'F', 'expiration_date': '370808', 'expiration_date_check_digit': '6', 'personal_number': '64U4CO5DC<<<<<<<<<', 'personal_number_check_digit': '8'}
        actual = MRTD.decodeMRZ(line1, line2)
        self.assertEqual(expected, actual)

        # Test 4 - Personal number shorter than 9 characters (remainder of 2)
        line1 = 'P<ALBFRANKLIN<<ARNOLD<SWOLE<<<<<<<<<<<<<<<<<<<<'
        line2 = 'MN6JC8BV39ALB4912251M09103180Q27L<<<<<<<<<<<<<2'
        expected = {'document_type': 'P', 'issuing_country': 'ALB', 'last_name': 'FRANKLIN', 'first_name': 'ARNOLD', 'middle_name': 'SWOLE', 'passport_number': 'MN6JC8BV3', 'passport_number_check_digit': '9', 'country_code': 'ALB', 'birth_date': '491225', 'birth_date_check_digit': '1', 'sex': 'M', 'expiration_date': '091031', 'expiration_date_check_digit': '8', 'personal_number': '0Q27L<<<<<<<<<<<<<', 'personal_number_check_digit': '2'}
        actual = MRTD.decodeMRZ(line1, line2)
        self.assertEqual(expected, actual)

        # Test 5 - Personal number shorter than 9 characters (remainder of 2)
        line1 = 'P<ALBFRANKLIN<<ARNOLD<SWOLE<<<<<<<<<<<<<<<<<<<<'
        line2 = 'MN6JC8BV39ALB4912251M0910318A9X<<<<<<<<<<<<<<<0'
        expected = {'document_type': 'P', 'issuing_country': 'ALB', 'last_name': 'FRANKLIN', 'first_name': 'ARNOLD', 'middle_name': 'SWOLE', 'passport_number': 'MN6JC8BV3', 'passport_number_check_digit': '9', 'country_code': 'ALB', 'birth_date': '491225', 'birth_date_check_digit': '1', 'sex': 'M', 'expiration_date': '091031', 'expiration_date_check_digit': '8', 'personal_number': 'A9X<<<<<<<<<<<<<<<', 'personal_number_check_digit': '0'}
        actual = MRTD.decodeMRZ(line1, line2)
        self.assertEqual(expected, actual)

        # Test 6 - Personal number shorter than 9 characters (remainder of 1)
        line1 = 'P<ALBFRANKLIN<<ARNOLD<SWOLE<<<<<<<<<<<<<<<<<<<<'
        line2 = 'MN6JC8BV39ALB4912251M0910318D07IAVT<<<<<<<<<<<8'
        expected = {'document_type': 'P', 'issuing_country': 'ALB', 'last_name': 'FRANKLIN', 'first_name': 'ARNOLD', 'middle_name': 'SWOLE', 'passport_number': 'MN6JC8BV3', 'passport_number_check_digit': '9', 'country_code': 'ALB', 'birth_date': '491225', 'birth_date_check_digit': '1', 'sex': 'M', 'expiration_date': '091031', 'expiration_date_check_digit': '8', 'personal_number': 'D07IAVT<<<<<<<<<<<', 'personal_number_check_digit': '8'}
        actual = MRTD.decodeMRZ(line1, line2)
        self.assertEqual(expected, actual)

        # Test 7 - Personal number longer than 9 characters (remainder of 1)
        line1 = 'P<ALBFRANKLIN<<ARNOLD<SWOLE<<<<<<<<<<<<<<<<<<<<'
        line2 = 'MN6JC8BV39ALB4912251M0910318FT8AO29BHY861<<<<<<2'
        expected = {'document_type': 'P', 'issuing_country': 'ALB', 'last_name': 'FRANKLIN', 'first_name': 'ARNOLD', 'middle_name': 'SWOLE', 'passport_number': 'MN6JC8BV3', 'passport_number_check_digit': '9', 'country_code': 'ALB', 'birth_date': '491225', 'birth_date_check_digit': '1', 'sex': 'M', 'expiration_date': '091031', 'expiration_date_check_digit': '8', 'personal_number': 'FT8AO29BHY861<<<<<<', 'personal_number_check_digit': '2'}
        actual = MRTD.decodeMRZ(line1, line2)
        self.assertEqual(expected, actual)

        # Test 8 - Personal number longer than 9 characters (remainder of 2)
        line1 = 'P<ALBFRANKLIN<<ARNOLD<SWOLE<<<<<<<<<<<<<<<<<<<<'
        line2 = 'MN6JC8BV39ALB4912251M0910318E9XLWPIW4GISGCT0<<3'
        expected = {'document_type': 'P', 'issuing_country': 'ALB', 'last_name': 'FRANKLIN', 'first_name': 'ARNOLD', 'middle_name': 'SWOLE', 'passport_number': 'MN6JC8BV3', 'passport_number_check_digit': '9', 'country_code': 'ALB', 'birth_date': '491225', 'birth_date_check_digit': '1', 'sex': 'M', 'expiration_date': '091031', 'expiration_date_check_digit': '8', 'personal_number': 'E9XLWPIW4GISGCT0<<', 'personal_number_check_digit': '3'}
        actual = MRTD.decodeMRZ(line1, line2)
        self.assertEqual(expected, actual)

        # Test 9 - Personal number max 18 characters
        line1 = 'P<ALBFRANKLIN<<ARNOLD<SWOLE<<<<<<<<<<<<<<<<<<<<'
        line2 = 'MN6JC8BV39ALB4912251M09103184UR757JNNONF8FLF3C1'
        expected = {'document_type': 'P', 'issuing_country': 'ALB', 'last_name': 'FRANKLIN', 'first_name': 'ARNOLD', 'middle_name': 'SWOLE', 'passport_number': 'MN6JC8BV3', 'passport_number_check_digit': '9', 'country_code': 'ALB', 'birth_date': '491225', 'birth_date_check_digit': '1', 'sex': 'M', 'expiration_date': '091031', 'expiration_date_check_digit': '8', 'personal_number': '4UR757JNNONF8FLF3C', 'personal_number_check_digit': '1'}
        actual = MRTD.decodeMRZ(line1, line2)
        self.assertEqual(expected, actual)
    
    @patch('MRTD.encodeTravelInfo')
    def test_encode_travel_info(self, mockedDBentry):
        # Test the encode_travel_info function
        # Test 1
        pass

    def test_checkMRZ(self):
        # Test the checkMRZ function
        # Test 1 -- all normal (full pass)
        traveler_info = {'document_type': 'P', 'issuing_country': 'ITA', 'last_name': 'PEPPERONI', 'first_name': 'JOHNNY', 'middle_name': 'DONNY', 'passport_number': '067FIKKXO', 'passport_number_check_digit': '7', 'country_code': 'ITA', 'birth_date': '840118', 'birth_date_check_digit': '6', 'sex': 'M', 'expiration_date': '921104', 'expiration_date_check_digit': '1', 'personal_number': 'T8W3UK289<<<<<<<<<', 'personal_number_check_digit': '7'}
        expected = {'Passport Number': 'Passed', 'Birth Date': 'Passed', 'Expiration Date': 'Passed', 'Personal Number': 'Passed'}
        actual = MRTD.checkMRZ(traveler_info)
        self.assertEqual(expected, actual)

        # Test 2 -- incorrect passport check
        traveler_info = {'document_type': 'P', 'issuing_country': 'ITA', 'last_name': 'PEPPERONI', 'first_name': 'JOHNNY', 'middle_name': 'DONNY', 'passport_number': '067FIKKXO', 'passport_number_check_digit': '9', 'country_code': 'ITA', 'birth_date': '840118', 'birth_date_check_digit': '6', 'sex': 'M', 'expiration_date': '921104', 'expiration_date_check_digit': '1', 'personal_number': 'T8W3UK289<<<<<<<<<', 'personal_number_check_digit': '7'}
        expected = {'Passport Number': 'Failed', 'Birth Date': 'Passed', 'Expiration Date': 'Passed', 'Personal Number': 'Passed'}
        actual = MRTD.checkMRZ(traveler_info)
        self.assertEqual(expected, actual)

        # Test 3 -- incorrect birth date check
        traveler_info = {'document_type': 'P', 'issuing_country': 'ITA', 'last_name': 'PEPPERONI', 'first_name': 'JOHNNY', 'middle_name': 'DONNY', 'passport_number': '067FIKKXO', 'passport_number_check_digit': '7', 'country_code': 'ITA', 'birth_date': '840118', 'birth_date_check_digit': '1', 'sex': 'M', 'expiration_date': '921104', 'expiration_date_check_digit': '1', 'personal_number': 'T8W3UK289<<<<<<<<<', 'personal_number_check_digit': '7'}
        expected = {'Passport Number': 'Passed', 'Birth Date': 'Failed', 'Expiration Date': 'Passed', 'Personal Number': 'Passed'}
        actual = MRTD.checkMRZ(traveler_info)
        self.assertEqual(expected, actual)

        # Test 4 -- incorrect expiration date check
        traveler_info = {'document_type': 'P', 'issuing_country': 'ITA', 'last_name': 'PEPPERONI', 'first_name': 'JOHNNY', 'middle_name': 'DONNY', 'passport_number': '067FIKKXO', 'passport_number_check_digit': '7', 'country_code': 'ITA', 'birth_date': '840118', 'birth_date_check_digit': '6', 'sex': 'M', 'expiration_date': '921104', 'expiration_date_check_digit': '4', 'personal_number': 'T8W3UK289<<<<<<<<<', 'personal_number_check_digit': '7'}
        expected = {'Passport Number': 'Passed', 'Birth Date': 'Passed', 'Expiration Date': 'Failed', 'Personal Number': 'Passed'}
        actual = MRTD.checkMRZ(traveler_info)
        self.assertEqual(expected, actual)

        # Test 5 -- incorrect personal number check
        traveler_info = {'document_type': 'P', 'issuing_country': 'ITA', 'last_name': 'PEPPERONI', 'first_name': 'JOHNNY', 'middle_name': 'DONNY', 'passport_number': '067FIKKXO', 'passport_number_check_digit': '7', 'country_code': 'ITA', 'birth_date': '840118', 'birth_date_check_digit': '6', 'sex': 'M', 'expiration_date': '921104', 'expiration_date_check_digit': '1', 'personal_number': 'T8W3UK289<<<<<<<<<', 'personal_number_check_digit': '0'}
        expected = {'Passport Number': 'Passed', 'Birth Date': 'Passed', 'Expiration Date': 'Passed', 'Personal Number': 'Failed'}
        actual = MRTD.checkMRZ(traveler_info)
        self.assertEqual(expected, actual)

        # Test 6 -- incorrect passport and birth date check
        traveler_info = {'document_type': 'P', 'issuing_country': 'ITA', 'last_name': 'PEPPERONI', 'first_name': 'JOHNNY', 'middle_name': 'DONNY', 'passport_number': '067FIKKXO', 'passport_number_check_digit': '3', 'country_code': 'ITA', 'birth_date': '840118', 'birth_date_check_digit': '8', 'sex': 'M', 'expiration_date': '921104', 'expiration_date_check_digit': '1', 'personal_number': 'T8W3UK289<<<<<<<<<', 'personal_number_check_digit': '7'}
        expected = {'Passport Number': 'Failed', 'Birth Date': 'Failed', 'Expiration Date': 'Passed', 'Personal Number': 'Passed'}
        actual = MRTD.checkMRZ(traveler_info)
        self.assertEqual(expected, actual)

        # Test 7 -- incorrect passport and expiration date check
        traveler_info = {'document_type': 'P', 'issuing_country': 'ITA', 'last_name': 'PEPPERONI', 'first_name': 'JOHNNY', 'middle_name': 'DONNY', 'passport_number': '067FIKKXO', 'passport_number_check_digit': '5', 'country_code': 'ITA', 'birth_date': '840118', 'birth_date_check_digit': '6', 'sex': 'M', 'expiration_date': '921104', 'expiration_date_check_digit': '9', 'personal_number': 'T8W3UK289<<<<<<<<<', 'personal_number_check_digit': '7'}
        expected = {'Passport Number': 'Failed', 'Birth Date': 'Passed', 'Expiration Date': 'Failed', 'Personal Number': 'Passed'}
        actual = MRTD.checkMRZ(traveler_info)
        self.assertEqual(expected, actual)

        # Test 8 -- incorrect passport, birth date, and personal number check
        traveler_info = {'document_type': 'P', 'issuing_country': 'ITA', 'last_name': 'PEPPERONI', 'first_name': 'JOHNNY', 'middle_name': 'DONNY', 'passport_number': '067FIKKXO', 'passport_number_check_digit': '1', 'country_code': 'ITA', 'birth_date': '840118', 'birth_date_check_digit': '1', 'sex': 'M', 'expiration_date': '921104', 'expiration_date_check_digit': '1', 'personal_number': 'T8W3UK289<<<<<<<<<', 'personal_number_check_digit': '1'}
        expected = {'Passport Number': 'Failed', 'Birth Date': 'Failed', 'Expiration Date': 'Passed', 'Personal Number': 'Failed'}
        actual = MRTD.checkMRZ(traveler_info)
        self.assertEqual(expected, actual)

        # Test 9 -- all checks failed
        traveler_info = {'document_type': 'P', 'issuing_country': 'ITA', 'last_name': 'PEPPERONI', 'first_name': 'JOHNNY', 'middle_name': 'DONNY', 'passport_number': '067FIKKXO', 'passport_number_check_digit': '4', 'country_code': 'ITA', 'birth_date': '840118', 'birth_date_check_digit': '2', 'sex': 'M', 'expiration_date': '921104', 'expiration_date_check_digit': '7', 'personal_number': 'T8W3UK289<<<<<<<<<', 'personal_number_check_digit': '4'}
        expected = {'Passport Number': 'Failed', 'Birth Date': 'Failed', 'Expiration Date': 'Failed', 'Personal Number': 'Failed'}
        actual = MRTD.checkMRZ(traveler_info)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()