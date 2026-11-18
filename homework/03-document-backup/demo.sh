#!/bin/sh
set -eu
run() {
  printf '$ %s\n' "$*"
  "$@"
}
run python3 scenario.py reset
run python3 backup.py create work T0.zip
run python3 scenario.py stage1
run python3 backup.py create work T1.zip
run python3 scenario.py stage2
run python3 backup.py create work T2.zip
run python3 backup.py restore T0.zip restored-T0
run python3 backup.py restore T1.zip restored-T1
run diff -qr initial_documents restored-T0
for name in 'Кадры/документ_002.txt' 'Договоры/документ_003.txt' 'Финансы/новая_смета.txt'; do
  case "$name" in Кадры/*) version=T0 ;; *) version=T1 ;; esac
  test ! -f "work/$name"
  test -f "restored-$version/$name"
  printf '%s восстановлен из %s\n' "$name" "$version"
done
head -c 90 T0.zip > damaged.zip
if run python3 backup.py restore damaged.zip rejected; then exit 1; fi
test ! -e rejected
printf 'Повреждённый архив отклонён. Папка восстановления не создана.\n'
