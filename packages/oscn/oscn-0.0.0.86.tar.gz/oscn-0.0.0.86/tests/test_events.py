import oscn


def test_entries():
    case = oscn.request.Case("tulsa-FD-2022-945")    
    events = case.events
    first = events[0]
    # {'date': 'Wednesday, May 25, 2022 at 9:30 AM', 'description': 'Parenting Plan Conference'},
    assert first['date'] == 'Wednesday, May 25, 2022 at 9:30 AM'
    assert first['description'] == 'Parenting Plan Conference'
    
