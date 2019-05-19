import * as cookies from '/static/scripts/cookies.js';
'use strict';

var auth_token = cookies.getCookie('auth_token');

if (auth_token == "")
    window.location.href = '/'