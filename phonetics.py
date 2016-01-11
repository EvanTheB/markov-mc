# -*- coding: utf-8 -*-

"
This code taken from http://mining4meaning.com/2015/02/13/raplyzer/
Raplyzer
https://github.com/ekQ/raplysaattori

The MIT License (MIT)

Copyright (c) 2014 ekQ

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"
"

import os
import codecs
import re

'''
This file contains all phonetics related functions. The phonetic
transcription is obtained using eSpeak speech synthesizer
(http://espeak.sourceforge.net/).

For English the list of available phonetic vowels can be found here:
    http://espeak.sourceforge.net/phonemes.html
'''

def is_vow(c, language='en'):
    '''
    Is the given (lowercase) character a vowel or not.
    '''
    if language == 'fi': # Finnish
        return c in u'aeiouyäöå'

    elif len(language) >= 2 and language[:2] == 'en': # English
        # In order to increase recall for the rhyme detection, we 
        # ignore the schwa vowel '@' as it can be rhymed with several
        # different vowels. However, in BattleBot we do not ignore it
        # in order to get a higher precision.
        return c in u'3L5aAeEiI0VuUoO@'

    else:
        raise Exception("Unknown language: %s" % language)

def map_vow(c, language):
    '''
    Map vowel to a similar sounding vowel (only for English).
    '''
    # This list is somewhat arbitrary, so some native English speaker 
    # who knows about phonetics might be able to improve it.
    vow_map = {
            '0':'o',
            'O':'o',
            'I':'i',
            'E':'e'
            }
    if len(language) >= 2 and language[:2] == 'en' and c in vow_map:
        return vow_map[c]
    else:
        return c

def is_space(c):
    '''
    Is the given character a space or newline (other space characters are 
    cleaned in the preprocessing phase).
    '''
    return c==' ' or c=='\n'

def get_phonetic_transcription(text, language='en-us', output_fname=None):
    if output_fname is None:
        fname2 = u'temp_transcription.txt'
    else:
        fname2 = output_fname

    if output_fname is None or not os.path.exists(fname2):
        fname = u'temp_lyrics.txt'
        f = codecs.open(fname, 'w', 'utf8')
        f.write(text)
        f.close()

        cmd = u'espeak -xq -v%s -f %s > %s' % (language, fname, fname2)
        os.system(cmd)

    f2 = codecs.open(fname2, 'r', 'utf8')
    new_text = f2.read()

    # Remove some unwanted stuff from the transcription
    new_text = re.sub("_:'Ekskl@m,eIS@n_:", "", new_text)
    new_text = re.sub("'", "", new_text)
    new_text = re.sub(",", "", new_text)
    return new_text
