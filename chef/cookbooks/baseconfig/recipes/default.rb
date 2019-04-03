# Make sure the Apt package lists are up to date, so we're downloading versions that exist.
cookbook_file "apt-sources.list" do
  path "/etc/apt/sources.list"
end
execute 'apt_update' do
  command 'sudo apt-get -o Acquire::Check-Valid-Until=0 update'
end

# Base configuration recipe in Chef.
package "wget"
package "ntp"
cookbook_file "ntp.conf" do
  path "/etc/ntp.conf"
end
execute 'ntp_restart' do
  command 'service ntp restart'
end

execute 'install_python' do
  command 'apt-get -y install python'
end

execute 'install_pip' do
  command 'apt-get -y install python-pip'
end

execute 'install_flask' do
  command 'pip install flask'
end

execute 'install_python_sql_dependency' do
  command 'sudo apt-get -y install python3.6-dev libmysqlclient-dev'
end

execute 'install_mysql' do
  command 'pip install flask-mysqldb'
end

execute 'install_mysqlserver' do
  command 'apt-get -y install mysql-server libmysqlclient-dev'
end

execute 'install_wtforms' do
  command 'pip install Flask-WTF'
end

execute 'install_passlib' do
  command 'pip install passlib'
end




