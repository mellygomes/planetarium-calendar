import calendar

class CalendarioAnual:
    def __init__(self, ano):
        self.ano =  ano

    def getNumberOfDays(self, mes):
        return calendar.monthrange(mes)

    def getWeekdayOfDay1th(self, mes):
        return calendar.weekday(self.ano, mes, 1)