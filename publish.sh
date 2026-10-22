#!/bin/bash
# ============================================
# Skill 发布助手 · publish.sh
# 作用：把桌面仓库同步到 GitHub，可选打包小红书 zip
# 用法：
#   ./publish.sh "更新说明"                        → 提交 + 推送 GitHub
#   ./publish.sh "更新说明" --zip                  → 提交推送 + 打包全部 skill
#   ./publish.sh "更新说明" --zip interview-coach → 只打包指定 skill
# ============================================
set -e
cd "$(dirname "$0")"

MSG="${1:-update skills}"
ONLY="${3:-}"          # 可选：只打包这一个 skill 的目录名
ROOT="$(pwd)"

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

  if [ -n "$ONLY" ]; then
    TARGETS="skills/$ONLY"
  else
    TARGETS=$(find skills -mindepth 1 -maxdepth 1 -type d | sort)
  fi

  for d in $TARGETS; do
    name=$(basename "$d")
    # zip 打在 skills/ 的同级（即仓库根），避免 cd 后的相对路径歧义
    out="${ROOT}/${name}-redskill-v${VERSION}.zip"
    rm -f "$out"
    (cd "$ROOT/$d" && zip -rq "$out" .)
    echo "  ✅ ${name}-redskill-v${VERSION}.zip"
  done
  echo "✅ 打包完成（去小红书创作平台手动上传）"
else
  echo "==> 2/2 未指定 --zip，跳过打包"
fi