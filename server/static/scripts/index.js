import * as cookies from '/static/scripts/cookies.js';

'use strict';

const createElement = React.createElement;

class RestAPITestButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
      clicked: false, 
      needs_ui_update: false,
      messagefromserver: "Click to see help"
    };
  }

  render() {
    if (this.state.clicked) {
      if (!this.state.needs_ui_update) {
        // There is no pending request. So start a request to REST server
        this.state.messagefromserver = ""
        fetch("/api")
        .then(serverresponse => {
          console.log(serverresponse);
          return serverresponse.json();
        }).then (data => {
          console.log("The response from server was : ");
          console.log("******************************\n");
          console.log(data['response']);
          console.log("The status from server was : ");
          console.log("******************************\n");
          console.log(data['status']);
          console.log("The response.message from server was : ");
          console.log("******************************\n");
          console.log(data['response']['message']);
          console.log("******************************\n");
          this.state.messagefromserver = "";
          for (var line in data['response']['message']){
            this.state.messagefromserver +=  (data['response']['message'][line] + "\n");
          }
          
          // Trigger a re-rendering with the new data
          this.setState({needs_ui_update:true}); 
        })
  
        return createElement(
          'div', 
          {
             onClick: () => this.setState({ clicked: false }), 
             align: "center"
          },
          'Loading Data...'  
        );
      }
      else {
        // update UI with new results and reset flag
        this.state.needs_ui_update = false;
         // e is same as React.createElement as defined earlier
        return createElement("div", {style:{borderStyle:"solid"}}, 
                createElement("pre", {
                  align: "left" 
                }, this.state.messagefromserver), 
                createElement("button", {
                    onClick: () => this.setState({ clicked: false }),
                    align: "center" 
                  }, " Close "), 
                  createElement('a', {
                      href: "http://localhost/mongo"
                    }, "Mongo"));
      }
    }
    
    return createElement(
      'button',
      { onClick: () => this.setState({ clicked: true }) },
      'Open'
    );
  }
}

class EnterWebsiteLink extends React.Component {
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
          href:"/books"
        },
        'Shop for Books'
      );
    }
    else {
      return createElement(
        'a',
        { 
          href:"https://nthomas.auth0.com/authorize?response_type=code&client_id=QN3TAKTeDu4U4i6tfVI2JCs7hXSxdePG&redirect_uri=http://localhost/api/loginsuccess&scope=openid%20profile%20email&state=xyzABC123"
        },
        'Login'
      );
    }
  }
}

// const domContainer = document.querySelector('#enter_website_button_container');
// ReactDOM.render(createElement(RestAPITestButton), domContainer);

const domContainer = document.querySelector('#enter_website_button_container');
ReactDOM.render(createElement(EnterWebsiteLink), domContainer);