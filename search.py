import os
from datetime import datetime
from pytz import timezone
from dateutil import parser

import config
import constant
from functions import getTweetData

hashTag = config.HASH_TAG
since = config.SINCE
until = config.UNTIL
outputPath = config.OUTPUT_PATH

# ディレクトリがなかったら作成
if not os.path.isdir(outputPath):
    os.mkdir(outputPath)

tweetsCsvFile = open(outputPath + '/' + constant.TWEETS_CSV_FILE_PATH, 'w')
tweetsTxtFile = open(outputPath + '/' + constant.TWEETS_TXT_FILE_PATH, 'w')
reportFile = open(outputPath + '/' + constant.REPORT_FILE_PATH, 'w')

maxId = -1  # 途絶えた場合はここにIDを入れる
count = 0
userIds = [""]
shouldGetNextTweetData = True

try:
    while shouldGetNextTweetData:
        res = getTweetData(hashTag, until, maxId)

        if not res['result']:
            print('APIがエラーなので中止')
            shouldGetNextTweetData = False
            break
        print('GetCount: ' + str(len(res['statuses'])))
        for status in res['statuses']:  # タイムラインリストをループ処理
            createdAt = parser.parse(status['created_at'])

            jstStr = datetime.strftime(createdAt.astimezone(timezone('Asia/Tokyo')), '%Y-%m-%d %H:%M:%S %Z')
            print(status['id_str'] + " / " + jstStr + ' - ' + status['user']['name'])

            t = status['text']
            t = t.replace(hashTag, '')
            t = t.replace('\n', ' ')
            t = t.replace(';', '；')
            tweetsTxtFile.write(t + '\n')
            tweetsCsvFile.write(str(status['id']) + ';' + status['user']['id_str'] + ';' + status['user']['name'] + ';' + t + '\n')

            count += 1
            maxId = status['id'] - 1
            userIds.append(status['user']['id_str'])

            if createdAt <= parser.parse(since):
                print("予定時間を超えたので停止")
                shouldGetNextTweetData = False
                break

        print('TotalCount: ' + str(count))
except:
    print('例外発生')
    shouldGetNextTweetData = False
else:
    print('例外は発生しませんでした。')
    shouldGetNextTweetData = False

# レポート作成
reportFile.write('Hash Tag;' + hashTag + '\n')
reportFile.write('Since;' + since.replace(":00+09:00", "").replace("-", "/") + '\n')
reportFile.write('Until;' + until.replace(":00_JST", "").replace("_", " ").replace("-", "/") + '\n')
reportFile.write('Total Tweets;' + str(count) + '\n')
uniqueUserIds = list(set(userIds))
reportFile.write('Unique Users;' + str(len(uniqueUserIds)) + '\n')
average = round((count / len(uniqueUserIds)), 1)
reportFile.write('Tweet Average;' + str(average) + '\n')
reportFile.write('Next Max ID;' + str(maxId) + '\n')

tweetsCsvFile.close()
tweetsTxtFile.close()
reportFile.close()
print('Finish!')
