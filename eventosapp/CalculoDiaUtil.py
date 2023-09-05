from bizdays import Calendar
from datetime import date


class CalculoDiaUtil():
    cal = Calendar.load('ANBIMA')

    def __init__(self, data):
        self.data = data.strftime("%Y-%m-%d")
        self.day = data.day
        self.month = data.month
        self.year = data.year

    def calculodia_util(self, dia):
        return self.cal.getdate(dia, self.year, self.month)

    def get_dias_uteis(self):
        dias_uteis = {
            "primeiro_dia_util": self.calculodia_util('1th bizday'),
            "quinto": self.calculodia_util('5th bizday'),
            "decimo": self.calculodia_util('10th bizday'),
            "decimo_quinto": self.calculodia_util('15th bizday'),
            "vigesimo": self.calculodia_util('20th bizday')
        }
        return dias_uteis

    def calculardiautil(self):
        primeiro_dia_do_mes = date(self.year, self.month, 1).strftime("%Y-%m-%d")

        return self.cal.bizdays(primeiro_dia_do_mes, self.data) + 1


data = date.today()

util = CalculoDiaUtil(data)

