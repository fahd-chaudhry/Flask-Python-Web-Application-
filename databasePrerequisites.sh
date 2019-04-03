#!/bin/sh

#check if database exists or not
database()
{
sudo mysql -u root <<EOF
DROP DATABASE GSWTechDemoFlask;
EOF
}

#surpress output so that less output is displayed when provisioning
database > /dev/null 2>&1

#for some reason this script doesn't return exit code = 0, therefore we habve to do it manually
exit 0
