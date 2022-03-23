from datetime import datetime, date

class Date:
    def __init__(self, date: str) -> None:
        self.date = datetime.fromisoformat(date)
        self.date_now = datetime.now()
        
        self.list_date = self.get_list_date(self.date)
        self.list_date_now = self.get_list_date(self.date_now)
        
    def get_list_date(self, date: datetime):
        return [date.day, date.month, date.year]
    
    def list_zip(self, iter_1: list, iter_2: list):
        return list(zip(iter_1, iter_2))
    
    def __join_dates(self):
        return self.list_zip(self.list_date_now, self.list_date)
    
    def verify_date(self):
        return any([i > j for i,j in self.__join_dates()])
    
    def days_passed(self):
        past = date(*reversed(self.list_date))
        today = date(*reversed(self.list_date_now))
        return (today-past).days