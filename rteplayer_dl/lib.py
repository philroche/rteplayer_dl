# -*- coding: utf-8 -*-


def findnth(haystack, needle, n):
    '''
    Find the nth occurrence of one string in another
    '''
    parts = haystack.split(needle, n+1)
    if len(parts) <= n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)
