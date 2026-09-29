#!/bin/bash
# ============================================
# Skill 发布助手 · publish.sh
# 作用：把桌面仓库同步到 GitHub，可选打包小红书 zip
# 用法：
#   ./publish.sh "更新说明"         → 提交 + 推送 GitHub
#   ./publish.sh "更新说明" --zip   → 额外把 interview-coach 打包成小红书上传包
# ============================================
set -e
cd "$(dirname "$0")"

MSG="${1:-update skills}"

echo "==> 1/2 提交并推送 GitHub ..."
git add -A
if git commit -m "$MSG"; then
  git push
  echo "✅ GitHub 已更新"
else
  echo "ℹ️ 没有新改动，跳过 push"
fi

if [ "$2" = "--zip" ]; then
  echo "==> 2/2 打包小红书上传包 ..."
  VERSION=$(date +%Y%m%d)
  (cd interview-coach && zip -rq "../面试陪练-redskill-v${VERSION}.zip" .)
  echo "✅ 已打包：面试陪练-redskill-v${VERSION}.zip（去小红书创作平台手动上传）"
else
  echo "==> 2/2 未指定 --zip，跳过打包"
fi
