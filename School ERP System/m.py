from time import ctime
def month():
    date=ctime().split()
    m_=date[1]
    if m_=='Jan':
        return '01'
    elif m_=='Feb':
        return '02'
    elif m_=='Mar':
        return '03'
    elif m_=='Apr':
        return '04'
    elif m_=='May':
        return '05'
    elif m_=='Jun':
        return '06'
    elif m_=='Jul':
        return '07'
    elif m_=='Aug':
        return '08'
    if m_=='Sep':
        return '09'
    if m_=='Oct':
        return '10'
    if m_=='Nov':
        return '11'
    if m_=='Dec':
        return '12'
def month_():
    mon=month()
    return mon
