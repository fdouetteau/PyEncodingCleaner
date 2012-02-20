
import re
import sys
    
map_table = {}

"""
Small utility that tries to fix automatically  some common encoding errors.
 
"""

def get_map_table(destinationCharset, sourceCharset):
    table_key = destinationCharset + ":" + sourceCharset 
    if table_key in map_table: 
        return map_table[table_key]
    m = {}
    for k in xrange(97, 256):
        sk = unichr(k)
        enc_sk = sk.encode(destinationCharset).decode(sourceCharset)
        if sk != enc_sk: 
            m[enc_sk] = sk  
    rc = re.compile(u'|'.join(map(re.escape, m)))
    map_table[table_key] = (rc, m)
    return (rc, m)
    
def cleanup_overencoded_string(s, destinationCharset="utf8", sourceCharset="latin1"): 
    """
    Cleanup a string where character have been encoded twice
        destinationCharset:  the charset the string should have
        sourceCharset : the original charset from the input data, from which bad (overencoding) might have been done.
    """
    (rc, m) = get_map_table(destinationCharset, sourceCharset) 
    if isinstance(s, unicode): 
        return rc.sub(lambda g: m[g.group(0)], s)
    else:        
         u = unicode(s, destinationCharset)
         tu = rc.sub(lambda g: m[g.group(0)], u)
         return tu.encode(destinationCharset)
         
if __name__ == "__main__":
    for line in sys.stdin:
        print cleanup_overencoded_string(line)