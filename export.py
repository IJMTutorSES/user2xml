from email.utils import parseaddr
import re
import os

REFIDS = {
    "Klasse 4+5": [2281, 0],
    "Klasse 6+7": [15389, 0],
    "Klasse 8+9": [15391, 0],
    "Klasse 10+11": [11261, 0],
    "Analysis (Abitur)": [6068, 0],
    "Algebra (Abitur)": [11393, 0],
    "Japanisch": [25548, 0],
    "Arabisch": [25574, 0],
    "Chinesisch": [25578, 0],
    "Deutsch": [25580, 0],
    "Englisch (AE)": [25540, 0],
    "Englisch (BE)": [25542, 0],
    "Französisch": [25544, 0],
    "Griechisch": [25552, 0],
    "Hebräisch": [25588, 0],
    "Hindi": [25572, 0],
    "Irisch": [25576, 0],
    "Italiensich": [25546, 0],
    "Koreanisch": [25570, 0],
    "Latein": [25550, 0],
    "Niederländisch": [25562, 0],
    "Persisch": [25586, 0],
    "Philippinisch": [25568, 0],
    "Polnisch": [25564, 0],
    "Portugiesisch": [25566, 0],
    "Russisch": [25558, 0],
    "Schwedisch": [25582, 0],
    "Spanisch (Lateinamerika)": [25556, 0],
    "Spanisch (Spanien)": [25554, 0],
    "Türkisch": [25560, 0],
    "Vietnamesisch": [25584, 0],
    "Robotik Smarttech": [43045, 0],
    "Robotik und Coding": [41646, 0],
    "Technik und Statik": [42125, 0],
    "Physik": [7507, 0],
    "Biologie": [9799, 0],
    "Human-Medizin": [5310, 0],
    "Chemie": [40880, 0],
    "Finanzwesen": [15378, 0],
    "BWL": [40594, 0],
    "Volkswirtschaft": [11740, 0],
}


class Id:
    def __init__(self, s):
        self.s = s

    def __call__(self, k):
        if n := REFIDS[k][1]:
            return n
        else:
            REFIDS[k][1] = self.s
            self.s += 1
            return self.s - 1


ID = Id(3)

_user_vorlage = (
    lambda fname, lname, email, gender, kurs, sdate, edate, user, pw: f"""
<User Id="{user.upper()}" Language="de" Action="Insert">
  <Active><![CDATA[true]]></Active>
  <Role Id="_1" Type="Global" Action="Assign"><![CDATA[User]]></Role>
  <Role Id="_2" Type="Local" Action="Assign"><![CDATA[il_crs_member_37553]]></Role>
{"".join([f'''  <Role Id="_{ID(k)}" Type="Local" Action="Assign"><![CDATA[il_crs_member_{REFIDS[k][0]}]]></Role>
''' for k in kurs])}
  <Login><![CDATA[{user.upper()}]]></Login>
  <Password Type="PLAIN">{pw}</Password>
  <Gender><![CDATA[{gender}]]></Gender>
  <Firstname><![CDATA[{fname}]]></Firstname>
  <Lastname><![CDATA[{lname}]]></Lastname>
  <Email><![CDATA[{email}]]></Email>
  <TimeLimitUnlimited><![CDATA[{0 if edate != "" else 1}]]></TimeLimitUnlimited>
  {f"<TimeLimitFrom><![CDATA[{sdate} 00:00:00]]></TimeLimitFrom>" if edate else ""}
  {f"<TimeLimitUntil><![CDATA[{edate} 23:59:59]]></TimeLimitUntil>" if edate else ""}
 </User>
"""
)


def validate(vals):
    if not re.match("^\\w+$", vals["fname"]):
        return "Vorname"
    if not re.match("^\\w+$", vals["lname"]):
        return "Nachname"
    if not parseaddr(vals["email"])[1]:
        return "E-Mail"
    if vals["gender"] == "Herr":
        gender = "m"
    elif vals["gender"] == "Frau":
        gender = "f"
    elif vals["gender"] == "Keine Angabe":
        gender = "n"
    kurs = vals["math"] + vals["lang"] + vals["stip"] + vals["prop"]
    if not re.match("^\\d{4}-\\d{2}-\\d{2}$", vals["sdate"]):
        return "Startdatum"
    if not re.match("^\\d{4}-\\d{2}-\\d{2}", vals["edate"]):
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
