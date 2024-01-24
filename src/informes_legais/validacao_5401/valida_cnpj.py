import re


class ValidarCnpj():

    def is_valid_cnpj(self, cnpj):
        # Remove non-digit characters
        cnpj = re.sub(r'\D', '', cnpj)

        # Check if the length is 14 characters
        if len(cnpj) != 14:
            return False

        # Check if all characters are the same
        if cnpj == cnpj[0] * 14:
            return False

        # Calculate the first verification digit
        total = 0
        weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        for i in range(12):
            total += int(cnpj[i]) * weights[i]
        remainder = total % 11
        digit1 = 0 if remainder < 2 else 11 - remainder

        # Calculate the second verification digit
        total = 0
        weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        for i in range(13):
            total += int(cnpj[i]) * weights[i]
        remainder = total % 11
        digit2 = 0 if remainder < 2 else 11 - remainder

        # Check if the calculated digits match the provided ones
        return int(cnpj[12]) == digit1 and int(cnpj[13]) == digit2

    # Example usage:

    def validar_cnpj(self, cnpj_to_check):

        result = self.is_valid_cnpj(cnpj_to_check)

        if result:
            return True
        else:
            return False

