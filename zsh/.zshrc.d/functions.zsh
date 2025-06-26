# $1: port number
who_uses_port() {
  local TMP_FILE="/tmp/$0"
  ss -lptn "sport = :$1" | tee $TMP_FILE
  local PID=$(cat $TMP_FILE | sed -n -e 's/^.*pid=\([0-9]\+\).*$/\1/p' | uniq | tr '\n' ' ' | sed 's/ *$//g')

  test -z $PID && return
  echo "Do you want to kill the following process(es): $PID ? (y|n)"
  read RESPONSE
  if [[ $RESPONSE == 'y' ]]; then
    for p in $PID; do
      kill -9 $p
      done
  fi
}


# $1: Database name
# $2: Database user
kill_all_pg_conn() {
  local db_name="$1"
  local db_user="${2:-postgres}"
  psql -U "$db_user" -d "$db_name" -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$db_name' AND pid <> pg_backend_pid();"
}

