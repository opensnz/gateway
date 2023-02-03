#################### SQLite installation #####################
# 0. Update the source list
sudo apt update
# 1. Install SQLite
sudo apt install sqlite3 -y

# 2. Check SQLite version
echo "sqlite3 version:"
sudo sqlite3 --version

# 3. Database directory
DIR=./SQLite
if [ -d "$DIR" ];
then
    echo "$DIR directory exists."
else
	sudo mkdir $DIR
    echo "$DIR directory created."
fi