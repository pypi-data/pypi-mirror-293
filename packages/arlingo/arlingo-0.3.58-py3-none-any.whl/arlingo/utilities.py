import requests
from bs4 import BeautifulSoup
from easygoogletranslate import EasyGoogleTranslate
from pydub import AudioSegment
from gtts import gTTS
from io import BytesIO
import time
import clipboard
import string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

"""
The latest version of Google Chrome is needed for the Selenium to work.
Get the chromedriver from here: https://googlechromelabs.github.io/chrome-for-testing/#stable
A zip file will be downloaded. Extract the file and put the chromedriver.exe in your desired directory.
"""

class Conjugator:
    
    def __init__(self):
        pass
    
    def retrieve_page(self):
        if self.lang in ['fr', 'de']:
            try:
                self.page = requests.get(f"https://dic.b-amooz.com/{self.lang}/dictionary/conjugation/v?verb={self.verb}")
                self.page = BeautifulSoup(self.page.content, 'html.parser')
            except:
                raise ValueError("Failed to get the page. Please try again later.")
            self.conjugation_tables = self.page.find_all('table', class_='conjugation-table')
        elif self.lang == 'ko':
            try:
                self.chromedriver_path
            except:
                raise ValueError("Please provide the path to the chromedriver.")
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            cService = webdriver.ChromeService(executable_path=self.chromedriver_path)
            driver = webdriver.Chrome(service = cService, options=chrome_options)
            driver.get(f"https://www.verbix.com/webverbix/korean/{self.verb}")
            self.page = BeautifulSoup(driver.page_source, 'html.parser')
        else:
            raise NotImplementedError("Only French, Korean and German are supported at the moment.")
        
    def get_conjugation(self, verb, tense='present', lang='fr', **kwargs):
        self.verb = verb[:]
        self.tense = tense
        self.lang = lang
        if 'chromedriver_path' in kwargs:
            self.chromedriver_path = kwargs['chromedriver_path']
        self.retrieve_page()
        if self.lang in ['fr', 'de']:
            if self.tense == 'present':
                self.conjugations_object = self.conjugation_tables[0]
            else:
                raise NotImplementedError("Only present tense is supported at the moment.")
            pronouns = [span.text.strip() for span in self.conjugations_object.find_all('span')][0::2]
            verbs = [span.text.strip() for span in self.conjugations_object.find_all('span')][1::2]
            conjugation_lst = [pronoun + " " + verb for pronoun, verb in zip(pronouns, verbs)]
            self.pronouns = pronouns
            self.verbs = verbs
            return conjugation_lst
        elif self.lang == 'ko':
            times = ['حال خبری', 'گذشته خبری',
                        'آینده خبری', 'حال پرسشی',
                        'گذشته پرسشی', 'امری',
                        'پیشنهادی', 'متفرقه']
            pronoun_to_persian = {
                'informal low': 'غیر رسمی کم‌احترام',
                'informal high': 'غیر رسمی پراحترام',
                'formal low': 'رسمی کم‌احترام',
                'formal high': 'رسمی پراحترام',
                'past base': 'گذشته پایه',
                'future base': 'آینده پایه',
                'conditional informal low': 'شرطی غیر رسمی کم‌احترام',
                'conditional informal high': 'شرطی غیر رسمی پراحترام',
                'conditional formal low': 'شرطی رسمی کم‌احترام',
                'conditional formal high': 'شرطی رسمی پراحترام',
                'present informal low': 'حال غیر رسمی کم‌احترام',
                'present informal high': 'حال غیر رسمی پراحترام',
                'present formal low': 'حال رسمی کم‌احترام',
                'present formal high': 'حال رسمی پراحترام',
                'connective if': 'پیوند شرطی',
                'connective and': 'پیوند و',
                'nominal ing': 'مصدر ing',
            }
            self.conjugations = dict()
            parts = [item for item in self.page.findAll('table', {'class': 'verbtense'}) if 'nospeech' not in item.get('class')]
            for part, time in zip(parts, times):
                curr_pronouns = [item.text.strip() for item in part.findAll('span', {'class':'pronoun'})]
                curr_verbs = [item.text.strip() for item in part.findAll('span') if item.get('class')==['orto'] or item.get('class')==['normal']]
                self.conjugations[time] = {pronoun_to_persian[pronoun]: verb for pronoun, verb in zip(curr_pronouns, curr_verbs)}
            return self.conjugations
        else:
            raise NotImplementedError("Only French and German are supported at the moment.")


class WordExplorer:
    
    def __init__(self):
        pass
    
    def explore(self, word, lang='fr'):
        self.word = word
        self.lang = lang
        if self.lang in ['fr', 'de']:
            try:     
                page = requests.get(f"https://dic.b-amooz.com/{self.lang}/dictionary/w?word={self.word}")
                page = BeautifulSoup(page.content, 'html.parser')
            except:
                raise ValueError("Failed to get the page. Please try again later.")
            try:
                self.part_of_speech = page.find_all('span', class_='part-of-speech')[0].text.replace('[','').replace(']','').strip()
                if self.part_of_speech == 'اسم':
                    target_divider = page.find_all('div', class_='attr-noun')[0]
                    features_span = target_divider.find_all('span')
                    features = [span.text.strip() for span in features_span]
                    self.gender = 'خنثی' if 'خنثی' in features else ('مذکر' if 'مذکر' in features else 'مونث')
                else:
                    self.gender = None
            except:
                self.part_of_speech = ' '
                self.gender = ' '
        else:
            raise NotImplementedError("Only French and German are supported at the moment.")
        
        

class Translator:
    
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.translator = EasyGoogleTranslate(source_language=self.source, target_language=self.target, timeout=100)
    
    def translate(self, phrase, translated=None, get_audio=False, filepath = None):
        '''
        - translated: if you already have the translation, you can pass it here. Helps when google translate fails to give a correct translation.
        '''
        if translated == None:
            self.translated = self.translator.translate(phrase.strip())
        else:
            self.translated = translated
        if get_audio != False:
            if (get_audio=='source' and self.source == 'fa') or (get_audio=='target' and self.target=='fa') or (get_audio=='both' and (self.source=='fa' or self.target=='fa')):
                raise ValueError("Generating Persian speech is not currently supported")
            if filepath == None:
                raise ValueError("Please provide a filepath.")
            if get_audio == 'source' or get_audio == 'both':
                source_audio = gTTS(text=phrase, lang=self.source)
                source_tmp_file = BytesIO()
                source_audio.write_to_fp(source_tmp_file)
                source_tmp_file.seek(0)
                self.source_audio_segment = AudioSegment.from_mp3(source_tmp_file)
            if get_audio == 'target' or get_audio == 'both':
                target_audio = gTTS(text=self.translated, lang=self.target)
                target_tmp_file = BytesIO()
                target_audio.write_to_fp(target_tmp_file)
                target_tmp_file.seek(0)
                self.target_audio_segment = AudioSegment.from_mp3(target_tmp_file)
            
            output_audio = AudioSegment.silent(duration=1)
            
            if get_audio == 'both':
                output_audio += self.source_audio_segment
                output_audio += AudioSegment.silent(duration=1500)
                output_audio += self.target_audio_segment
            elif get_audio == 'source':
                output_audio += self.source_audio_segment
            elif get_audio == 'target':
                output_audio += self.target_audio_segment
            
            output_audio.export(filepath, format='mp3')
            
            
            
class PhraseTranslationWriter:
    
    def __init__(self, phrases, translations, audiopaths, part_of_speechs, genders=None, header=True, **kwargs):
        self.phrases = phrases
        self.translations = translations
        self.audiopaths = audiopaths
        self.part_of_speechs = part_of_speechs
        self.genders = genders
        self.header = header
        self.no_gender = False
        self.no_role = False
        if 'no_gender' in kwargs and kwargs['no_gender'] == True:
            self.no_gender = True
        if 'no_role' in kwargs and kwargs['no_role'] == True:
            self.no_role = True
        
    def write(self, output_type='markdown'):
        if output_type not in ['markdown', 'telegram']:
            raise ValueError("output type must be either 'markdown' or 'telegram'")
        
        output = ''
        if self.header == True:
            if self.no_role == False and self.no_gender == False:
                output += '|--|--|--|--|--|\n'
                output += '| کلمه/عبارت | ترجمه | نقش | جنسیت | تلفظ |\n'
                output += '|--|--|--|--|--|\n'
            elif self.no_role == True and self.no_gender == True:
                output += '|--|--|--|\n'
                output += '| کلمه/عبارت | ترجمه | تلفظ |\n'
                output += '|--|--|--|\n'
            else:
                raise ValueError("The case where only of the no_rule and no_gender is True is not supported.")
        if output_type == 'markdown':
            if self.no_role == False and self.no_gender == False:
                for phrase, translated, part_of_speech, gender, filepath in zip(self.phrases, self.translations, self.part_of_speechs, self.genders, self.audiopaths):
                    gender = gender if gender is not None else ' '
                    output += '| ' + phrase + ' | ' + translated + ' | ' + part_of_speech + ' | ' + gender + ' | ' + f'<audio controls><source src="{filepath}" type="audio/mpeg"></audio>' + ' |' + '\n'        
            elif self.no_role == True and self.no_gender == True:
                for phrase, translated, filepath in zip(self.phrases, self.translations, self.audiopaths):
                    output += '| ' + phrase + ' | ' + translated + ' | ' + f'<audio controls><source src="{filepath}" type="audio/mpeg"></audio>' + ' |' + '\n'
            else:
                raise ValueError("The case where only of the no_rule and no_gender is True is not supported.")    
        elif output_type == 'telegram':
            if self.no_role == False and self.no_gender == False:
                for phrase, translated, part_of_speech, gender in zip(self.phrases, self.translations, self.part_of_speechs, self.genders):
                    gender = gender if gender is not None else ' '
                    output += '| ' + phrase + ' | ' + translated + ' | ' + part_of_speech + ' | ' + gender + ' | ' + '\n'
            elif self.no_role == True and self.no_gender == True:
                for phrase, translated in zip(self.phrases, self.translations):
                    output += '| ' + phrase + ' | ' + translated + ' | ' + '\n'
            else:
                raise ValueError("The case where only of the no_rule and no_gender is True is not supported.")    
        
        return output
    
    
class VerbConjugationWriter:
    
    def __init__(self, verb, meaning, pronouns, verbs, audiopaths):
        self.verb = verb[:]
        self.meaning = meaning
        self.pronouns = pronouns
        self.verbs = verbs
        self.audiopaths = audiopaths
        
    def write(self, output_type='markdown'):
        if output_type not in ['markdown', 'telegram']:
            raise ValueError("output type must be either 'markdown' or 'telegram'")
        
        output = ''
        if output_type == 'markdown':
            output += '## فعل ' + self.verb + ' (' + self.meaning + ')' + '\n\n'    
            output += '|--|--|--|' + '\n'
            output += '| ضمیر | فعل | تلفظ |' + '\n'
            output += '|--|--|--|' + '\n'
            for pronoun, verb, audiopath in zip(self.pronouns, self.verbs, self.audiopaths):
                output += '| ' + pronoun + ' | ' + verb + ' | ' + f'<audio controls><source src="{audiopath}" type="audio/mpeg"></audio>' + ' |' + '\n'
        elif output_type == 'telegram':
            output += 'فعل ' + self.verb + ' (' + self.meaning + ')' + '\n\n'
            for pronoun, verb, audiopath in zip(self.pronouns, self.verbs, self.audiopaths):
                output += pronoun + ' | ' + verb + ' | '  + '\n'
        
        return output


def get_conjugation_output(verb, output_type='markdown', save_root_path='', github_root_path='', translated=None, lang='fr'):
    if lang not in ['fr', 'de']:
        raise ValueError("Only French and German are supported at the moment.")
    failure = False
    conjugator = Conjugator()
    _ = conjugator.get_conjugation(verb=verb, lang=lang)
    github_filepaths = []

    system_filepaths = []
    
    for pronoun, curr_verb in zip(conjugator.pronouns, conjugator.verbs):
        pronoun = pronoun.split('/')[0] if '/' in pronoun else pronoun
        text_for_speech = pronoun + ' ' + curr_verb
        base_filepath = str(time.time()).replace('.','P') + '-' + text_for_speech.translate(str.maketrans('', '', string.punctuation)).replace(' ','').lower() + '.mp3'
        save_filepath = save_root_path + base_filepath
        system_filepaths.append(save_filepath)
        github_filepath = github_root_path + base_filepath
        github_filepaths.append(github_filepath)
        try:
            tr = Translator(source=lang, target='fa')
            tr.translate(text_for_speech, get_audio='source', filepath=save_filepath)
        except:
            failure = True
            for filepath in system_filepaths:
                if os.path.exists(filepath):
                    os.remove(filepath)
            raise ValueError("Failed to translate or get audio for the conjugation. Please try again later.")
        
    translated = translated if translated is not None else tr.translated
    writer = VerbConjugationWriter(verb, translated, conjugator.pronouns, conjugator.verbs, github_filepaths)
    if failure == False:
        clipboard.copy(writer.write(output_type))


def get_phrase_translation_output(phrases, given_translations=[], source='fr', target='fa', save_root_path='', github_root_path='', output_type='markdown', header = True):
    failure = False
    translator = Translator(source=source, target=target)
    github_filepaths = []
    system_filepaths = []
    part_of_speechs = []
    translations = []
    genders = []
    explorer = WordExplorer()
    for phrase, given_translation in zip(phrases, given_translations):
        base_filepath = str(time.time()).replace('.','P') + '-' + phrase.translate(str.maketrans('', '', string.punctuation)).replace(' ','').lower() + '.mp3'
        save_filepath = save_root_path + base_filepath
        system_filepaths.append(save_filepath)
        github_filepath = github_root_path + base_filepath
        try:
            translator.translate(phrase, get_audio='source', filepath=save_filepath)
        except:
            failure = True
            for filepath in system_filepaths:
                if os.path.exists(filepath):
                    os.remove(filepath)
            raise ValueError("Failed to get audio for the phrase. Please try again later.")
        github_filepaths.append(github_filepath)
        if len(given_translation.strip()) == 0:
            translations.append(translator.translated)
        else:
            translations.append(given_translation)
        is_word = True if len(phrase.strip().split())==1 else False
        try:
            if source in ['de', 'fr']:
                if is_word == True:
                    explorer.explore(phrase, source)
                    part_of_speechs.append(explorer.part_of_speech)
                    genders.append(explorer.gender)
                else:
                    part_of_speechs.append(' ')
                    genders.append(' ')
            elif source == 'ko':
                pass
            else:
                raise NotImplementedError('Only French, Korean, and German are supported at the moment.')
        except:
            for filepath in system_filepaths:
                if os.path.exists(filepath):
                    os.remove(filepath)
            break
    
    if source in ['de', 'fr']:        
        writer = PhraseTranslationWriter(phrases, translations, github_filepaths, part_of_speechs, genders, header, lang=source)
    elif source == 'ko':
        writer = PhraseTranslationWriter(phrases, translations, github_filepaths, part_of_speechs, genders, header, no_gender=True, no_role=True, lang=source)
    else:
        raise NotImplementedError('Only French, Korean, and German are supported at the moment.')
    if failure == False:
        clipboard.copy(writer.write(output_type))