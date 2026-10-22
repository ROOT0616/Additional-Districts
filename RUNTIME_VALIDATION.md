# 4.5.2 実機読み込み検証

実行日: 2026-10-22（日本時間）。本体: Cygnus v4.5.2 (9776)。

Steamの `steam://rungameid/281990` → Paradox Launcher →「プレイ」で起動。
検証用プレイセット「Additional Districts 4.5.2 Test」を作成し、`mod/AdditionalDistricts_local.mod` の1件だけを有効化しました。既存Initial playsetのMOD構成は変更していません。

直接起動時の0xC0000005はMOD原因の根拠にしていません。Steam経由ではメインメニューに到達しました。

実機ログに基づくβ2修正:

- スクリプトのUTF-8 BOMを除去。localizationのBOMは維持。
- 全93建造物にbuilding_setsを追加。支社建造物に不足していたcategoryを追加。
- 全34区域に必須zone_slotsを指定。建造物区画を持たない区域はVanillaのslot_emptyを使用。
- 区域上限を現行の`*_max_add`へ移行し、is_uncappedとshared_capacity_modifierを指定。
- 区域の新UI用背景はVanillaの区域iconを参照。
- 残っていた職業のbuilding_iconをswappable_dataへ移動。
- 廃止されたjob_weights_modifier参照と、precalc名をtriggerとして使う旧処理を除去。
- 惑星decision直下のis_aiをownerのcountry scopeへ修正。
- 旧leader_ageをleader_lifespan_addへ移行。
- 未提供の他MOD専用static modifier参照を除外。
- 支社建造物のhas_building判定をhas_holdingへ移行。
- 旧slave階級判定をis_enslavedへ移行。
- 不足していた職業・modifier・建造物・デポジットの画像に既存AD画像の代替を追加。一部の画像は共通です。

起動ログと静的検査は、経済バランスやプレイ中の動作保証にはなりません。新規銀河生成、初期化イベント、追加区域の表示・建設、職業割当、資源産出、AI、セーブ再ロードは引き続き検証対象です。

Vanilla特化3件（col_mining / col_farming / col_generator）の重複定義通知は、READMEに記載した意図的な上書きです。

最終確認: β2でメインメニュー到達。本体表示 Cygnus v4.5.2、MOD適用後チェックサム3718。error.logは意図した惑星特化3件の重複通知のみ（494 bytes）。構文・scope・定義参照・画像不足エラーなし。新規銀河の検証は未実施。
