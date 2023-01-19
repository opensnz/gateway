const sqlite3 = require('sqlite3').verbose();
const SQLITE_DATABASE_PATH = "../SQLite/devices.db";
// open the database
let db = new sqlite3.Database(SQLITE_DATABASE_PATH, sqlite3.OPEN_READWRITE, (err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Connected to database.');
});

db.serialize(() => {
  db.each(`SELECT * FROM DEVICE`, (err, rows) => {
    if (err) {
      console.error(err.message);
    }
    console.log(rows);
  });
});

db.close((err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Close the database connection.');
});