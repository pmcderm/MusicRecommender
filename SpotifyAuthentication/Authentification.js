const express = require('express');
const crypto = require('crypto');
const querystring = require('querystring');
const client_id = 'f84481c403ec4569a9ee6ab6959629e6';
const redirect_uri = 'http://localhost:8888/callback/';
const client_secret = '4997dd3a43ee41adbf7b3d87c1e9479a'
const port = 8888

const app = express();

app.get('/login', function(req, res) {

  var state = crypto.randomBytes(16).toString('hex');
  var scope = `user-read-recently-played \
  user-read-playback-position \
  user-top-read \
  playlist-read-collaborative\
  playlist-modify-public\
  playlist-read-private\
  playlist-modify-private\
  user-library-modify\
  user-library-read`;

  res.redirect('https://accounts.spotify.com/authorize?' +
    querystring.stringify({
      response_type: 'code',
      client_id: client_id,
      scope: scope,
      redirect_uri: redirect_uri,
      state: state
    }));
});

app.get('/callback', function(req, res) {

    var code = req.query.code || null;
    var state = req.query.state || null;
  
    if (state === null) {
      res.redirect('/#' +
        querystring.stringify({
          error: 'state_mismatch'
        }));
    } else {
      var authOptions = {
        url: 'https://accounts.spotify.com/api/token',
        form: {
          code: code,
          redirect_uri: redirect_uri,
          grant_type: 'authorization_code'
        },
        headers: {
          'Authorization': 'Basic ' + (new Buffer(client_id + ':' + client_secret).toString('base64'))
        },
        json: true
      };
      res.send(authOptions);
    }
  });

// Put into Python
app.get('/refresh_token', function(req, res) {

  var refresh_token = req.query.refresh_token;
  var authOptions = {
    url: 'https://accounts.spotify.com/api/token',
    headers: { 'Authorization': 'Basic ' + (new Buffer(client_id + ':' + client_secret).toString('base64')) },
    form: {
      grant_type: 'refresh_token',
      refresh_token: refresh_token
    },
    json: true
  };

  request.post(authOptions, function(error, response, body) {
    if (!error && response.statusCode === 200) {
      var access_token = body.access_token;
      res.send({
        'access_token': access_token
      });
    }
  });
});
app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
  })