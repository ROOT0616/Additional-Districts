# Additional Districts And Buildings 2.0.0-beta.3

対象: Stellaris 4.5.2 (9776)。4.5.* 表記はLauncher用であり、将来の4.5パッチまで動作保証するものではありません。

これは3.11対応版1.25.16からの移植β版です。静的検査に加え、Steam→Paradox Launcher経由で4.5.2のメインメニュー到達を確認しました。起動ログから文字コード・必須区画・上限modifier・旧scope/参照・不足アイコンを修正しています。新規銀河とゲーム進行の検証は未完了です。詳細はRUNTIME_VALIDATION.mdを参照してください。

## 変更

- 独自区域34種、建造物93種、職業50種、技術4種のIDを維持。
- 職業枠・住居・快適度と人口条件を4.xの100倍単位へ変換。職業の資源産出・維持費は100労働力あたりの元の値を維持。
- 旧研究者・計算機の枠を、物理・生物・工学の現行3職へ分配。整数枠の合計は維持。
- 旧executive/manager/high_priest/head_researcher/priest/merchantの枠は、現行の就業可能なpolitician/bureaucrat/traderへ移行。名称・条件が旧版と完全一致するものではありません。
- 旧交易価値の固定産出をtrade資源産出へ、職業交易補正を現行経済modifierへ移行。
- 人口数判定をcount_owned_pop_amountへ、軍隊のPOP判定をany_owned_pop_groupへ移行。
- 職業UI情報をswappable_dataへ移行。旧職業割当を前提とするhas_jobの重み付けと、廃止research_leader参照を除去。
- 成長速度補正を現行logistic_growth_multへ変更。旧成長計算との数値的な同等性は保証しません。
- 初期化はglobal event additionaldistricts.9000から銀河全体の生成effectを一度だけ実行。旧.01と.1の数値ID重複、およびglobal scopeからのcountry_event呼出しを解消。
- 区画整備イベントの支払いをownerのcountry scopeへ修正。
- 惑星画面の3.11全体上書きを廃止し、4.5の標準画面を使用。
- AD都市区域の建造物枠は独自zone/zone_slotへ移植。区域数に応じて1/2/3枠ずつ開放し、区画ごとの上限は現行Vanillaに合わせて6枠。旧惑星全体36枠とは異なります。
- 旧惑星特化の全体複製を撤去。資源特化3定義だけ4.5.2実定義にAD区域のAI重みを追加。
- 惑星防衛艦の不一致なセクション・武器スロットを、独自セクションの12小型ミサイルスロットへ修正。リアクターと戦闘コンピュータを追加。戦闘挙動は未検証。
- 英語localizationの壊れた行と、廃止交易アイコンを修正。独自区画の日本語・英語名を追加。

## 今回含めない旧機能

- 旧36惑星建造物枠・8支社枠のglobal define上書き。支社枠を増やす個別建造物補正は現行branch_office_target_max_buildings_addへ移行しています。
- 廃止された交易路収集距離・交易路保護のmodifier。これらだけを持っていた星系基地モジュールには現在実益がないものがあります。
- 廃止された移民流入・流出圧力modifier。関連施設の他の効果は残っています。
- Planetary Diversity等の他MOD専用惑星クラス列挙。対象MODの現行実ファイルがないため旧参照を除外しました。独立した互換パッチは含みません。
- Gigastructural Engineering 3.11への固定依存指定。独自区域等の基本機能にその依存は不要ですが、現行Gigastructuresとの併用互換は未確認です。

旧効果を削除・再設計した箇所があるため、元の機能を完全再現した正式版ではありません。これらを維持するには、現行システムに合わせた追加設計・実機確認が必要です。

## Vanilla override・競合

定義を上書きするのは `col_mining`、`col_generator`、`col_farming` の3つです。4.5.2の本体定義を基準にしています。同じ惑星特化を変更するMODと競合します。

`on_press_begin` と `on_planet_bombarded` にイベントを追加します。4.5.2実ファイルを基準にinterface/planet_view.guiとinterface/colonize_planet_view.guiを上書きします。区域一覧のスクロール対応のためであり、同じGUIを変更するMODと競合します。replace_path、global define上書きはありません。イベントnamespaceはadditionaldistrictsを維持しているため、旧版との同時有効化は禁止です。

## 導入とセーブ

ZIP内のAdditionalDistrictsフォルダとAdditionalDistricts.modを、ユーザーのStellaris/modフォルダへ配置してください。Launcher用.modのpathは `mod/AdditionalDistricts` です。別の場所から読み込む場合は、そのコピーのpathを変更します。

3.11からのセーブ移行は非対応です。新規ゲームを必須とし、旧セーブに導入しないでください。4.5.2の既存セーブも区域の初期生成・職業・区画移行を確認できていないため対象外です。削除時には独自IDの参照がセーブに残ります。

## 検証手順

1. 本MOD単独で新規銀河を作成し、error.logの最初のparser/script errorを確認。
2. 開始時にADデポジットが生成され、生成が重複しないことを確認。
3. 一般帝国・集合意識・機械帝国で区域建設と職業割当を確認。100枠あたりの資源・住居・快適度を確認。
4. 4技術を取得し、区画整備と撤去が実行でき、所有国家から費用が引かれることを確認。
5. 都市区域を複数建設し、追加区画の1/2/3枠ずつの開放と上限6枠、建造物選択・建設を確認。
6. 建造物、星系基地、支社を確認。交易を受け取る国家と、条件付き産出を重点確認。
7. 軌道爆撃で防衛艦生成・艦隊所有者・戦闘・生成数を確認。
8. 20年以上進め、AIの区域・建造物・技術選択を確認。
9. セーブして再ロードし、区域・区画・職業と初期化の非再実行を確認。

未確認: 上記実機項目、経済バランス、3研究職への再配分、成長計算、独自職への特化補正、区画GUI、他MOD併用。次の作業は4.5.2での起動確認と、error.logに基づく修正です。

根拠: 提供Vanilla_common.zipとインストール済み4.5.2。対象の区域・職業・惑星特化・zone・zone_slot関連133ファイルは内容一致を確認。本体出力のscript_documentationでtrigger/effect/modifierも照合しました。
