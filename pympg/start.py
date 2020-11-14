import os


initPrm = (
    input(
        "- For port forwarding, type 'proxy'. Examples include express.js and webmin.\n\n- For services located in a webroot, type 'webroot'. [webroot] \n> "
    ).lower()
    or "webroot"
)

APACHE_LOG_DIR = "{APACHE_LOG_DIR}"


def proxyConf():
    if not "." in domainPrm:
        print("Not a valid domain.")
    f = open(f"{domainPrm}.conf", "w")
    f.write(
        f"<VirtualHost *:80>\nServerName {domainPrm}\n{serverAlias}\nProxyPass / http://localhost:{portForForward}/\nProxyPassReverse / http://localhost:{portForForward}/\n</VirtualHost>"
    )
    f.close()
    os.system(f"sudo cp {domainPrm}.conf {apcPa}/sites-enabled/{domainPrm}.conf")


def regConf():
    if not "." in domainPrm:
        print("Not a valid domain.")
    f = open(f"{domainPrm}.conf", "w")
    f.write(
        f"<VirtualHost *:80>\nServerName {domainPrm}\n{serverAlias}\nDocumentRoot {webLoc}\nErrorLog ${APACHE_LOG_DIR}/error.log\nCustomLog ${APACHE_LOG_DIR}/access.log combined\n</VirtualHost>"
    )
    f.close()
    os.system(f"sudo cp {domainPrm}.conf {apcPa}/sites-enabled/{domainPrm}.conf")


# Domain setup
domainAnswer = (
    input("What are your domain names? [example.com] \n> ").lower() or "example.com"
)
domainAnswer = domainAnswer.split(",")
domainPrm = domainAnswer[0]
serverAlias = "".join(list(map(lambda d: f"{d} ", domainAnswer[1:])))
if serverAlias:
    serverAlias = "ServerAlias " + serverAlias
if initPrm == "proxy":
    portForForward = (
        input("Please enter the port you wish to forward [8080] \n> ") or "8080"
    )
    apcPa = (
        input("Where is your Apache installation located? [/etc/apache2/] \n> ")
        or "/etc/apache2"
    )
    proxyConf()
elif initPrm == "webroot":
    webLoc = (
        input("What is the absolute path of the files for your website?\n> ")
        or "/var/www/html"
    )
    apcPa = (
        input("Where is your Apache installation located? [/etc/apache2/] \n> ")
        or "/etc/apache2"
    )
    regConf()
else:
    print("Not a valid option.")
    exit(0)

restart = (
    input("Would you like to reload the configuration now? [n] \n> ").lower() or "n"
)
if restart == "y" or restart == "yes":
    os.system("sudo apachectl -k graceful")
exit(0)
