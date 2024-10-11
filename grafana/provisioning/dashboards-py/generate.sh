DIRECTORY=silly

mkdir $DIRECTORY

for file in *.dashboard.py; do
  # a file name looks like "example.dashboard.py"
  FILE_NAME=$(basename "$file")
  # the dashboard name is the first value before the ".", i.e. "example"
  DASHBOARD_NAME=$(echo "$FILE_NAME" | cut -d '.' -f 1)

  generate-dashboard -o $DIRECTORY/$DASHBOARD_NAME.json $FILE_NAME
done
