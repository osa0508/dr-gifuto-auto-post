# dr-gifuto-auto-post

Instagram（[@dr.gifuto](https://www.instagram.com/dr.gifuto)）へ、
lifecolor-health.com のお役立ちコラムをリライトして毎日自動投稿する仕組みです。

GitHub Actions が毎日 **20:00（日本時間）** に実行され、`queue.json` の中から
まだ投稿していない記事を1件選んで、画像つきでInstagramに投稿します。

## セットアップ（最初の1回だけ）

### 1. Secretsを登録する

**Settings → Secrets and variables → Actions → New repository secret** から2つ登録します。

| Name | Value |
|---|---|
| `IG_ACCESS_TOKEN` | dr.gifuto のアクセストークン |
| `IG_USER_ID` | `17841476853761246` |

### 2. GitHub Pagesを有効にする

**Settings → Pages** で、Source を `Deploy from a branch`、Branch を `main` / `/ (root)` にして保存します。
数分で `https://osa0508.github.io/dr-gifuto-auto-post/` が使えるようになります。

### 3. 手動で1回試す

**Actions → Daily Instagram Post → Run workflow** で1回実行し、dr.gifuto に投稿されるか確認します。

## 日々の運用

- 投稿のたびに `queue.json` の該当記事が `posted: true` になります。
- 投稿のあと、トークンの有効期限（60日）を自動で延長します。トークンはログに出しません。
- ネタが切れたら、`build_queue.py` の `POSTS` に記事を追加して実行し、
  できた画像と `queue.json` をアップロードします（既存の `posted` の状態は手で引き継いでください）。

## ファイル構成

```
queue.json                  … 投稿予定の記事（キャプション・画像・投稿済みフラグ）
post-XXX.jpg                … アイキャッチ画像
post_daily.py               … 次の記事を投稿するスクリプト
generate_eyecatch.py        … アイキャッチ画像の生成
build_queue.py              … 記事データから queue.json と画像を作る
.github/workflows/daily-post.yml … 毎日の自動投稿
```
