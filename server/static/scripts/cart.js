'use strict';

// When the customer press check out button , the  cart entries in his cart 
// will be used for creating the order , a new Order Id will be assigned to it.
//const element = React.createElement;
class PlaceOrder extends React.Component {
    constructor(props){
        super(props);
        // console.log("Props = " + JSON.stringify(props));
        this.state = {
            CustomerId : props.CustomerId
        };
    }

    handleClick(){
        console.log("Order has been placed");
        // '/api/neworder' , POST 
        // console.log("Button Clicked" + JSON.stringify(buttonId));
        // console.log("state = " + JSON.stringify(this.state));
        // console.log("object = " + this);
        //console.log("Adding to Cart, Book with ISBN = " + this.state.isbn13);
    }
    render(){
        return React.createElement('button', {key:this.props.addButtonId, onClick: () => this.handleClick()},  'PlaceOrder')
    }
}

class CancelOrder extends React.Component {
    constructor(props){
        super(props);
        // console.log("Props = " + JSON.stringify(props));
        this.state = {
            CustomerId : props.CustomerId
        };
    }

    handleClick(){
        console.log("Order has been placed");
        // '/api/neworder' , DELETE 
        // console.log("Button Clicked" + JSON.stringify(buttonId));
        // console.log("state = " + JSON.stringify(this.state));
        // console.log("object = " + this);
        //console.log("Adding to Cart, Book with ISBN = " + this.state.isbn13);
    }
    render(){
        return React.createElement('button', {key:this.props.addButtonId, onClick: () => this.handleClick()},  'CancelOrder')
    }
}

class CartEntriesHeading extends React.Component {
    constructor(props) {
      super(props);
      this.state = { 
        headings : [
            "BookId",
            "QTY" 
        ]
      };
    }

    render() {
        let cells = [];
        for (var i = 0; i < this.state.headings.length; i++){
            cells.push(
                React.createElement('th', {key:i}, this.state.headings[i])
            );
        }
        return React.createElement( 'tr',  null, cells);
    }
}

class CartEntriesData extends React.Component{
    constructor(props) {
        super(props);
        this.state = {  cartEntries : [] };
    }
    componentDidMount() {
        this.setState({books: []});
        console.log("Cart: going to call fetch The response from server was : ");
        fetch("/api/cart/2").then(serverresponse => {
          console.log(serverresponse);
          return serverresponse.json();
        }).then (data => {
          console.log("Cart: The response from server was : ");
          console.log("******************************\n");
          console.log(data['response']);
          console.log("Cart:The status from server was : ");
          console.log("******************************\n");
          console.log(data['status']);
          console.log("Cart:The cart_details from server was : ");
          console.log("******************************\n");
          console.log(data['response']['cart_details']);
          console.log("******************************\n");
          this.state.messagefromserver = ""; 
          
          // Trigger a re-rendering with the new data
          this.setState({cartEntries: data['response']['cart_details'] } ); 
        });
    }

    render() {
        let rows = [];  
        console.log(" cart: this.state.cartEntries.length \n" , this.state.cartEntries.length );
        for (var i = 0; i < this.state.cartEntries.length; i++){
            let cells = [];
            var BookId = `BookId${i}`;
            var QtyId = `qty${i}`;
            console.log(" cart: this.state.cartEntries[" , i , "] \n" , this.state.cartEntries[i] );
            cells.push(React.createElement('td', {key:BookId}, this.state.cartEntries[i]['BookId']));
                cells.push(React.createElement('td', {key:QtyId}, this.state.cartEntries[i]['qty']));
         
            var thisRow = React.createElement(
                'tr',
                {key:`cart_entry_${i}`},
                cells
            );
    
         console.log(cells);
         rows.push(thisRow);
        }
         console.log(rows);
        return rows;
    }
}
 

const cart_list_heading = document.querySelector('#cart_list_heading');
ReactDOM.render(React.createElement(CartEntriesHeading), cart_list_heading);
const cart_list_data = document.querySelector('#cart_list_data');
ReactDOM.render(React.createElement(CartEntriesData), cart_list_data);

 