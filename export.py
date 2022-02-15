from email.utils import parseaddr
import re
import os

REFIDS = {
    "Klasse 4+5": 2281,
    "Klasse 6+7": 15389,
    "Klasse 8+9": 15391,
    "Klasse 10+11": 11261,
    "Analysis (Abitur)": 6068,
    "Algebra (Abitur)": 11393,
    "Japanisch": 25548,
    "Arabisch": 25574,
    "Chinesisch": 25578,
    "Deutsch": 25580,
    "Englisch (AE)": 25540,
    "Englisch (BE)": 25542,
    "Französisch": 25544,
    "Griechisch": 25552,
    "Hebräisch": 25588,
    "Hindi": 25572,
    "Irisch": 25576,
    "Italiensich": 25546,
    "Koreanisch": 25570,
    "Latein": 25550,
    "Niederländisch": 25562,
    "Persisch": 25586,
    "Philippinisch": 25568,
    "Polnisch": 25564,
    "Portugiesisch": 25566,
    "Russisch": 25558,
    "Schwedisch": 25582,
    "Spanisch (Lateinamerika)": 25556,
    "Spanisch (Spanien)": 25554,
    "Türkisch": 25560,
    "Vietnamesisch": 25584,
    "Robotik Smarttech": 43045,
    "Robotik und Coding": 41646,
    "Technik und Statik": 42125,
    "Physik": 7507,
    "Biologie": 9799,
    "Human-Medizin": 5310,
    "Chemie": 40880,
    "Finanzwesen": 15378,
    "BWL": 40594,
    "Volkswirtschaft": 11740,
}

_user_vorlage = (
    lambda fname, lname, email, gender, kurs, sdate, edate, user, pw: f"""
<User Id="{user.upper()}" Language="de" Action="Insert">
  <Active><![CDATA[true]]></Active>
  <Role Id="_1" Type="Global" Action="Assign"><![CDATA[User]]></Role>
  <Role Id="_2" Type="Local" Action="Assign"><![CDATA[il_crs_member_37553]]></Role>
{"".join([f'''  <Role Id="_{i+3}" Type="Local" Action="Assign"><![CDATA[il_crs_member_{n}]]></Role>
''' for i,n in enumerate(kurs)])}
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
    kurs = []
    for val in vals["math"]:
        kurs.append(REFIDS[val])
    for val in vals["lang"]:
        kurs.append(REFIDS[val])
    for val in vals["stip"]:
        kurs.append(REFIDS[val])
    for val in vals["prop"]:
        kurs.append(REFIDS[val])
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
