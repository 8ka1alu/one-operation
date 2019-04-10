# ワンナイト人狼GMbot ver1.0(beta)

discord.pyと自作モジュールonenight_jinro.pyによって動くDiscord Bot用のスクリプトです。不具合だらけですのでよく読んでプレイしてください(可能であれば「占い師の操作」以下をプレイヤーにも読ませておいてください)。
構造の複雑さから上限人数の増加、役職の追加などは推奨されませんがonenight_jinro.pyの方から改造してください。
近い内に改造の容易な、不具合を減らしたバージョンを追加する予定です。

## 遊び方

 1. onjbot.pyの12行目、accesstokenの内容をDiscordのbot管理画面からコピーできるトークンに書き換えてください。
 2. ```$ python onjbot.py```でbotを起動します。
 3. Discord内の好きなテキストチャンネルで```!人狼スタート```とチャットに送ることでゲームが待機状態になります。以降のコマンドはこのときのチャンネルのみ使用することを推奨します。
 4. ```!参加```をそれぞれのプレイヤーが送ることで参加が受理され、プレイヤー人数が更新されていきます。またすでに参加しているプレイヤーがもう一度送ることで参加を取り消すこともできます。
 5. 人数が揃い準備が整ったら(```!人数```で確認できます)、```!開始```でゲームが開始されます。このときからノンストップでゲームが進行するので、全員の準備が完了していることを確認してから送ってください。
 6. ゲーム開始の合図がメインチャンネルに送られ、ダイレクトメッセージにて各参加者に役職が通知されます。この時点から夜明けのメッセージが送られるまで各プレイヤーはマイクミュートすることを推奨します。
 7. 役職の通知の10秒後、占い師のターンが行われます(占い師のプレイヤーにのみダイレクトメッセージが送られます)。占い師のターンは占い師が存在してもしなくても、占いを行っても行わなくても**20秒で終了します**。
 8. 占い師のターン終了後、人狼のターンが行われます(人狼のプレイヤーにのみダイレクトメッセージが送られます)。人狼のターンは**10秒で終了します**。
 9. 人狼のターン終了後、怪盗のターンが行われます(怪盗のプレイヤーにのみダイレクトメッセージが送られます)。怪盗のターンは**20秒で終了します**。
 10. 怪盗のターン終了後、夜明けとなり討論の時間になります。ゲーム内にタイマーを設定していないので、討論時間を無制限としない場合ご自分で時間を測ってください(投げやり)。
 11. 討論の時間が終了したら、```!投票```で投票フェーズに移行します。
 12. 投票が終了したら、```!結果```で試合結果を開示します。誰が吊られたか(複数同票の場合その中からランダムで吊られます)、吊られたのが人間か人狼か、そして最終的なプレイヤー全員の役職が開示されます。
 13. 試合結果の開示をもってゲームの終了となりますが、この状態では参加プレイヤーの情報は保持しています。同じメンバーで再度試合を始めるには```!開始```を押すのみですし、この状態で他のプレイヤーが追加で```!参加```することもできます。
 14. botの終了には```!じゃあな```をご利用ください。

## 占い師の操作

占い師のターンになると、占い師のプレイヤー宛に
>@PLAYER3 占う相手を選んでください。「!u」の後ろに以下の数字をつけてチャットを送ってください：

>0: @PLAYER1, 1: @PLAYER2, 3: @PLAYER4, -1: 山札
というようなメッセージがダイレクトメッセージで送られてきます。
この状態で例えばPLAYER1を占うのであれば```!u0```、山札を見るのであれば```!u-1```と送ってください。占い結果が返ってきます。また占いは一度しか行えませんので占い先の変更はできません。
エラー処理をしていないので最初にゲームを開始したテキストチャンネルなどにコマンドを送っても占い結果がそのテキストチャンネルに返ってきます。デバッグでなければゲーム崩壊ものですのでコマンドは**絶対にダイレクトメッセージで送ってください**。
また20秒間何もコマンドを送らない場合、**ゲームが進行不能になるバグが存在します(そんな馬鹿な)**。占い師のプレイヤーは**絶対にコマンドを送ってください**。
占い拒否については、表示されていませんが自分のIDをつけてコマンドを送ってください。0〜(プレイヤー人数 - 1)のうち上記メッセージで欠けている数字です(上の例では2)。

占いの結果は**個人を占う場合は役職ごと**、**山札の2枚の場合は人間か人狼かのみ**判明します。

## 人狼の操作

人狼のターンになると、人狼のプレイヤー宛に
>人狼はあなた一人です。
または
>あなたと@PLAYER1が人狼です。
というようなメッセージがダイレクトメッセージで送られてきます。
人狼にはコマンド操作はありませんので返信する必要はありません。

## 怪盗の操作

怪盗のターンになると、怪盗のプレイヤー宛に
>@PLAYER1 役職を盗む相手を選んでください。「!k」の後ろに以下の数字をつけてチャットを送ってください：

>1: @PLAYER2, 2: @PLAYER3, 3: @PLAYER4,
というようなメッセージがダイレクトメッセージで送られてきます。
この状態で例えばPLAYER2のカードを盗むのであれば```!k1```と送ってください。カードの交換が行われ、対象としたプレイヤーの元の属性(つまり怪盗だったプレイヤーの現在の属性)が返ってきます。またカード交換は一度しか行なえませんのでカード交換先の変更はできません。
不具合は占い師と同じようなものを持っています。**コマンドはダイレクトメッセージで**、また**絶対にコマンドを送ってください**。
怪盗拒否については、表示されていませんが自分のIDをつけてコマンドを送ってください。0〜(プレイヤー人数 - 1)のうち上記メッセージで欠けている数字です(上の例では0)。

怪盗の結果は**人間か人狼かのみ**判明します。

## 投票の操作

>@PLAYER1 @PLAYER2 @PLAYER3 @PLAYER4 @PLAYER5 投票に入ります。各プレイヤーは当アカウント宛に「!t」の後ろに以下の英数字をつけてダイレクトメッセージを送ってください：

>0: @PLAYER1, 1: @PLAYER2, 2: @PLAYER3, 3: @PLAYER4, 4: @PLAYER5, h: 平和村

>投票結果および試合結果の表示を行う際には「!結果」とお送りください。
```!投票```によって投票フェーズに入ったら、bot宛にダイレクトメッセージを送ってください。
例えばPLAYER3の処刑に投票するのであれば```!t2```と送ってください。
>@PLAYER3 に投票しました。
と返ってきます。また別の投票コマンドを追加で送ることで投票先を変更できます。
メッセージではダイレクトメッセージと書かれていますが、最初にゲームを開始したテキストチャンネルに投票コマンドを送っても問題ありません。テキストチャンネルに投票結果が表示されるため、投票は開示まで伏せられているもの、というルールを厳密にするのであれば**絶対にダイレクトメッセージで投票してください**。
```!投票```コマンド後は```!結果```までマイクミュートを推奨します。
全員の投票が済んでいない場合、```!結果```してもエラーを吐きます。
