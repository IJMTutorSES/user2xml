from email.utils import parseaddr
from data_reader import Data
import re
import os

class Id:
    def __init__(self, s):
        self.s = s

    def __call__(self, k):
        if n := Data.REFIDS[k][1]:
            return n
        else:
            Data.REFIDS[k][1] = self.s
            self.s += 1
            return self.s - 1


ID = Id(3)

_user_vorlage = (
    lambda fname, lname, email, gender, kurs, sdate, edate, user, pw: f"""
<User Id="{user.upper()}" Language="de" Action="Insert">
  <Active><![CDATA[true]]></Active>
  <Role Id="_1" Type="Global" Action="Assign"><![CDATA[User]]></Role>
  <Role Id="_2" Type="Local" Action="Assign"><![CDATA[il_crs_member_37553]]></Role>
{"".join([f'''  <Role Id="_{ID(k)}" Type="Local" Action="Assign"><![CDATA[il_crs_member_{Data.REFIDS[k][0]}]]></Role>
''' for k in kurs])}
  <Login><![CDATA[{user.upper()}]]></Login>
  <Password Type="PLAIN">{pw}</Password>
  <Gender><![CDATA[{gender}]]></Gender>
  <Firstname><![CDATA[{fname}]]></Firstname>
  <Lastname><![CDATA[{lname}]]></Lastname>
  <Email><![CDATA[{email}]]></Email>
  <TimeLimitUnlimited><![CDATA[{0 if edate != "" else 1}]]></TimeLimitUnlimited>
  {f"<TimeLimitFrom><![CDATA[{'-'.join(sdate.split('-')[::-1])} 00:00:00]]></TimeLimitFrom>" if edate else ""}
  {f"<TimeLimitUntil><![CDATA[{'-'.join(['20' + b if i == 0 and len(b) == 2 else b for i, b in enumerate(edate.split('-')[::-1])])} 23:59:59]]></TimeLimitUntil>" if edate else ""}
 </User>
"""
)


def validate(vals):
    if not re.match("^[\\w\\- ]+$", vals["fname"]):
        return "Vorname"
    if not re.match("^[\\w\\- ]+$", vals["lname"]):
        return "Nachname"
    if not parseaddr(vals["email"])[1]:
        return "E-Mail"
    if vals["gender"] == "Herr":
        gender = "m"
    elif vals["gender"] == "Frau":
        gender = "f"
    elif vals["gender"] == "Keine Angabe":
        gender = "n"
    kurs = []
    for cat in Data.CATEGORIES:
        kurs.extend(vals[cat])
    if not re.match("^\\d{2}-\\d{2}-\\d{2}|\\d{4}$", vals["sdate"]):
        return "Startdatum"
    if vals["edate"]:
        if not re.match("^\\d{2}-\\d{2}-(\\d{2}$|\\d{4}$)", vals["edate"]):
            return "Enddatum"
    return (gender, kurs)


def export(vals, prop, login, sess):
    if not os.path.exists(f"user_import_{sess}.xml"):
        buffer = '<?xml version="1.0" encoding="UTF-16LE"?>\n<Users>'
    else:
        buffer = ""
    buffer += _user_vorlage(
        vals["fname"],
        vals["lname"],
        vals["email"],
        prop[0],
        prop[1],
        vals["sdate"],
        vals["edate"],
        login[0].upper(),
        login[1],
    )
    with open(f"user_import_{sess}.xml", "a", encoding="UTF-16LE") as file:
        file.write(buffer)


def end_file(sess):
    if os.path.exists(f"user_import_{sess}.xml"):
        with open(f"user_import_{sess}.xml", "a", encoding="UTF-16LE") as file:
            file.write("\n</Users>")

