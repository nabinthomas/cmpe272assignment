import * as cookies from '/static/scripts/cookies.js';

'use strict';

const createElement = React.createElement;

class LogoutLink extends React.Component {
    constructor(props) {
      super(props);
      this.state = { 
        logged_in: false, 
      };
    }
  
  
    componentDidMount() {
      // TODO: Validate Cookie
      // console.log("Cookie read " + getCookie('auth_token'))
      if (cookies.getCookie('auth_token') != ""){
        this.setState({ logged_in: true });
      }
    }
    render() {
      if (this.state.logged_in) {
        var signoutString = 'Sign out ' + cookies.getCookie('userFullName') + '(' + cookies.getCookie('userEmailId') + ')';
        signoutString = 'Sign out';
        return createElement(
          'a',
          { 
            href : '/logout'
          },
          signoutString
        );
      }
      else {
          return createElement('div');
      }
    }
  }
  
  class ProfilePicture extends React.Component {
    constructor(props) {
      super(props);
      this.state = { 
        hasPicture: false, 
      };
    }
  
  
    componentDidMount() {
      // TODO: Validate Cookie
      // console.log("Cookie read " + getCookie('auth_token'))
      if (cookies.getCookie('userPicture') != ""){
        this.setState({ hasPicture: true });
      }
      else {
        this.setState({ hasPicture: false });
      }
    }
    render() {
      if (this.state.hasPicture) {
        var pictureUrl = cookies.getCookie('userPicture');
        
        return createElement(
          'img',
          { 
            style: {
              float : 'right',
              margin: '15px 15px 15px 15px'
            },
            src : pictureUrl,
            width : "24",
            height : "24"
          }
        );
      }
      else {
          return createElement('div');
      }
    }
  }
  // const domContainer = document.querySelector('#enter_website_button_container');
  // ReactDOM.render(createElement(RestAPITestButton), domContainer);
  
  const logout = document.querySelector('#logout_button');
  if (logout)
    ReactDOM.render(createElement(LogoutLink), logout);

  const profilePic = document.querySelector('#profilePic');
  if (profilePic)
    ReactDOM.render(createElement(ProfilePicture), profilePic);