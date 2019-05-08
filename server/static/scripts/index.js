'use strict';

const e = React.createElement;

class EnterWebsiteButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { clicked: false };
  }

  render() {
    if (this.state.clicked) {
      var message = 'Loading Shopping site.. Please Wait...';
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
        //let message = data.toString();
      })
      
      return e(
        'button', 
        {
           onClick: () => this.setState({ clicked: false }), 
        },
        message 
      )
    }

    return e(
      'button',
      { onClick: () => this.setState({ clicked: true }) },
      'Enter'
    );
  }
}

const domContainer = document.querySelector('#enter_website_button_container');
ReactDOM.render(e(EnterWebsiteButton), domContainer);