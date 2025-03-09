import requests
import re
from bs4 import BeautifulSoup

login_url = "https://erp.campus-dual.de/sap/bc/webdynpro/sap/zba_initss?sap-client=100&sap-language=de&uri=https%3a%2f%2fselfservice.campus-dual.de%2findex%2flogin"

session = requests.Session()

# Initial request to get the login page
init_response = session.get(login_url)
if init_response.status_code != 200:
    raise Exception("Failed to initialize the login session")

# Parse the response and get the XSRF token
soup = BeautifulSoup(init_response.text, "html.parser")
# Get the XSRF token. Hint: The token hides in a hidden input field
xsrf_token = soup.find("input", {"name": "sap-login-XSRF"})["value"]
if xsrf_token is None:
    raise Exception("Failed to get the XSRF token")

# print(xsrf_token)

login_data = {
    "FOCUS_ID": "sap-user",
    "sap-system-login-oninputprocessing": "onLogin",
    "sap-urlscheme": "",
    "sap-system-login": "onLogin",
    "sap-system-login-basic_auth": "",
    "sap-client": "100",
    "sap-language": "DE",
    "sap-accessibility": "",
    "sap-login-XSRF": xsrf_token,
    "sap-system-login-cookie_disabled": "",
    "sap-user": input("Deine Matrikelnummer: "),
    "sap-password": input("Dein CampusDual Passwort: "),
    "SAPEVENTQUEUE": "Form_Submit~E002Id~E004SL__FORM~E003~E002ClientAction~E004submit~E005ActionUrl~E004~E005ResponseData~E004full~E005PrepareScript~E004~E003~E002~E003",
}

login_response = session.post(login_url, data=login_data)
# Check if login was successful by looking for the MYSAPSSO2 cookie
if "MYSAPSSO2" in session.cookies:
    mysapsso2_cookie = session.cookies["MYSAPSSO2"]
    # print("MYSAPSSO2 cookie:", mysapsso2_cookie)
else:
    raise Exception("Failed to retrieve MYSAPSSO2 cookie")


response = session.get("https://selfservice.campus-dual.de/index/login", verify=False)
if response.status_code != 200:
    raise Exception("Failed to retrieve the page")

html = response.text
soup = BeautifulSoup(html, "html.parser")
script_tag = soup.select_one("#main script")

if script_tag:
    script_content = script_tag.string
    hash_regexp = re.compile(r'hash="([^"]*)"')
    match = hash_regexp.search(script_content)

    if match:
        hash_value = match.group(1)
        print(f"\033[92m{hash_value}\033[0m")
    else:
        raise Exception("Failed to scrape hash")
else:
    raise Exception("Failed to scrape hash")
