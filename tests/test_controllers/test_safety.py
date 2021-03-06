# project
from dephell.controllers import Safety


def test_safety():
    safety = Safety()
    vulns = safety.get('django', '1.11.0')
    assert len(vulns) == 5
    assert {vuln.name for vuln in vulns} == {'django'}
