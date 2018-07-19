### 天気予報apiとtwitterapiをマッシュアップして天気情報取得サービスを作成するリポジトリ(一応完成）

#### ○仕様
    □URL:https://ancient-castle-70500.herokuapp.com/
    
    □今の所、都市名を入力欄に入れるとweatherhacks(情報があれば）とtwitterから天気情報を収集して1つのページに表示します
    
    □twitterは5時間以内のその都市の天気に関するツイートを新しい順に20件まで拾ってきます
    
    □現在の時刻からの時間差も表示しますが、ここはバグがあるかもしれません

#### ○使用api
    □weatherhacks(livedoor天気情報）

    □twitterapi

#### ○言語
    □python
    
    □html

    □CSS
    
    □javascript

#### ○ウェブサービス作成に使用したサービス
    □Flask

    □heroku
    
#### ○Todo
    □他の天気情報apiも組み合わせる（openweathermap, darkskyが候補）
    
    □twitterapiの検索クエリを改善する（今かなり雑な検索をしている）
    
    □CSSを改造して見栄えを改善する
    
    □configオプションをユーザ側から幾つか弄れるようにする
    
    □weatherhacksは限られた都市しか情報がないのでプルダウン選択か何かにする
    
    □多分時間差周りにバグがあるので直す
    
    □コードがごちゃごちゃしているので直す
    
#### ○備考
    □このリポジトリをクローンして実行する場合は、
    '''python
    CONSUMER_KEY = '*****************'
    CONSUMER_SECRET = '*****************'
    ACCESS_TOKEN = '*****************'
    ACCESS_SECRET = '*****************'
    '''
    という形式のconfig.pyというファイルに自身で取得したtwitterの認証情報を入れる必要があります。
