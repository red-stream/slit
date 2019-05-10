LOGO="[SLIT]"

RET_POSIX_SHELL="FALSE"
if [ "`echo $POSIXLY_CORRECT`" != "" ]; then
    RET_POSIX_SHELL="TRUE"
fi

printf "%s --------- SYSTEM CONFIG ------\n" "$LOGO"
printf "%s SHELL: %s\n" "$LOGO" "`ls -al /bin/sh | awk '{print $NF}'`"
printf "%s POSIX SHELL: %s\n" "$LOGO" "$RET_POSIX_SHELL"
printf "%s LONG BIT: %s\n" "$LOGO" "`getconf LONG_BIT`"
printf "%s EDITOR: %s\n" "$LOGO" "$EDITOR"

