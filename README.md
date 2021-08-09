# __<font color="Lime">  　設定  </font>__
CWTools Paradox Language Servicesの設定方法  
ユーザー設定	→	設定	→	ユーザー  
拡張機能	→	CWTools configuration  
Cwtools › Cache: Stellaris	にステラリス本体を  
例C:\Program Files (x86)\Steam\steamapps\common\Stellaris  

ユーザー設定	→	設定	→	ワークスペース  
拡張機能	→	CWTools configuration  
Cwtools › Cwtools: Rules_folder	にModフォルダにある.cwtoolsの絶対パスを  
例I:\Prg\Stellaris\Additional Districts\.cwtools

これしたのちにvscordを再起すると補助機能が使える

# __<font color="Lime">  　ToDo  </font>__
・自然生成される地区をAIが使うように調整   
  調整する場所  
common\districts  
common\sector_focuses  
common\colony_automation  
common\economic_plans  
それぞれのai_weightもしくはweightで調整  
現状colony_automation	sector_focuses	districtsのweightが影響していると思われる  

economic_plansはAIが鉱石無視してあほみたいに消費財を作るのを防ぐため  
個々の条件考えればAI賢いよ

00_colony_typesにADBの地区を追加

------
# __<font color="Lime">  　完成  </font>__
## __☆ 技術__

| 技術 | Tire | cost | weight | effect  |
|:------|:------|:------|:------|:------|

大規模地区開発計画  2次区域  
大規模水中建設技術  水中都市  
大規模空中建設技術  空中都市  
大規模地中建設技術  地下都市  

## __☆ 地区__
### __〇 都市区域追加__
区域 | 住居 | 効果 | 生成
---|----|----|---
遺跡都市 | 5 | 発掘者1 |自然発生
空中都市 | 30 | 事務員5 区域+1 |自然発生 技術開発
水上都市 | 20 | 事務員4 区域+1 | 自然発生 技術開発
水中都市 | 5 | 水中農家2 区域+1 | 自然発生 技術開発
地中都市 | 5 | 施設維持業者1 区域+1 | 自然発生 技術開発

### __〇 発電区域追加__
区域 | 住居 | 効果 | 生成
---|----|----|---
太陽光発電 | 2 | 技術者5 | （技術開発）  
地熱発電 | 2 | 地熱技師2 | （自然発生）  
潮流発電 | 2 | 技術者5  区域+1 | （自然発生）  
天然原子炉発電 | 2 | 原子力技師2 | （自然発生）  

### __〇 鉱物区域追加__
区域 | 住居 | 効果 | 生成
---|----|----|---
露天鉱床 | 2 | 採掘者6 | 自然発生
水中鉱床 | 2 | 水中採掘者2 区域+1 | 自然発生
軌道鉱石群 | 0 | 宇宙採掘者2  区域+1  | 自然発生 月か輪がある
高質鉱床 | 2 | 効率的採掘者4 | 自然発生
低質鉱床 | 2 | 低効率採掘者5 | 自然発生

### __〇 農業区域追加__
区域 | 住居 | 効果 | 生成
---|----|----|---
棚状耕作地 | 2 | 農民3 | 自然発生
水中生態系 | 2 | 水中農家2 | 自然発生
菌類群生体 | 2 | 菌農家2 | 自然発生
大規模牧草地 | 2 | 酪農家3 | 自然発生
大自然農業地 | 2 | 大規模農家3 | 自然発生

### __〇 その他区域__
区域 | 住居 | 効果 | 生成
---|----|----|---
古代遺跡群 | 2 | 発掘者2 | 自然発生
古代データバンク | 2 | データマイナー2 | 自然発生
天然の要塞 | 2 | 将校1  兵士4 爆撃耐性高 | 自然発生

### __〇 後で設置可能__（1-4つまで設置可能）
区域 | 住居 | 効果
---|----|---
官庁街 | 2 | 行政官1 官僚4 | 
大学街 | 5 | 教授職2 科学者2 | 
住宅街 | 10 | 事務員5 | 
造船工廠 | 2 | 造船技師4 | 
通信区域 | 2 | インフラ技師2 | 
観光区域 | 3 | エンターテイナー４ | 
防衛区域 | 3 | 将官1 将校2 兵士4 | 
構想特区 | 2 | 豪商1 起業家3 | 
研究特区 | 2 | 科学総裁1 研究者5 | 
宇宙港区域 | 2 | 宇宙港整備員3 | 
軌道エレベーター | 2 | 快適度5 交易価値5 幸福度5 宇宙港整備員1 造船技師1 |

## __☆ 職業__
### __〇 労働者__
| 職業 | produces | upkeep | effect  |
|:------|:------|:------|:------|
水中農家 | 食料6 | 消費財1 | 
施設維持業者 | 鉱石5 | 消費財1 | 快適度3
地熱技師 | エネルギ6 |  | 
原子技師 | エネルギ8 | 消費財2 | 
水中採掘者 | 鉱石5 | 消費財1 | 
宇宙採掘者 | 鉱石6 | 消費財2 | 
効率的採掘者 | 鉱石8 | 
低効率採掘者 | 鉱石3 | 
菌農家 | 食料5 | 
酪農家 | 食物 8 | 消費財1
大規模農家 | 食料6 | 
サービス職 |  |  | 快適度2 幸福度+1%
強制労働者 | 食料1 鉱物1<br>消費財0.1 |  | 

### __〇 専門家__
| 職業 | produces | upkeep | effect  |
|:------|:------|:------|:------|
データマイナー | 物理2 社会2 工学2 | 消費財5 | 科学者出力0.05
造船技師 |  | 消費財3  合金2 | 造船速度0.05 宇宙軍許容量2
インフラ技師 |  | 消費財3 | 労働者出力0.05
将校 |  | 消費財3 | 防衛軍5    宇宙軍許容量    10
起業家 | 社会研究2 | 消費財3 | 交易価値0.05 交易価値5
宇宙港管制官 | 工学3 | 消費財2   合金1 | 宇宙軍許容量10
教授職 |  | 消費財5 | 専門家出力*0.05
発掘者 | 出土品0.5 | 消費財5 | 
銀行家 | エネルギー+5 |  | 快適度+3 交易価値+5
法曹 | 社会学+2 |  | 快適度+1 犯罪度-5
ジャーナリスト | 統合力+3 |  | 労働者政治力-10% 快適度+2
データ司書 | 物理2 社会2 工学2 統合力+3 |  | 
公安職員 |  |  | 暗号力+1 犯罪度-15 安定度+1

### __〇 統治者__
| 職業 | produces | upkeep | effect  |
|:------|:------|:------|:------|
将官 |  | 消費財4 | 防衛軍8 宇宙軍許容量16  
側近 | 影響力1 | 消費財3 | 
代弁者 |  | 消費財3 | 安定度+5 幸福度+5%   

## __☆ 建物__
### __〇 帝国に1つ__

| 建物 | authority | cost | upkeep | time | effect
|:------|:------|:------|:------|:------|:------|
| __宮殿__ | 企業以外 | 鉱物1000 | エネルギ3 | 550 | 安定度+10	側近Job+1 |
| __CEOオフィス__ | 企業のみ | 鉱物800 | エネルギ3 | 550 | 安定度+10	側近Job+1 |
| __国防省__ | 企業以外 | 鉱物800 揮発粉100 | エネ5 揮発粉1 | 550 | 宇宙軍許容量+30 地上軍士気+10	行政官+1 将校+1 官僚+1 |
| __管理警備本部__ | 企業のみ | 鉱物800 揮発粉100 | エネ5 揮発粉1 | 550 | 宇宙軍許容量+10 地上軍士気+5 艦隊建造速度+10	役員+1 将校+1 管理職+1 |
| __内務省__ | 企業以外 | 鉱物800 レアクリ100 | エネ5 レアクリ1 | 550 | 帝国の犯罪度-10% 各惑星幸福度+10%	行政官+1 官僚+2 |
| __労務管理本部__ | 企業のみ | 鉱物800 レアクリ100 | エネ5 レアクリ1 | 550 | 帝国の犯罪度-10% 各惑星幸福度+5% リーダー経験値+10%	役員+1 管理職+2 |
| __外務省__ | 企業以外 | 鉱物800 揮発粉100 | エネ5 揮発粉1 | 550 | 外交発言力+10% 使節+1	行政官+1 官僚+2 |
| __外商本部__ | 企業のみ | 鉱物800 揮発粉100 | エネ5 揮発粉1 | 550 | 支社価値+10% 使節+1 交易価値+10%	役員+1 管理職+2 |
| __情報省__ | 企業以外 | 鉱物800 エキゾガス100 | エネ5 エキゾガス1 | 550 | 解読力+5 暗号力+10	行政官+1 官僚+2 |
| __情報セキュリティー本部__ | 企業のみ | 鉱物800 エキゾガス100 | エネ5 エキゾガス1 | 550 | 解読力+10 暗号力+5	役員+1 管理職+2 |
| __運輸省__ | 企業以外 | 鉱物800 レアクリ100 | エネ5 レアクリ1 | 550 | 交易保護値+3 交易価値+10%	行政官+1 官僚+2 |
| __流通搬送本部__ | 企業のみ | 鉱物800 レアクリ100 | エネ5 レアクリ1 | 550 | 交易保護値+5 交易価値+10% 支社価値+10%	役員+1 管理職+2 |
| __産業省__ | 企業以外 | 鉱物800 エキゾガス100 | エネ5 エキゾガス1 | 550 | 労働者生産量+5%	行政官+1 官僚+2 |
| __製造技術本部__ | 企業のみ | 鉱物800 エキゾガス100 | エネ5 エキゾガス1 | 550 | 研究力+5%	役員+1 管理職+2 |
| __議事堂__ | 企業以外 | 鉱物900 | エネ3 | 500 | 代弁者+1 官僚+2 |
| __株主総会議場__ | 企業のみ | 鉱物900 | エネ3 | 500 | 代弁者+1 管理職+2 |
| __帝国裁判所__ | 企業以外 | 鉱物900 | エネ3 | 500 | 犯罪度-20 安定度+10	行政官+1 法曹+2 |
| __本社査問会議場__ | 企業のみ | 鉱物900 | エネ3 | 500 | 犯罪度-20 安定度+10	役員+1 法曹+2 |
| __中央準備銀行__ | 企業以外 | 鉱物800 レアクリ100 | エネ5 レアクリ1 | 550 | エネルギー算出+10%	行政官+1 銀行家+2 |
| __企業資産管理本部__ | 企業のみ | 鉱物800 レアクリ100 | エネ5 レアクリ1 | 550 | エネルギー算出+10% 交易価値+5%	役員+1 銀行家+2 |
| __参謀本部__ | 企業以外 | 鉱物800 揮発粉100 | エネ5 揮発粉1 | 550 | 宇宙軍移動速度+5% 射程+5%	将官+1 将校+2 |
| __企業警備作戦本部__ | 企業のみ | 鉱物800 揮発粉100 | エネ5 揮発粉1 | 550 | 宇宙軍移動速度+5% 射程+5%	将官+1 将校+2 |
| __中央放送局__ |  | 鉱物800 レアクリ100 | エネ3 レアクリ1 | 550 | 統治志向魅力+15%	代弁者+1 ジャーナリスト+2 |
| __帝国記録保管庫__ |  | 鉱物700 エキゾガス200 | エネ3 エキゾガス2 | 550 | 科学総裁+1 データ司書+2 |
| __医薬基盤研究所__ |  | 鉱物1000 | エネ5 | 550 | Pop成長速度+5% リーダー寿命+10年	科学総裁+1 医療従事者+4 |

### __〇 惑星に一つ__
1. 惑星データバンク	なし	データ司書+1 研究者+1	物質主義のみ	維持:エネ3 エキゾガス1	建設:鉱物600 エキゾガス200 合金100 時間650
2. 帝国図書館	なし	データ司書+2	君主制のみ	維持:エネ3 エキゾガス1	建設:鉱物600 エキゾガス200 合金100 時間650
3. 労働福祉センター	20Popあたりにサービス職+1	官僚+1 事務員+2 サービス職+4	維持:エネ3 消費財2	建設:鉱物800 レアクリ200 時間500
4. 公安局	暗号力+5 30Popあたりに法務執行官+1	官僚+1 法務執行官+2 公安職員+2	維持:エネ3 揮発粉1	建設:鉱物900 揮発粉200 時間600
5. 任意労働監督署	20Popあたりに強制労働者+1	官僚+1 強制労働者+10	権威主義のみ	維持:エネ3 揮発粉1	建設:鉱物900 揮発粉200 時間600
6. 開発植民銀行	30Popあたりに開拓者+1	銀行家+2	維持:エネ3 エキゾガス1	建設:鉱物900 エキゾガス200 時間600
7. イノベーションセンター	20Popあたりに事務員+1	役員+1 起業家+2 管理職+2 事務員+5	(様々なアイデアを支援し 起業や特許取得を支援する施設)平等主義のみ	維持:エネ3 レアクリ1	建設:鉱物900 レアクリ200 時間600
8. 管区軍司令部	なし	将官+1 将校+2	維持:エネ3 揮発粉1	建設:鉱物900 揮発粉200 時間600
9. 入境管理局	流入魅力+30%	官僚+1 事務員+3	維持:エネ3 エキゾガス1	建設:鉱物900 エキゾガス200 時間600
10. 移民推進局	流出圧力+50%	官僚+1 事務員+3	維持:エネ3 エキゾガス1	建設:鉱物900 エキゾガス200 時間600
11. 出境管理局	流出圧力-30%	官僚+1 事務員+3	維持:エネ3 エキゾガス1	建設:鉱物900 エキゾガス200 時間600
12. プレジデンシャルオフィス	20Popあたりに事務員+1	役員+2 管理職+2 法曹+2 事務員+5	(高度な知識やアイデアを生かして活動する人々のためのオフィス)	維持:エネ3 レアクリ1	建設:鉱物900 レアクリ200 時間600
13. 運輸通信管制局	なし	官僚+1 インフラ技師+2	維持:エネ3 レアクリ2	建設:鉱物600 レアクリ200 合金100 時間650
14. 総合大学	なし	科学総裁+1 教授職+2 研究者+2 文化人+2	維持:エネ3 エキゾガス2	建設:鉱物600 エキゾガス200 合金100 時間650
15. 安全思想教育センター	統治志向魅力+20%	官僚+1 公安職員+2 強制労働者+3	権威主義のみ	維持:エネ3 レアクリ1	建設:鉱物600 レアクリ100 合金100 時間650
16. 社会多様性センター	受容志向魅力+20%	官僚+1 文化人+3	受容主義のみ	維持:エネ3 レアクリ1	建設:鉱物600 レアクリ100 合金100 時間650
17. 異民族審判所	犯罪度-20%	官僚+1 文化人+1 法曹+2	排他主義のみ	維持:エネ3 レアクリ1	建設:鉱物600 レアクリ100 合金100 時間650
18. 放送局	安定度+5 幸福度+5%	ジャーナリスト+2 文化人+1	維持:エネ3 レアクリ1	建設:鉱物600 レアクリ100 合金100 時間650

### __〇 個数限定なし__
1. スラム	労働者幸福度-10% 住宅+30	サービス職+1 事務員+2	維持:エネ1	建設:鉱物300 時間100	
2. 大規模高層住宅	住宅+20	サービス職+3 事務員+3	維持:エネ6 消費財1	建設:鉱物700 時間500
3. 高級住宅街	住宅+10 統治者幸福度+20% 快適度+5%	サービス職+3 事務員+3 法務執行官+1	維持:エネ4 消費財2	建設:鉱物400 レアクリ50 時間700
4. 歓楽街	労働者幸福度+5% 快適度+5%	エンターテイナー+4 文化人+1	精神主義以外	維持:エネ6 消費財2	建設:鉱物600 時間500
5. 刑務所	犯罪度-5%	法務執行官+2 法曹+1	維持:エネ2 合金1	建設:鉱物600 合金100時間500
6. 強制収容所	犯罪度-10% 統治志向魅力+10% 幸福度-5%	官僚+1 法務執行官+2 強制労働者+10	権威主義のみ	維持:エネ2 合金1	建設:鉱物600 時間500
7. 専門学校	なし	研究者+1 法曹+1 医療従事者+1 文化人+1	物質主義のみ	維持:エネ3 エキゾガス1	建設:鉱物400 エキゾガス100 合金100 時間650	
8. 高級ホテル	流入魅力+10% 住宅+5 快適度+5%	エンターテイナー+2 サービス職+2	受容主義のみ	維持:エネ4 消費財3	建設:鉱物300 合金50 レアクリ100 時間800
9. 報道ステーション	なし	ジャーナリスト+1 事務員+2	維持:エネ2 レアクリ1	建設:鉱物500 レアクリ50 合金50 時間550
10. 法律事務所	なし	法曹+1 事務員+2	維持:エネ2 揮発粉1	建設:鉱物500 揮発粉50 時間550
11. 砲兵空軍基地	防衛軍与ダメージ+10% 防衛軍指揮ダメージ+10%	将校+1 兵士+2	
12. 廃棄物処理施設	居住性-5% 幸福度+5%	事務員+1 サービス職+3	維持:エネ3 揮発粉1	建設:鉱物900 揮発粉200 時間600
13. 自動防衛設備	防衛軍与ダメージ+30%	なし	軍国主義のみ	維持:エネ1 合金2 揮発粉1	建設:鉱物400 合金50 揮発粉200 時間300
14. 対爆壕	惑星の荒廃度-20% 防衛軍耐久度+10%	兵士+1	平和主義のみ	維持:エネ1 合金1 揮発粉1	建設:鉱物400 合金100 揮発粉100 時間100
15. 対宙ミサイル施設	軌道上の艦隊に与ダメージ	将校+1 兵士+1	維持:エネ2 合金2 揮発粉1	建設:鉱物300 合金200 揮発粉200 時間450
16. 市街地調整地域（鉱物300・維持費エネルギー1）（事務員+2 企業建築物スロット+2）
17. 惑星規模産業調整地域（鉱物500・維持費エネルギー3）（事務員+4 企業建築物スロット+4）

### __〇 企業用__
1. 社会福祉法人（社会の弱者に対して福祉サービスを提供する税制優遇のある法人）  
企業国家の外交発言力+5%。惑星の幸福度+5%。医療従事者+1 サービス職+3  
2. 行列のできる法律事務所（行列ができるほど凄腕の法律家が在籍する法律事務所）  
企業国家の統合力+10。惑星の安定度+5 犯罪度-5%。法曹+1 事務員+2  
3. 高度有機農園（オーガニック生産に気を使った高級志向の農園）  
企業国家の食料+5 消費財+5。惑星の快適度+10。酪農家+1 農家+2  
4. 惑星間通信社（惑星間の通信と報道を行う民間企業）  
企業国家の統合力+10 支社の価値+10%。惑星の安定度+5 交易価値+5%。ジャーナリスト+1 事務員+2  
5. イノベーティブコーポ（イノベーティブなアイデアでハイパフォーマンスのリザルトにコミットメントするコーポ）  
企業国家の支社の価値+10%。惑星の交易価値+10。起業家+1 事務員+2  
6. 貯蓄銀行（市民の貯蓄資産を低利率だが安全に運用する金融機関）  
企業国家のエネルギー+10 支社の価値+5%。惑星の交易価値+5%。銀行家+1 事務員+2  
7. 惑星造船所（惑星に根差した民間船や軍艦を造る船舶企業）  
企業国家の造船速度+5%。惑星の合金生産量+5%。造船技師+2  
8. 惑星工場(惑星に根差した民需品を造る企業)  
企業国家の消費財+20。惑星の消費財生産+5%。職人+1 事務員+2  
9. 銀河旅客運送社（民間船や惑星内輸送機関を運用し 物と者を運ぶ企業）  
企業国家の支社価値+25%。惑星の交易価値+10 交易価値+10%。事務員+1 サービス職+2  
10. 惑星建設組合（惑星における建築と建築資材の調達を行う建設企業）  
企業国家の鉱物+10。惑星の区域と建造物建設速度+5%。インフラ技師+1 事務員+2  
11. 小規模宇宙港（惑星につき1つ）（小規模だが堅実な民間船離発着を行う民間宇宙港）  
企業国家の支社価値+50%。惑星の交易価値+20%。宇宙港管制官+1 サービス職+2  
12. 企業アカデミー（惑星につき1つ）（民間企業が運営する小規模だが高度な人材を輩出する大学）  
企業国家の研究力+5ずつ。惑星の社会学+10。教授職+1 研究者+1  
13. 民間刑務所（惑星につき1つ）（民間企業が惑星政府の委託を受けて治安のために運営する刑務所）  
企業国家のエネルギー+10 鉱物+20。惑星の幸福度-5% 犯罪度-10。法務執行官+1 強制労働者+3  
14. 民間廃棄物処理施設（惑星につき1つ）（民間企業が惑星政府の委託を受けて運営する廃棄物処理施設）  
企業国家のエネルギー+10 消費財+10。惑星の快適度-10 居住性+5%。サービス職+2  