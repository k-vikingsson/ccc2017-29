import couchdb
from couchdb.design import ViewDefinition
import json


class CouchdbViewManager:
    server = couchdb.Server('http://cloud:password@115.146.93.125:5984/')

    def save_view(self, dbname, viewname):
        fp = './' + viewname.split('/')[1] + '.json'
        try:
            f = open(fp, 'w+')
            db = self.server[dbname]

            doc_list = []
            docs = db.view(viewname, group=True)
            for doc in docs:
                entry = {}
                for dictkey, value in doc.key.items():
                    entry[dictkey] = value
                entry['value'] = doc.value
                doc_list.append(entry)
            result = json.dumps(doc_list)
            f.write(result)
        except IOError:
            pass
        finally:
            f.close()


    def save_hours_view(self, dbname, viewname):
        fp = './' + viewname.split('/')[1] + '.json'
        try:
            f = open(fp, 'w+')
            db = self.server[dbname]

            '''entry:{name:'',state:'',24h_sentiments:{00:sentiment,01:sentiment,...}}'''
            entry_list = []
            docs = db.view(viewname, group=True)
            for doc in docs:
                name = doc.key['name']
                state = doc.key['state']
                hour = doc.key['hour']
                sentiment = doc.value

                key_exist = False
                for entry in entry_list:
                    if (entry['name'] == name) and (entry['state'] == state):
                        entry["24h_sentiments"][hour] = sentiment
                        key_exist = True
                        break

                if not key_exist:
                    entry = {}
                    entry['name'] = name
                    entry['state'] = state
                    sentiment_dict = {}
                    sentiment_dict[hour] = sentiment
                    entry['24h_sentiments'] = sentiment_dict
                    entry_list.append(entry)

            result = json.dumps(entry_list)
            f.write(result)
        except IOError:
            pass
        finally:
            f.close()


    def save_weekday_view(self, dbname, viewname):
        fp = './' + viewname.split('/')[1] + '.json'
        try:
            f = open(fp, 'w+')
            db = self.server[dbname]

            '''entry:{name:'',state:'',weekday:{'Mon':sentiment,'Tue':sentiment,...}}'''
            entry_list = []
            docs = db.view(viewname, group=True)
            for doc in docs:
                name = doc.key['name']
                state = doc.key['state']
                weekday = doc.key['weekday']
                sentiment = doc.value

                key_exist = False
                for entry in entry_list:
                    if (entry['name'] == name) and (entry['state'] == state):
                        entry["24h_sentiments"][weekday] = sentiment
                        key_exist = True
                        break

                if not key_exist:
                    entry = {}
                    entry['name'] = name
                    entry['state'] = state
                    sentiment_dict = {}
                    sentiment_dict[weekday] = sentiment
                    entry['24h_sentiments'] = sentiment_dict
                    entry_list.append(entry)

            result = json.dumps(entry_list)
            f.write(result)
        except IOError:
            pass
        finally:
            f.close()

'''
if __name__ == '__main__':
    couchdbVM = CouchdbViewManager()
    couchdbVM.save_view("final_tweets", "Scenarios/city_language")
    couchdbVM.save_view("final_tweets", "Scenarios/city_average_sentiment")
    couchdbVM.save_view("final_tweets", "Scenarios/emoji_contains_smile")
    couchdbVM.save_hours_view("final_tweets", "Scenarios/hours_average_sentiment")
    couchdbVM.save_view("final_tweets", "Scenarios/tweets_city_eng_noneng")
    couchdbVM.save_weekday_view("final_tweets", "Scenarios/weekday_average_sentiment")
    couchdbVM.save_view("language", "Scenario/aurin_city_eng_noneng")
    couchdbVM.save_view("person_earn_2000_weekly_vic", "newDoc/person_earn_2000_vic")
'''