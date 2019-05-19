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
        return createElement(
          'a',
          { 
            href : '/logout'
          },
          'Sign out ' + cookies.getCookie('userFullName') + '(' + cookies.getCookie('userEmailId') + ')'
        );
      }
      else {
          return createElement('div');
      }
    }
  }
  
  // const domContainer = document.querySelector('#enter_website_button_container');
  // ReactDOM.render(createElement(RestAPITestButton), domContainer);
  
  const domContainer = document.querySelector('#logout_button');
  ReactDOM.render(createElement(LogoutLink), domContainer);