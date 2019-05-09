'use strict';

const e = React.createElement;

class EnterWebsiteButton extends React.Component {
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
  
        return e(
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
        return e("div", {style:{borderStyle:"solid"}}, 
                e("pre", {
                  align: "left" 
                }, this.state.messagefromserver), 
                e("button", {
                    onClick: () => this.setState({ clicked: false }),
                    align: "center" 
                  }, " Close "));
      }
    }
    
    return e(
      'button',
      { onClick: () => this.setState({ clicked: true }) },
      'Open'
    );
  }
}

const domContainer = document.querySelector('#enter_website_button_container');
ReactDOM.render(e(EnterWebsiteButton), domContainer);