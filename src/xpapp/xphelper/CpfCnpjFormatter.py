

class CpfCnpjFormatter:

    @staticmethod
    def format_to_cpf(number):
        cpf = "{:011}".format(number)
        formatted_cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return formatted_cpf

    @staticmethod
    def format_to_cnpj(number):
        cnpj = "{:014}".format(number)
        formatted_cnpj = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
        return formatted_cnpj
    @staticmethod
    def validar( num_str):
        teste1 = str(num_str).zfill(14)

        if teste1[8:12] == "0001":
            return "CNPJ"
        else:
            return "CPF"

    @staticmethod
    def formatar(number):
        validacao = CpfCnpjFormatter.validar(number)
        if validacao == 'CNPJ':
            return CpfCnpjFormatter.format_to_cnpj(str(number).zfill(14))
        else:
            return CpfCnpjFormatter.format_to_cpf(str(number).zfill(11))