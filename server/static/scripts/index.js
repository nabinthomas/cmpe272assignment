'use strict';

const e = React.createElement;

class EnterWebsiteButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { clicked: false };
  }

  render() {
    if (this.state.clicked) {
      return 'Loading Shopping site.. Please Wait...';
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