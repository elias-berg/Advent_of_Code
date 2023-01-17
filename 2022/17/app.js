var express = require('express');
var path = require('path');
var ejs = require('ejs');

const app = express();
const port = 8080;

app.set('views', path.join(__dirname, 'views'));
app.engine('html', ejs.renderFile);
app.set('view engine', 'html');

app.use(express.static(path.join(__dirname, 'dist')));
app.use(express.static(path.join(__dirname, 'inputs')));

app.get('/', (req, res) => {
  res.render('index', {}); // Render the engine-type of file with the name index (index.html)
});

app.listen(port, () => {
  console.log(`Listening on port ${port}`)
});