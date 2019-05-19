import * as cookies from '/static/scripts/cookies.js';
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
        console.log("Placing Order");
        document.getElementById('PlaceOrder').disabled = true;
        document.getElementById('CancelOrder').disabled = true;

        // '/api/neworder' , DELETE 
        // console.log("Button Clicked" + JSON.stringify(buttonId));
        // console.log("state = " + JSON.stringify(this.state));
        // console.log("object = " + this);
        //console.log("Adding to Cart, Book with ISBN = " + this.state.isbn13);
        //console.log("Cart updated ");
        
        var auth_token = cookies.getCookie('auth_token');
        var customerId = cookies.getCookie('customerId');
        var customerInfo = {"CustomerId" : customerId}; 

        fetch('/api/placeorder', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + auth_token
            }, 
            body: JSON.stringify(customerInfo)

        }).then(res => res.json())
        .then(replyFromServer => {
            console.log('response:', JSON.stringify(replyFromServer));
            /* 
            {
                "response": {
                    "CustomerId": 2
                },
                "status": "Success"
            }
            */
           if (replyFromServer['status'] == "Success")
           {
                document.getElementById('statusmessage').innerText = "Order# (" + replyFromServer['response']['order_request']['OrderID'] +") Placed Successfully (Redirecting to homepage in 5 seconds)";
                setTimeout(function () {
                    window.location.replace("/");
                }, 5000);
           }
           else {
                document.getElementById('statusmessage').innerText = "Failed to Place the order !! Reason: " + replyFromServer['response']['Reason'];
           }
            /* const book_list_data = document.querySelector('#book_list_data');
            ReactDOM.render(element(BookListData), book_list_data); */
        })
        .catch(error => console.error('Error:', error));
    }
    render(){
        return React.createElement('button', {key:this.props.addButtonId, id:'PlaceOrder', onClick: () => this.handleClick()},  'Place Order')
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
        console.log("Cancelling Order");
        document.getElementById('PlaceOrder').disabled = true;
        document.getElementById('CancelOrder').disabled = true;
        

        
        // '/api/neworder' , DELETE 
        // console.log("Button Clicked" + JSON.stringify(buttonId));
        // console.log("state = " + JSON.stringify(this.state));
        // console.log("object = " + this);
        //console.log("Adding to Cart, Book with ISBN = " + this.state.isbn13);
        //console.log("Cart updated ");
        var auth_token = cookies.getCookie('auth_token');
        var customerId = cookies.getCookie('customerId');
        var customerInfo = {"CustomerId" : customerId} ; 
        fetch('/api/deletecart', {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + auth_token
            }, 
            body: JSON.stringify(customerInfo)

        }).then(res => res.json())
        .then(replyFromServer => {
            console.log('response:', JSON.stringify(replyFromServer));
            /* 
            {
                "response": {
                    "CustomerId": 2
                },
                "status": "Success"
            }
            */
           if (replyFromServer['status'] == "Success")
           {
                document.getElementById('statusmessage').innerText = "Cart Emptied Successfully (Redirecting to homepage in 5 seconds)";
                setTimeout(function () {
                    window.location.replace("/");
                }, 5000);
           }
           else {
                document.getElementById('statusmessage').innerText = "Failed to Empty Cart!!";
           }
            /* const book_list_data = document.querySelector('#book_list_data');
            ReactDOM.render(element(BookListData), book_list_data); */
        })
        .catch(error => console.error('Error:', error));
    

        console.log("Status Message posted");
    }
    render(){
        return React.createElement('button', {key:this.props.addButtonId, id:'CancelOrder', onClick: () => this.handleClick()},  'Empty Cart')
    }
}

class CartEntriesHeading extends React.Component {
    constructor(props) {
      super(props);
      this.state = { 
        headings : [
            "ISBN-13",
            "Title",
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
        var auth_token = cookies.getCookie('auth_token');
        var customerId = cookies.getCookie('customerId');

        fetch("/api/cart/" + customerId, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + auth_token
            }, 
        }).then(serverresponse => {
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
        if (this.state.cartEntries.length > 0){
            for (var i = 0; i < this.state.cartEntries.length; i++){
                let cells = [];
                var BookId = `BookId${i}`;
                var TitleId = `TitleId${i}`;
                var QtyId = `qty${i}`;
                console.log(" cart: this.state.cartEntries[" , i , "] \n" , this.state.cartEntries[i] );
                cells.push(React.createElement('td', {key:BookId}, this.state.cartEntries[i]['BookId']));
                cells.push(React.createElement('td', {key:TitleId}, this.state.cartEntries[i]['Title']));
                cells.push(React.createElement('td', {key:QtyId}, this.state.cartEntries[i]['qty']));
             
                var thisRow = React.createElement(
                    'tr',
                    {key:`cart_entry_${i}`},
                    cells
                );
        
             console.log(cells);
             rows.push(thisRow);
            }
        }
        else {
            var messageCell = React.createElement('td',{key:0, colSpan:3, className:'count_cell'}, "Your Cart is Empty");
            var messageRow = React.createElement('tr', {key:0 }, messageCell);
            rows.push(messageRow);
        }
        
        console.log(rows);
        return rows;
    }
}
 

const cart_list_heading = document.querySelector('#cart_list_heading');
ReactDOM.render(React.createElement(CartEntriesHeading), cart_list_heading);
const cart_list_data = document.querySelector('#cart_list_data');
ReactDOM.render(React.createElement(CartEntriesData), cart_list_data);

const place_order_button = document.querySelector('#place_order_button');
ReactDOM.render(React.createElement(PlaceOrder), place_order_button);

const cancel_order_button = document.querySelector('#cancel_order_button');
ReactDOM.render(React.createElement(CancelOrder), cancel_order_button);

