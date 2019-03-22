from DBconnection import connection1
from googleapiclient.discovery import build
from TwitterAPI import TwitterAPI
from datetime import datetime
import re
from nltk.tokenize import word_tokenize, sent_tokenize


class GeneralSearch:
    def __init__(self, clientName, clientID):
        '''
              A Constructr to initialize needed variables and retrive
              Keywords from Database
              '''

        self.clientName = clientName
        self.clientID = clientID
        self.document = ''
        self.textDocument = ''
        self.cleanText = ''
        self.keyWords = {}
        self.GOOGLE_API_KEY = "AIzaSyDVjsiH1KjjI7Wus5imNPXFpdczbR5Iaqg"
        self.GOOGLE_CSE_ID = "002858524502186211496:qscl9gemjug"  # Google Custom search engine ID
        try:
            cursor, conn, engine = connection1()

            query = "SELECT * from KeyWord"
            cursor.execute(query)

            data = cursor.fetchall()

            for i in range(len(data)):
                self.keyWords[data[i][1]] = 0

            cursor.close()
        except Exception as e:
            print(str(e))

    def twitter_search(self):
        '''
        this function is responsible for running search on twitter
        :param SEARCH_TERM: the search key word 'Client Name'
        '''

        SEARCH_TERM = self.clientName
        PRODUCT = 'fullarchive'
        LABEL = 'SMI_tool'
        SANDBOX_CONSUMER_KEY = 'd51IGnDlp7Aw58l4SnDufKop2'
        SANDBOX_CONSUMER_SECRET = '92rDpKfnLUR01y69gU7KFo5iCWCIVBZgLOCtxerfNq6dhfO8vZ'
        SANDBOX_TOKEN_KEY = '705985483-XBPCazD0DB1I9gh9SepR1S26FnTTubMsPONEttr9 '
        SANDBOX_TOKEN_SECRECT = 'wPSaAbogn7kIgzOLm2EeMdtY0vZthDcrGHCBTDFe38RZ0'

        api = TwitterAPI(SANDBOX_CONSUMER_KEY,
                         SANDBOX_CONSUMER_SECRET,
                         SANDBOX_TOKEN_KEY,
                         SANDBOX_TOKEN_SECRECT)

        r = api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL),
                        {'query': SEARCH_TERM})
        f = open("Twitterresult.txt", "w+")
        for item in r:
            f.write(item['text'] + '\n')
            self.tweets.append(item['text'])
            self.document = self.document + '\n' + item['text']

        f.close()

    def google_search(self):
        '''
        this function is responsible for running search on google
        :return: Client_searchResult : numeric search result between 0 and 1
                Client_SearchLabel : String Labeling the client (High, Medium,Low,Clean)
        '''

        res = []
        service = build("customsearch", "v1", developerKey=self.GOOGLE_API_KEY)

        res.append(service.cse().list(
            q=self.clientName,
            cx=self.GOOGLE_CSE_ID,
            num=10,
            start=1,
        ).execute())
        try:
            for each in res:

                for i in range(0, len(each['items'])):
                    self.document = self.document + '\n' + each['items'][i]['title']
                    self.document = self.document + '\n' + each['items'][i]['snippet']

            self.textDocument = sent_tokenize(self.document)
            self.cleanText = [self.cleanDocument(s) for s in self.textDocument]

            self.docInfo = self.createDocuments(self.cleanText)
            self.create_freq_dict(self.cleanText)
            Client_searchResult, Client_SearchLabel = self.calculate_TFIDF()
        except Exception as e:
            Client_searchResult = 0
            Client_SearchLabel = 'clean'

        return Client_searchResult, Client_SearchLabel

    def cleanDocument(self, doc):
        '''
        this function clean the search result from any white space and special characters
        :param doc: a string containing the search result
        :return: a clean string
        '''

        # Replace special character with ' '
        str = re.sub('[^\w\s]', '', doc)
        str = re.sub('_', '', str)

        # Change any white space to one space
        str = re.sub('\s+', ' ', str)

        # Remove start and end white space
        str = str.strip()

        return str

    def createDocuments(self, cleanDoc):
        '''
        This function splits the search results into sentance considring each
        sentance as a document
        :param cleanDoc:
        :return:
        '''

        doc_info = []
        i = 0
        for cleanDoc in self.cleanText:
            i += 1
            count = self.countWords(cleanDoc)
            temp = {'doc_id': i, 'doc_length': count}
            doc_info.append(temp)
        return doc_info

    def countWords(self, doc):
        count = 0
        words = word_tokenize(doc)
        for word in words:
            count += 1
        return count

    def create_freq_dict(self, cleanDoc):
        i = 0
        for each in cleanDoc:
            i += 1
            words = word_tokenize(each)
            for word in words:
                word = word.lower()
                if word in self.keyWords:
                    self.keyWords[word] += 1

    def calculate_TFIDF(self):
        '''
        this function calculating the number of keywords appeared form the list
        and frequncey of each word then the calculate TFIDF
        :return: Client_searchResult : numeric search result between 0 and 1
                Client_SearchLabel : String Labeling the client (High, Medium,Low,Clean)
        '''

        num_of_apearance = 0
        sum_of_frequencies = 0
        max_frequency = 0
        Client_SearchResult = 0
        Client_SearchLabel = ''
        for keys, values in self.keyWords.items():
            if values > 0:
                max_frequency = max(self.keyWords.values())
                sum_of_frequencies += values
                num_of_apearance += 1
        try:

            Client_SearchResult = ((num_of_apearance * max_frequency) / (16))
            # Normalization
            if Client_SearchResult > 1:
                Client_SearchResult = 1
        except ZeroDivisionError:
            Client_SearchResult = 0

        if 0.7 < Client_SearchResult <= 1:
            Client_SearchLabel = 'High'
        elif 0.33 < Client_SearchResult <= 0.7:
            Client_SearchLabel = 'Medium'
        elif 0 < Client_SearchResult <= 0.33:
            Client_SearchLabel = 'Low'
        else:
            Client_SearchLabel = 'Clean'

        date_now = datetime.now()
        formatted_date = date_now.strftime('%Y-%m-%d %H:%M:%S')

        cur, db, engine = connection1()
        cur.execute(
            "UPDATE SMI_DB.Client SET generalSearchDate= '%s', generalSearchResult= '%s' WHERE clientID='%s' " % (
            formatted_date, Client_SearchResult, self.clientID))
        db.commit()
        cur.close()
        db.close()
        return Client_SearchResult, Client_SearchLabel



