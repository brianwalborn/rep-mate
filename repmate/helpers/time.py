from datetime import datetime

class Time:
  @staticmethod
  def format(time) -> str:
    return datetime.strftime(time, '%m/%d/%Y %H:%M:%S %Z')
