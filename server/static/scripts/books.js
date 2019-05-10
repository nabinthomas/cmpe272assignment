'use strict';

const element = React.createElement;

class AddToCartButton extends React.Component {
    constructor(props){
        super(props);
        // console.log("Props = " + JSON.stringify(props));
        this.state = {
            isbn13 : props.isbn13
        };
    }

    handleClick(){
        // console.log("Button Clicked" + JSON.stringify(buttonId));
        // console.log("state = " + JSON.stringify(this.state));
        // console.log("object = " + this);
        console.log("Adding to Cart, Book with ISBN = " + this.state.isbn13);
    }
    render(){
        return element('button', {key:this.props.addButtonId, onClick: () => this.handleClick()},  '+')
    }
}
class BooksListHeadingRow extends React.Component {
    constructor(props) {
      super(props);
      this.state = { 
        headings : [
            "ISBN-13",
            "Title", 
            "Author(s)",
            "Price",
            "Available",
            "In Cart",
            "Add to Cart", // Add To Cart + button

        ]
      };
    }

    render() {
        let cells = [];

        for (var i = 0; i < this.state.headings.length; i++){
            cells.push(
                element('th', {key:i}, this.state.headings[i])
            );
        }
        return element(
            'tr',
            null,
            cells
        );
    }
}

class BookListData extends React.Component{
    constructor(props) {
        super(props);
        this.state = { 
          books : []
        };
      }

      componentDidMount() {
        this.setState({books: []});
        
        fetch("/api/books")
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
          console.log("The response.books from server was : ");
          console.log("******************************\n");
          console.log(data['response']['books']);
          console.log("******************************\n");
          this.state.messagefromserver = "";
          var booklist = []
          for (var bookIndex in data['response']['books']){
            /* ISBN13: "1",
            Title: "The Jungle Book", 
            Author: "Rudyard Kipling",
            Price: 24.0,
            AvailableCopies: 399,
            InCartCopies:0 */
            
            var formatted_book_data = {
                ISBN13 : data['response']['books'][bookIndex]['ISBN-13'],
                Title : data['response']['books'][bookIndex]['Title'],
                Author : data['response']['books'][bookIndex]['Author'],
                Price : data['response']['books'][bookIndex]['Price'],
                AvailableCopies : data['response']['books'][bookIndex]['Inventory'],
                InCartCopies : 0
            };
            booklist.push(
              formatted_book_data  
            ) ;
          }
          
          console.log(booklist);
          // Trigger a re-rendering with the new data
          this.setState({books:booklist}); 
        });
      }

      // render this component
      render() {
        let rows = [];
        for (var i = 0; i < this.state.books.length; i++){
            let cells = [];
            var isbn13id = `isbn13-${i}`;
            var titleId = `title-${i}`;
            var authorId= `author-${i}`;
            var priceId=`price-${i}`;
            var availableCopiesId = `availableCopies-${i}`;
            var inCartCopiesId = `inCartcopies-${i}`;
            var addButtonId = `add-${i}`;
            var addButtonCellId = `add-button-cell-${i}`;
            cells.push(element('td', {key:isbn13id}, this.state.books[i].ISBN13));
            cells.push(element('td', {key:titleId}, this.state.books[i].Title));
            var authorListString = '';
            for (var j = 0; j < this.state.books[i].Author.length; j++){
                if (j != 0) {
                    authorListString += " & ";
                }
                authorListString += this.state.books[i].Author[j];
            }
            cells.push(element('td', {key:authorId}, authorListString));
            cells.push(element('td', {key:priceId, className:'price_cell'}, '$' + this.state.books[i].Price.toFixed(2)));
            cells.push(element('td', {key:availableCopiesId, className:'count_cell'}, this.state.books[i].AvailableCopies));
            cells.push(element('td', {key:inCartCopiesId, className:'count_cell'}, this.state.books[i].InCartCopies));
            var addButton = element(AddToCartButton, {key:addButtonId, isbn13:this.state.books[i].ISBN13}, ''); 
            cells.push(element('td', {key:addButtonCellId, className:'button_cell'}, addButton));
            var thisRow = element(
                'tr',
                {key:`book-${i}`},
                cells
            );
            // console.log(cells);
            rows.push(thisRow);
        }
        // console.log(rows);
        return rows;
    }
}

const book_list_heading = document.querySelector('#book_list_heading');
ReactDOM.render(element(BooksListHeadingRow), book_list_heading);
const book_list_data = document.querySelector('#book_list_data');
ReactDOM.render(element(BookListData), book_list_data);