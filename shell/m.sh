# bash directory bookmark

# 将下列代码保存成 /path/to/m.sh 然后在 .bashrc 里 source /path/to/m.sh ，就可以使用了。

# 0）m + 将当前路径保存为以最后一级目录名称为书签；

# 1）m +foo 将当前路径保存为名称为 foo 的书签，注意加号和名称之间没有空格；

# 2）m -foo 删除名为 foo 的书签，注意减号号和名称之间没有空格；

# 3）m foo 跳转；

# 4）m 列出所有书签；

# 5）m /bar 搜索名字匹配 bar 的书签；

function cd_mark() {
    MARKPATH="${MARKPATH:-$HOME/.local/share/marks}"
    [ -d "$MARKPATH" ] || mkdir -p -m 700 "$MARKPATH" 2> /dev/null
    case "$1" in
        +*)            # m +foo  - add new bookmark for $PWD
            ln -snf "$(pwd)" "$MARKPATH/${1:1}" 
            ;;
        -*)            # m -foo  - delete a bookmark named "foo"
            rm -i "$MARKPATH/${1:1}" 
            ;;
        /*)            # m /bar  - search bookmarks matching "bar"
            find "$MARKPATH" -type l -name "*${1:1}*" | \
                awk -F "/" '{print $NF}' | MARKPATH="$MARKPATH" xargs -I'{}'\
                sh -c 'echo "{} ->" $(readlink "$MARKPATH/{}")'
            ;;
        "")            # m       - list all bookmarks
            command ls -1 "$MARKPATH/" | MARKPATH="$MARKPATH" xargs -I'{}' \
                sh -c 'echo "{} ->" $(readlink "$MARKPATH/{}")'
            ;;
        *)             # m foo   - cd to the bookmark directory
            local dest="$(readlink "$MARKPATH/$1" 2> /dev/null)"
            [ -d "$dest" ] && cd "$dest" || echo "No such mark: $1"
            ;;
    esac
}

# by default, alias cd_mark to m
alias ${MARKCMD:-m}='cd_mark'
