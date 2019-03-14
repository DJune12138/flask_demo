#! /bin/bash

. ./functions.sh

SVN_URL="svn://192.168.0.10:3695/php/"
TRUNK="zs_backend/"
TAGS="tags/"

UPLOAD_SVN_URL="svn://120.79.78.35/api/"
UPLOAD_SVN_USER="lkhua"
UPLOAD_SVN_PASSWD="zslm@#$lkh"
DEST_PATH="/tmp/pub/"

SQL_UPLOAD_SVN_URL="svn://120.79.78.35/SQL/"
SQL_DEST_PATH="/tmp/pub_sql/"

## 切版本
new_tag()
{
	VERSION="v"$1
	echo "creating new tag: "$VERSION
	echo "from:"${SVN_URL}${TRUNK}
	echo "to:"${SVN_URL}${TAGS}${VERSION}
	svn copy ${SVN_URL}${TRUNK} ${SVN_URL}${TAGS}${VERSION} -m "create tags by script"
}

## 打包
pack()
{
	VERSION="v"
	TYPE="admin"

	while [ $# -ne 0 ] ; do
	    PARAM=$1
	    echo ${PARAM}
	    shift
	    case ${PARAM} in
	        --) break ;;
	        -v) VERSION=${VERSION}$1; shift ;;
            -p) DEST_PATH=$1; shift ;;
			-t) TYPE=$1; shift ;;
	    esac
	done

	SRC_DIR=`mktemp -d`
	echo "SRC_DIR:"${SRC_DIR}

	cd ${SRC_DIR}
	if [ ${VERSION} = "v" ]; then
		svn export ${SVN_URL}${TRUNK} ./ --force
		SVN_VERSION=`svn info ${SVN_URL}${TRUNK} |grep Revision | awk -F\: '{print $2}'`
	else
		svn export ${SVN_URL}${TAGS}${VERSION} ./ --force
		SVN_VERSION=`svn info ${SVN_URL}${TAGS}${VERSION} |grep Revision | awk -F\: '{print $2}'`
	fi

	echo `date +"%x %T"`${SVN_VERSION} > version

    if [ ${TYPE} = "admin" ]; then
    	ZIPNAME="admin-`date "+%Y%m%d%H%M"`"
		zip -r ./${ZIPNAME}.zip zs_backend config scripts manage.py readme start uwsgi.ini version game.sql admin.sql
	elif [ ${TYPE} = "tj" ]; then
		ZIPNAME="tj-`date "+%Y%m%d%H%M"`"
		rm -f tj/base_stat.py
		zip -r ./${ZIPNAME}.zip tj version crontab
	elif [ ${TYPE} = "sql" ]; then
		ZIPNAME="sdb-`date "+%Y%m%d%H%M"`"
		zip -r ./${ZIPNAME}.zip sql/update.sql
	else
		ZIPNAME="api-`date "+%Y%m%d%H%M"`"
		rm -fr zs_backend/busi zs_backend/static zs_backend/templates zs_backend/api tj
		zip -r ./${ZIPNAME}.zip zs_backend scripts manage.py readme start uwsgi.ini version config
	fi

	## 查看svn信息
	mkdir -p ${DEST_PATH}
	mkdir -p ${SQL_DEST_PATH}
	cd ${DEST_PATH}
    if [ -d ${DEST_PATH}/.svn ]; then
        svn up
    else
        svn co ${UPLOAD_SVN_URL} ./ --username lkhua --password 'zslm@#$lkh' --non-interactive
    fi
    cd ..

    cd ${SQL_DEST_PATH}
    if [ -d ${SQL_DEST_PATH}/.svn ]; then
        svn up
    else
        svn co ${SQL_UPLOAD_SVN_URL} ./ --username lkhua --password 'zslm@#$lkh' --non-interactive
    fi
    cd ..

    if [ ${TYPE} = "admin" ]; then
    	cd ${DEST_PATH}/admin
    elif [ ${TYPE} = "tj" ]; then
    	cd ${DEST_PATH}/tj
    elif [ ${TYPE} = "sql" ]; then
    	cd ${SQL_DEST_PATH}/sdb
    else
    	cd ${DEST_PATH}/api
    fi

    mv ${SRC_DIR}/${ZIPNAME}.zip ${ZIPNAME}.zip
    rm -fr ${SRC_DIR}

    echo `md5sum ${ZIPNAME}.zip | awk '{print $1}'` > ${ZIPNAME}.md5
    svn add ${ZIPNAME}.zip
    svn add ${ZIPNAME}.md5
    svn commit -m "==*Game-Script Execute*==Pre_Pub"

    echo "pub succ ${ZIPNAME}.zip"
}

ACTION=$1
shift
case ${ACTION} in
    'new') new_tag $@;;
	'pack') pack $@;;
    *) usage; exit 1;;
esac
